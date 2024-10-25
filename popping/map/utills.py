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




