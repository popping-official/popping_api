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

def crawling_data(request, url):
    TIME_SLEEP = 1
    
    # Selenium 설정
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # url = "https://www.diningcode.com/list.dc?query=서울맛집"
        driver.get(url)
        time.sleep(TIME_SLEEP)  # 페이지 로드 대기
        # 페이지 최하단까지 스크롤 (임시로 비활성화)
        
        index = 1
        
        while True:
            print(index)
            try:
                # 클래스가 SearchMore인 버튼 찾기
                search_more_button = driver.find_element(By.CLASS_NAME, 'SearchMore')
                # 버튼 클릭
                search_more_button.click()
                print('버튼 클릭')
                time.sleep(TIME_SLEEP)
            except Exception as e:
                print(f"Error or no more buttons: {e}")
                break

            index += 1


        # BeautifulSoup을 사용해 HTML 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(TIME_SLEEP)  # 페이지 로드 대기
        # 'sc-kMzDYw VwAlC PoiBlock' 클래스 값을 가진 a 태그 추출
        poi_blocks = soup.find_all('a', class_='PoiBlock')
        # print("poi_blocks")
        # print(len(poi_blocks))
        # 각 링크 클릭 후 title 추출
        titles = []
        best_menus = []
        points = []
        addrs = []
        telnums = []
        tags = []
        
        for i,block in enumerate(poi_blocks):
            relative_link = block.get('href')
            # print(f"Relative link: {relative_link}")  # 디버깅을 위해 출력
            if relative_link:
                absolute_link = f"https://www.diningcode.com{relative_link}"  # 절대 URL로 변경
                # print(f"Absolute link: {absolute_link}")  # 디버깅을 위해 출력
                driver.get(absolute_link)
                time.sleep(TIME_SLEEP)  # 페이지 로드 대기

                try:
                    # 새로운 페이지의 HTML 파싱
                    new_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    title_element = new_soup.find('h1', class_='tit')
                    if title_element:
                        title = title_element.get_text()
                        titles.append(title)
                        # print(f'Title: {title}')
                        
                    menu_element = new_soup.find_all('a', class_='btxt')
                    if menu_element:
                        menu_texts = [element.get_text() for element in menu_element]
                        best_menus.append(menu_texts)
                        
                    point_element = new_soup.find('strong', id='lbl_review_point')
                    if point_element:
                        point = point_element.get_text()
                        points.append(point)
                    
                    # li 태그 찾기
                    li_tag = new_soup.find('li', class_='locat')

                    # li 하위에 있는 a 태그의 마지막 요소 가져오기
                    last_a_in_li = li_tag.find_all('a')[-1]

                    # li 하위에 있는 div 하위에 있는 a 태그의 마지막 요소 가져오기
                    div_tag = li_tag.find('div')
                    last_a_in_div = div_tag.find_all('a')[-1]

                    # 결과 출력
                    li_text_value = last_a_in_li.get('href').replace('/list.dc?query=', '') if last_a_in_li else 'Not found'
                    div_text_value = last_a_in_div.get('href').replace('/list.dc?query=', '') if last_a_in_div else 'Not found'
                    addrs.append([li_text_value,div_text_value])
                    
                    tel_tag = new_soup.find('li', class_='tel')
                    if tel_tag:
                        tel = tel_tag.get_text()
                        telnums.append(tel)
                        
                    li_tag = new_soup.find('li', class_='tag')
                    a_tag = li_tag.find_all('a')
                    tag_texts = [element.get_text() for element in a_tag]
                    
                    li_tag = new_soup.find('li', class_='char')
                    a_tag = li_tag.find_all('a')
                    char_texts = [element.get_text() for element in a_tag]
                    
                    tags.append(tag_texts+char_texts)
                    
                except Exception as e:
                    print(f"Error: {e}")
                    continue
            print(i)
            if i == 1:
                break
        
        # 드라이버 종료
        driver.quit()
        
        # 결과 출력
        # for title in titles:
        #     print('Title 출력:')
        #     print(title)
        print(f'titles={titles}')
        print(f'best_menus={best_menus}')
        print(f'points={points}')
        print(f'addrs={addrs}')
        print(f'telnums={telnums}')
        print(f'tags={tags}')

    except Exception as e:
        print('Error')
        print(e)
        # 드라이버 종료
        driver.quit()
        
    return 