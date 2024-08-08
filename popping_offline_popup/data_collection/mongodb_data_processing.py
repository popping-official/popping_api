import pymongo
import re

# MongoDB 클라이언트 설정
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["popupstore_db"]
collection = db["popupstore_data"]

# 한글, 영어, 숫자, 기본 구두점을 제외한 모든 문자를 제거하는 정규 표현식 패턴
emoji_pattern = re.compile("[^"
                           u"\uAC00-\uD7A3"  # 한글
                           u"\u1100-\u11FF"  # 한글 자모
                           u"\u3130-\u318F"  # 한글 호환 자모
                           u"\uA960-\uA97F"  # 한글 자모 확장-A
                           u"\uD7B0-\uD7FF"  # 한글 자모 확장-B
                           u"\u4E00-\u9FFF"  # 한자
                           u"\u3040-\u309F"  # 히라가나
                           u"\u30A0-\u30FF"  # 가타카나
                           u"\uFF00-\uFFEF"  # 반각 및 전각 형태
                           u"\u0000-\u007F"  # ASCII
                           u"\u0080-\u00FF"  # Latin-1 Supplement
                           u"\u0100-\u017F"  # Latin Extended-A
                           u"\u0180-\u024F"  # Latin Extended-B
                           u"\u0250-\u02AF"  # IPA Extensions
                           u"\u02B0-\u02FF"  # Spacing Modifier Letters
                           u"\u0300-\u036F"  # Combining Diacritical Marks
                           u"\u0370-\u03FF"  # Greek and Coptic
                           u"\u0400-\u04FF"  # Cyrillic
                           u"\u0500-\u052F"  # Cyrillic Supplement
                           u"\u2000-\u206F"  # General Punctuation
                           "]+", flags=re.UNICODE)


# 데이터에서 이모티콘을 제거하는 함수
def remove_emojis(text):
    return emoji_pattern.sub(r'', text)


# 컬렉션의 모든 문서에 대해 이모티콘을 제거하고 업데이트
for doc in collection.find():
    new_values = {}
    for key, value in doc.items():
        if isinstance(value, str):
            new_values[key] = remove_emojis(value)
        else:
            new_values[key] = value

    # 문서를 업데이트
    collection.update_one({"_id": doc["_id"]}, {"$set": new_values})

print("Emojis removed from all documents.")
# 모든 문서를 순회하면서 각 필드의 문자열 공백 제거 및 업데이트
for doc in collection.find():
    updated_fields = {}
    for key, value in doc.items():
        if isinstance(value, str):
            trimmed_value = value.strip()  # 맨 처음과 맨 마지막 공백 제거
            if trimmed_value != value:
                updated_fields[key] = trimmed_value

    # 변경된 필드가 있는 경우에만 업데이트
    if updated_fields:
        collection.update_one({"_id": doc["_id"]}, {"$set": updated_fields})

print("Leading and trailing spaces removed from all string fields in all documents.")

# title 필드를 기준으로 중복된 데이터를 하나만 남기고 제거하는 파이프라인
pipeline = [
    {"$group": {
        "_id": "$title",
        "ids": {"$push": "$_id"},
        "count": {"$sum": 1}
    }},
    {"$match": {"count": {"$gt": 1}}}
]

# 중복된 문서를 찾는 파이프라인 실행
duplicates = collection.aggregate(pipeline)
# 중복된 문서를 삭제
for group in duplicates:
    print(group)
    ids = group["ids"]
    # 첫 번째 문서를 제외하고 나머지 중복된 문서의 ID를 가져와 삭제
    for id_to_delete in ids[1:]:
        print(id_to_delete)
        collection.delete_one({"_id": id_to_delete})

print("Duplicates removed, only one document per title retained.")

result = collection.delete_many({"title": {"$regex": "zip", "$options": "i"}})
print(f"Deleted {result.deleted_count} documents with 'zip' in the title.")

result = collection.delete_many({
    "$or": [
        {"title": None},
        {"locations": None},
        {"dates": None},
        {"times": None}
    ]
})

print(f"Deleted {result.deleted_count} documents with null values in title, locations, dates, or times.")