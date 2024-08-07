import instaloader
from datetime import datetime, timedelta
import pytz
import json
import time
import os
from pymongo import MongoClient, errors
import google.generativeai as genai
from dotenv import load_dotenv

# KST 시간대 설정
kst = pytz.timezone('Asia/Seoul')
today = datetime.now(kst)

# MongoDB 클라이언트 설정
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['popupstore_db']
    collection = db['popupstore_data']
except errors.ServerSelectionTimeoutError as err:
    print(f"MongoDB connection error: {err}")
    exit(1)

# Instaloader 설정
L = instaloader.Instaloader()

# 인스타그램 계정 로그인
L.login('shoesmy', 'asd1659311')

# GPT API 설정
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1.15,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="1.팝업스토어의 title, locations, dates, times, events를 가지고 온다.\n2.dates는 yyyy-mm-dd 의 형태로 start, end로 구분되고, times은 요일: 00:00 ~ 00:00의 형태를 가지고있다. \n3.#로 시작하는 해시태그 형태의 데이터는 무시한다.\n4.각 새로운 prompt는 위의 데이터와 독립적으로 작용한다. 이제까지의 대화를 학습하지 않아도 된다.\n5.locations의 경우 한국의 도로명주소나 지명주소로 이루어져 있다. 예) 강남구 테헤란로 517, 현대백화점 무역센터점 B1 대행사장 \n6.결과는 {\"title\":str, \"locations\": [str], \"dates\": {\"start\": str,\"end\": str}, \"times\": {}, \"events\": [str]} 이거나 Array[{\"title\":str, \"locations\": [str], \"dates\": {\"start\": str,\"end\": str}, \"times\": {}, \"events\": [str]}]의 형태를 무조건 준수해야한다.",
    )

def insta_popup_data_get(insta_id: str, days: int = 365, batch_size: int = 5, rpm_limit: int = 14):
    last_date = today - timedelta(days=days)
    posts_data = []
    existing_data = set()
    data_file = 'popupstore_data.json'

    # 기존 데이터 파일이 존재하면 로드
    if os.path.exists(data_file):
        print("Existing data file found. Loading data from file.")
        with open(data_file, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
    else:
        # Instaloader를 사용하여 데이터 수집
        profile = instaloader.Profile.from_username(L.context, insta_id)
        posts = profile.get_posts()

        total_posts = 0  # 필터링된 포스트 수 초기화

        # 순차적으로 포스트 저장
        for post in posts:
            post_date = post.date_local.astimezone(kst)
            if post_date < last_date:
                break  # 설정된 날짜 범위 벗어나면 중단
            if post_date > today:
                continue  # 미래 날짜 포스트는 건너뜀

            total_posts += 1  # 필터링된 포스트 수 증가

            caption = post.caption
            date_str = post_date.strftime('%Y-%m-%d %H:%M:%S')
            post_info = f"{caption}\n{date_str}\n"
            post_info_hash = json.dumps({"caption": caption, "date": date_str}, ensure_ascii=False)

            # 중복 확인
            if post_info_hash in existing_data or collection.count_documents({"caption": caption, "date": date_str}, limit=1) > 0:
                continue

            posts_data.append({"caption": caption, "date": date_str})

            # 진행율 출력
            progress = (len(posts_data) / total_posts) * 100
            print(f"Progress: {progress:.2f}% ({len(posts_data)}/{total_posts})")

        # JSON 파일로 저장
        if posts_data:
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(posts_data, f, ensure_ascii=False, indent=4)

    # 모든 포스트 저장 완료 후 GPT API 요청
    post_batch = []
    gpt_responses = []
    for i, post in enumerate(posts_data):
        post_batch.append(post["caption"] + "\n" + post["date"])
        if (i + 1) % batch_size == 0 or (i + 1) == len(posts_data):
            response_json = send_message_to_gpt(post_batch)
            if isinstance(response_json, list):
                gpt_responses.extend(response_json)
            elif isinstance(response_json, dict):
                gpt_responses.append(response_json)
            post_batch = []
            # 1분에 rpm_limit 이상 요청하지 않도록 60초 대기
            time.sleep(60 / rpm_limit)

    # GPT 응답을 MongoDB 및 JSON 파일에 저장
    if gpt_responses:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(gpt_responses, f, ensure_ascii=False, indent=4)

        if isinstance(gpt_responses, list) and all(isinstance(item, dict) for item in gpt_responses):
            try:
                collection.insert_many(gpt_responses)
            except errors.BulkWriteError as bwe:
                print(f"Bulk write error: {bwe.details}")
        else:
            print("Data format is incorrect. It should be a list of dictionaries.")

def send_message_to_gpt(post_batch):
    message = "\n".join(post_batch)
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(message)
    print("GPT API Response: ", response.text)  # 응답 데이터 출력
    try:
        response_data = json.loads(response.text)  # JSON 형태의 응답을 파싱
    except json.JSONDecodeError as e:
        print("JSONDecodeError: ", e)
        return []

    # 응답이 리스트 안에 딕셔너리 형태 또는 딕셔너리 형태인지 확인
    if isinstance(response_data, dict):
        return [response_data]
    elif isinstance(response_data, list):
        if all(isinstance(item, dict) for item in response_data):
            return response_data
        else:
            print("Unexpected data format received from GPT API.")
            return []
    return []

# 실행 예시
insta_popup_data_get('popupstorego', days=30, batch_size=10, rpm_limit=14)