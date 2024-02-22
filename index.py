# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re

from selenium.webdriver.chrome.options import Options



#셀레니움 크롬 드라이버 116버전
chrome_options = webdriver.ChromeOptions()


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"


chrome_options.add_argument('user-agent=' + user_agent)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
chrome_options.add_argument('incognito')
chrome_options.add_argument('headless')

driver = webdriver.Chrome('/Users/remy/Downloads/chromedriver-mac-arm64/chromedriver')



#각 크롤링 결과 저장하기 위한 리스트 선언

pressName =[]
contacts =[]
company = []
introduction = []
category = []

age10 = []
age20 = []
age30 = []
age40 = []
age50 = []
age60 = []
male = []
female = []

result={}


#엑셀로 저장하기 위한 변수
RESULT_PATH ='/Users/remy/Desktop/python study/beautifulSoup_ws/crawling_result/'  #결과 저장할 경로
now = datetime.now() #파일이름 현 시간으로 저장하기




#신문사별 기자목록 페이지 불러오기
urlLists = [
    "https://contents.premium.naver.com/ch/list?categoryId=all&stype=weeklySubscriber&ctype=premium"
]



for k in range(len(urlLists)):
    url = urlLists[k]
    # response = requests.get(url)
    # html = response.text
    driver.get(url)

    #스크롤
    SCROLL_PAUSE_SEC = 3

    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    #소스 가져오기
    html = driver.page_source

    title_text = []
    link_text = []
    sec_text = []

    #뷰티풀소프의 인자값 지정
    soup = BeautifulSoup(html, 'html.parser')

    #<a>태그에서 제목과 링크주소 추출
    atags = soup.select('.pcp_link')
    # spantags = soup.select('div.journalist_list_content_info > span:nth-child(2)')

    for atag in atags:
        # title_text.append(atag.text)     #기자이름
        link_text.append(atag['href'])   #링크주소
    # for spantag in spantags:
    #     sec_text.append(spantag.text)   #메인에서 섹션정보 가져옴
    # print(title_text)
    # print(sec_text)
    print(link_text)

    for i in range(len(link_text)):
        url2 = 'https://contents.premium.naver.com'+link_text[i] +'/profile'
        print(url2)
        driver.implicitly_wait(10)  # seconds
        driver.get(url2)
        html2 = driver.page_source
        soup2 = BeautifulSoup(html2, 'html.parser')
        # response2 = requests.get(url2)
        # html2 = response2.text
        # soup2 = BeautifulSoup(html2, 'html.parser')

        try:
            #기자명
            results = soup2.find('a', "main_content_title").get_text().strip()
            print(results)
            #이메일
            results2 = driver.find_element(By.XPATH,'//a[@data-clk="chlh_fot.cpinfomail"]').text
            print(results2)
            # #언론사명
            # results3 = driver.find_element(By.XPATH,'//*[@id="ct"]/div[1]/div[2]/div[3]/div/div[4]/div/div/dl/div[2]/dd').text
            # print(results3)

            # # #기자소개
            # results4 = soup2.find('p', "media_reporter_profile_introduce").get_text().strip()
            # # #카테고리
            # # results5 = soup2.select_one('ul.media_reporter_summary_list > li:nth-child(2) > em').string
            # results5 = sec_text[i]


            # #인구통계
            # #10대
            # results6 = soup2.select_one('div.media_reporter_profile_subscriber_statistics > div > dl > div:nth-child(1) > dd > div > span.percent').string
            # #20대
            # results7 = soup2.select_one('div.media_reporter_profile_subscriber_statistics > div > dl > div:nth-child(2) > dd > div > span.percent').string
            # #30대
            # results8 = soup2.select_one('div.media_reporter_profile_subscriber_statistics > div > dl > div:nth-child(3) > dd > div > span.percent').string
            # #40대
            # results9 = soup2.select_one('div.media_reporter_profile_subscriber_statistics > div > dl > div:nth-child(4) > dd > div > span.percent').string
            # #50대
            # results10 = soup2.select_one('div.media_reporter_profile_subscriber_statistics > div > dl > div:nth-child(5) > dd > div > span.percent').string
            # #60대
            # results11 = soup2.select_one('div.media_reporter_profile_subscriber_statistics > div > dl > div:nth-child(6) > dd > div > span.percent').string
            # # #성별
            # results12 = soup2.select_one('div.media_reporter_profile_subscriber_statistics > div > div > dl > dd.blind._male').string
            # # results13 = soup2.select_one('div.media_reporter_profile_subscriber_statistics > div > div > dl > dd:nth-child(2)').string

            pressName.append(results)
            contacts.append(results2)
            # company.append(results3)
            # introduction.append(results4)
            # category.append(results5)

            # age10.append(results6)
            # age20.append(results7)
            # age30.append(results8)
            # age40.append(results9)
            # age50.append(results10)
            # age60.append(results11)
            # male.append(results12)
            # female.append(results13)
        except:
            pass



    print(urlLists[k])


# 모든 리스트 딕셔너리형태로 저장
# result = {"기자명": pressName, "이메일": contacts, "분야": category, "언론사": company, "기자소개": introduction}
# result = {"기자명": pressName, "이메일": contacts, "분야": category, "언론사": company}
result = {"기자명": pressName, "이메일": contacts}
# result = {"기자명": pressName, "이메일": contacts}


df = pd.DataFrame(result)  # df로 변환

# 새로 만들 파일이름 지정
outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
df.to_excel(RESULT_PATH+outputFileName,sheet_name='sheet1')




#
# #신문사 추출
# source_lists = soup.select('.info_group > .press')
# for source_list in source_lists:
#     source_text.append(source_list.text)    #신문사
#
# #날짜 추출
# date_lists = soup.select('.info_group > span.info')
# for date_list in date_lists:
#     # 1면 3단 같은 위치 제거
#     if date_list.text.find("면") == -1:
#         date_text.append(date_list.text)
#
# #본문요약본
# contents_lists = soup.select('.news_dsc')
# for contents_list in contents_lists:
#     contents_cleansing(contents_list) #본문요약 정제화
#
#
# #모든 리스트 딕셔너리형태로 저장
# result= {"date" : date_text , "title":title_text ,  "source" : source_text ,"contents": contents_text ,"link":link_text }
# print(page)
#
# df = pd.DataFrame(result)  #df로 변환
# page += 10