import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from .mongodb import MongoDBClient

def insert_mongo(request, data, collection_name, option):
    collection = MongoDBClient.get_collection('poppingmongo',collection_name)
    
    match option:
        case 'one':
            pass
        
        case 'many':
            collection.insert_many(data)
    
    return

# 다이닝 크롤링 코드
def crawling_data(request, url, option):
    TIME_SLEEP = 0.5
    
    # Selenium 설정
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url)
        time.sleep(TIME_SLEEP)  # 페이지 로드 대기
        # 페이지 최하단까지 스크롤 (임시로 비활성화)
        
        
        while True:
            try:
                # 클래스가 SearchMore인 버튼 찾기
                search_more_button = driver.find_element(By.CLASS_NAME, 'SearchMore')
                # 버튼 클릭
                search_more_button.click()
                time.sleep(TIME_SLEEP)
            except Exception as e:
                # print(f"Error or no more buttons: {e}")
                break

        # BeautifulSoup을 사용해 HTML 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(TIME_SLEEP)  # 페이지 로드 대기
        # 'sc-kMzDYw VwAlC PoiBlock' 클래스 값을 가진 a 태그 추출
        poi_blocks = soup.find_all('a', class_='PoiBlock')
        # 각 링크 클릭 후 title 추출
        place_list = []
        
        for i,block in enumerate(poi_blocks):
            relative_link = block.get('href')
            
            if relative_link:
                absolute_link = f"https://www.diningcode.com{relative_link}"  # 절대 URL로 변경
                driver.get(absolute_link)
                time.sleep(TIME_SLEEP)  # 페이지 로드 대기

                try:
                    temp_dict={}
                    # 새로운 페이지의 HTML 파싱
                    new_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    title_element = new_soup.find('h1', class_='tit')
                    if title_element:
                        title = title_element.get_text()
                        temp_dict['title'] = title
                        
                    menu_element = new_soup.find_all('a', class_='btxt')
                    if menu_element:
                        menu_texts = [element.get_text() for element in menu_element]
                        temp_dict['bestMenu'] = menu_texts
                        
                    point_element = new_soup.find('strong', id='lbl_review_point')
                    if point_element:
                        point = point_element.get_text()
                        temp_dict['gradePoint'] = float(point)
                    
                    # li 태그 찾기
                    li_tag = new_soup.find('li', class_='locat')

                    # li 하위에 있는 a 태그(도로명 + 지명)
                    a_in_li_all = li_tag.find_all('a')
                    
                    # li 하위에 있는 div 하위에 있는 a 태그(지명)
                    div_tag = li_tag.find('div')
                    num_addr_a = div_tag.find_all('a')
                    # num_addr_a_last = div_tag.find_all('a')[-1]
                    num_addr_a_last = div_tag.find('span', class_='profile_jibun')

                    # 도로명 + 지명 - 지명 = 도로명
                    load_addr_a = [item for item in a_in_li_all if item not in num_addr_a][-1]

                    # 결과 출력 도로명, 지명 주소
                    load_addr_value = load_addr_a.get('href').replace('/list.dc?query=', '') if load_addr_a else 'Not found'
                    # num_addr_'value' = num_addr_a_last.get('href').replace('/list.dc?query=', '') if num_addr_a_last else 'Not found'
                    num_addr_value = num_addr_a_last.get_text(separator="")
                    temp_dict['loadAddr'] = load_addr_value
                    temp_dict['numberAddr'] = num_addr_value
                    
                    tel_tag = new_soup.find('li', class_='tel')
                    if tel_tag:
                        tel = tel_tag.get_text()
                        temp_dict['telNumber'] = tel
                        
                    li_tag = new_soup.find('li', class_='tag')
                    a_tag = li_tag.find_all('a')
                    
                    # 모든 a 태그를 대상으로 텍스트를 추출하면서 '다코'가 포함된 경우에는 빈 문자열로 대체
                    tag_texts = [
                        element.get_text().replace('다코', '') if '다코' in element.get_text() else element.get_text() 
                        for element in a_tag
                    ]
                    temp_dict['tag'] = tag_texts
                    
                    li_tag = new_soup.find('li', class_='char')
                    a_tag = li_tag.find_all('a')
                    char_texts = [element.get_text() for element in a_tag]
                    temp_dict['char'] = char_texts
                    
                    temp_dict['option'] = option
                    
                    place_list.append(temp_dict)
                    
                except Exception as e:
                    print(f"Error: {e}")
                    continue
                
            # if i == 4:    
            #     break
        
        # 드라이버 종료
        driver.quit()
        
    except Exception as e:
        print('Error')
        print(e)
        # 드라이버 종료
        driver.quit()
        
    return place_list

# 인스타 크롤링 팝업 json data 가공 코트
def json_test(request):
    # JSON 파일 경로 지정
    file_path = 'C:/big15/popping_api/popping_offline_popup/data/popupstore_data.json'

    # JSON 파일 열기
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    popup_list = []
    '''
        title = me.StringField(required=False)
        location = me.StringField(required=False)
        startDate = me.DateTimeField(required=False)
        endDate = me.DateTimeField(required=False)
        opneTime = me.ListField(me.StringField(),required=True, unique=True)
        event = me.ListField(me.StringField(),required=True, unique=True)
    '''
    for popup in data:
        
        temp_dict = {}
        
        temp_dict['title'] = popup['title']
        
        # [{addr:'',placeName:''},{}]
        location_list = []
        for item in popup['locations']:
            location_dict = {}
            tepm_item = item.split(',')
            try:
                location_dict = {
                    'address':tepm_item[0],
                    'placeName':tepm_item[1]
                }
            except:
                location_dict = {
                    'address':tepm_item[0],
                    'placeName':''
                }
            location_list.append(location_dict)
        temp_dict['location'] = location_list
        try:
            if popup['dates']['start']:
                try:
                    start_date = datetime.strptime(popup['dates']['start'], '%Y-%m-%d')
                except:
                    
                    current_year = datetime.now().year
                    start_date_str = f"{current_year}-{popup['dates']['start']}".replace('.','-')
                    
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                    
            temp_dict['startDate'] = start_date
        except:
            temp_dict['startDate'] = None
        
        try:
            if popup['dates']['end']:
                try:
                    end_date = datetime.strptime(popup['dates']['end'], '%Y-%m-%d')
                except:
                    
                    current_year = datetime.now().year
                    end_date_str = f"{current_year}-{popup['dates']['end']}".replace('.','-')
                    
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                    
            temp_dict['endDate'] = end_date
        except:
            temp_dict['endDate'] = end_date
            
        if popup['times']:
            opne_date_list = []
            for key, val in popup['times'].items():
                opne_date_list.append( f'{key} : {val}')
            temp_dict['openTime'] = opne_date_list
        
        temp_dict['event'] = popup['events']
        popup_list.append(temp_dict)
        
    return popup_list

# 주소 지오코딩
def geocode_address(address):
    list_ = address.split(' ')
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": '+'.join(list_),
        "format": "json",
        "polygon_geojson":1
    }
    response = requests.get(base_url, params=params)
    time.sleep(1)
    if response.status_code == 200:
        geocode_result = response.json()
        if geocode_result:
            location = geocode_result[0]
            return {"lat": location["lat"], "lon": location["lon"]}
        else:
            return None
    else:
        print(response.status_code)
        return None



