# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 22:43:19 2022

@author: SAKURA-x
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller

from bs4 import BeautifulSoup
import time

#import sys
#sys.path.append('C:\\git')
#
#from yhlibe import controller as controller
#from yhlibe import Datelib

#이거 예전 lib 위치를 가지고 있음
#from yhlibe import stocklib

import pyperclip
import csv

import requests
import re
import os
import random

import datetime
import threading

import warnings
warnings.filterwarnings("ignore")
chromedriver_autoinstaller.install()


driver = ''
DATETYPE = '%Y-%m-%d-%H'
# DATETYPE2 = '%Y.%m.%d'

def DateToString(value):
    if value == 'now':
        value = datetime.datetime.now()
        
    # day = value.day    
    # month = value.month
    
    # if len(str(day)) == 1:
    #     day = '0' + str(day)
            
    # if len(str(month)) == 1:
    #     month = '0' + str(month)
    
    # String = str(year)+str(month)+str(day)    
    String = value.strftime(DATETYPE)
    return String  

def StringToDate(value):
    return datetime.datetime.strptime(value, DATETYPE)

# def StringToDate2(value):
#     return datetime.datetime.strptime(value, DATETYPE2)

def StringToDateV2(value, tDATETYPE = DATETYPE):
    return datetime.datetime.strptime(value, tDATETYPE)

def IncreaseDate(nowDateString, value, val):
    
    date = StringToDate(nowDateString)
    if value == 'day':
        date = date + datetime.timedelta(days=val)
    elif value == 'second':
        date = date + datetime.timedelta(seconds=val)

    String = date.strftime(DATETYPE)
    
    return String


# STARTDATE = '2017-01-01'
# ENDDATE = DateToString('now')

import itertools

def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)



def scrollDown(driver):
    for i in range(6):
        ActionChains(driver).send_keys(Keys.DOWN).perform()


def scrollDownTime(driver, sec):
    for i in range(sec):
        for i in range(6):
            ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)

def overTimer():
    global driver
    print('최대 탐색 시간 초과')
#    iterate = False
    driver.close()
#    raise ValueError('over search time')

def clickXpathByClass(classId, string):
    global driver
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    numList = soup.find_all(class_= classId)

    nextNum = numList[0].findNext('a')
    while(True):
        if string == str(nextNum.getText()):
            break
        nextNum = nextNum.findNext('a')
    
    xpath = xpath_soup(nextNum)
    selenium_element = driver.find_element_by_xpath(xpath)
#    ActionChains(driver).move_to_element(selenium_element).perform()
    selenium_element.click()
    

def readCsv(path):
    f = open(path, 'r', encoding='utf-8')
    cin = csv.reader(f, delimiter=',')
    temp = [row for row in cin]
    f.close()
    return temp


allCount = 0
ipAddr = ''
timer = ''


timerule = readCsv('../settime.txt')
_timeRule = []
for _rule in timerule:
    if _rule[0][0] != '#':
        _timeRule.append([int(_rule[0]), int(_rule[1])])
    
    
while(True):
    
    try:
        addTime = 1
        
        if timer != '': 
            timer.cancel()
        
        #새벽시간입니다.
        if _timeRule[-1][-1] == 1:
            H = int(DateToString('now').split('-')[-1])
            if 2 <= H and  7 >= H:
                addTime = _timeRule[-1][0]
                print('새벽시간 이므로',addTime,'(초) 만큼 시간이 추가됨')
            
        allCount += 1
        print('시도 횟수', allCount)
        
        s = time.time()
        
        print(ipAddr)
        
        os.popen('cd C:/git/adb && C:/git/adb/ipch.bat')
        print('IP 주소 변경')
        
        while(True):
            try:
                req = requests.get("http://ipconfig.kr")
                print(re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1])
                ipAddr = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]
                break
            except:
                pass
        
        #def checkip():
        #    res = requests.get('http://ipconfig.kr') # 아이피 알려주는 단순 사이트에 접속해 값 리턴
        #    soup = BeautifulSoup(res.text, 'html.parser')
        #    ip = soup.select_one('body').getText().split() # soup.find 사용해도 됨 배열 형태로 
        #    return ip
        #
        #checkip()
        
        #auto selenium()
        
        
        #cookies = driver.get_cookies()
        
        #driver = webdriver.Chrome('../chromedriver_win3298/chromedriver')
        
        #url = 'https://naver.com'
        #driver.get(url)
        
        time.sleep(5)
        
        options = webdriver.ChromeOptions() 
        #options.add_argument("--auto-open-devtools-for-tabs")
        
        mobile_emulation = { "deviceName": "Nexus 5" }
        
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        #driver = webdriver.Chrome(options=options, executable_path=r'../chromedriver_win3298/chromedriver')
        driver = webdriver.Chrome(options=options)
        driver.get("https://google.com")
        #print(driver.title)
        
        newsCount = random.randrange(_timeRule[0][0],_timeRule[0][1])
        searchCount = random.randrange(_timeRule[2][0],_timeRule[2][1])
        
        timer = threading.Timer(1201+(addTime*(5+newsCount+searchCount)), overTimer)
        timer.start()

        time.sleep(2)
        driver.get("https://naver.com")
        
        scrollDown(driver)
        time.sleep(1)
        scrollDown(driver)
        time.sleep(1)
        
        
        clickXpathByClass('nav_list_wrap native_scroll', '뉴스')
#        driver.find_element_by_xpath('//*[@id="NAV_LIST"]/ul/li[12]/a').click()
        
        time.sleep(1)
        
        print('### 뉴스')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find_all(class_='cjs_news_a')
        
        news = []
        for _title in title: 
            #print(_title.attrs['href'])
            news.append(_title.attrs['href'])
        
#        newsCount = random.randrange(2,5)
#        newsCount = random.randrange(_timeRule[0][0],_timeRule[0][1])
            
        print('볼 뉴스', newsCount)
        
        for _ in range(newsCount):
            newsNum = random.randrange(1, len(news))
            print('볼 뉴스 번호', newsNum)
            driver.get(news[newsNum])
#            newsTime =  random.randrange(30, 60)
            newsTime =  random.randrange(_timeRule[1][0]+addTime,_timeRule[1][1]+addTime)
            
            
            print('뉴스 체류 시간',newsTime)
            scrollDownTime(driver, newsTime)
            
        time.sleep(1)
        #len(driver.get_cookies())
        
        
        print('### 실시간 검색어 검색')
        
        words = readCsv('../realtimekeyword.txt')
        n = []
        for _word in words:
            n.append(_word[0])
        print('txt에 있는 검색어 갯수 :', len(n))
              
#              
#              
#        n = [
#'최민정',
#'컬링',
#'서른 아홉',
#'곽윤기',
#'나이키',
#'손예진',
#'안철수',
#'이유빈',
#'소상공인 방역지원금',
#'김아랑',
#'나는 솔로',
#'우크라이나',
#'손예진',
#'RE100',
#'김종국',
#'김원웅',
#'곽윤기',
#'최민정 쇼트트랙 1500 M',
#'잠실새내역 이재명 대선',
#'정동원 코로나 무증상',
#'10시로 6인 유지',
#'방역지원금',
#'러시아 우크라이나',
#'유영',
#'발리예바',
#'서른아홉',
#'트루소바',
#'영탁',
#'촛불로 쫓겨난 세력 5년만에',
#'소상공인 방역지원금',
#'우크라 주권 해결',
#'이혜성',
#'이준석 복합쇼핑몰 광주',
#'청년희망적금 자격',
#'러시아',
#'생생정보',
#'싱어게인2',
#'윤석열',
#'러시아 우크라이나',
#'방역지원금',
#'이재명 윤석열 갤럽',
#'국제사회 제재에 동참',
#'나스닥',
#'돈바스',
#'청년희망적금',
#'서른 아홉',
#'체르노빌',
#'한가인'
#        ]
        
        #request 값이 다르기에 버튼 클릭으로 변경
        #driver.get('https://naver.com')
        #뉴스에서는 클릭이 안됨
        #driver.find_element_by_xpath('//*[@id="_sch"]/section/div/h1/a[1]').click()
        while(True):
#            print(driver.current_url)
            if driver.current_url == ('https://m.naver.com/'):
                break
            driver.back()
            time.sleep(0.3)
        
#        searchCount = random.randrange(0,3)
#        searchCount = random.randrange(_timeRule[2][0],_timeRule[2][1])
        print('검색어 찾기 갯수', searchCount)
        
#        searchKey = random.randrange(1, len(n))
#        for _key in n[searchKey]:
#            driver.find_element_by_xpath('//*[@id="query"]').send_keys(_key)
#            time.sleep(0.3)
#            
#            
#        driver.find_element_by_xpath('//*[@id="query"]').send_keys('\n')
#        
##        searchTime =  random.randrange(30, 60)
#        searchTime =  random.randrange(_timeRule[3][0], _timeRule[3][1])
#        print('검색 체류 시간',searchTime)
#        scrollDownTime(driver, searchTime)
        
        for k in range(searchCount):
            searchKey = random.randrange(1, len(n))
            
            if k == 0:
                for _key in n[searchKey]:
                    driver.find_element_by_xpath('//*[@id="query"]').send_keys(_key)
                    time.sleep(0.3)
                    
                    
                driver.find_element_by_xpath('//*[@id="query"]').send_keys('\n')
            
            else:
                driver.find_element_by_xpath('//*[@id="nx_input_clear"]/i').click()    
                
                for _key in n[searchKey]:
                    driver.find_element_by_xpath('//*[@id="nx_query"]').send_keys(_key)
                    time.sleep(0.3)
                driver.find_element_by_xpath('//*[@id="nx_query"]').send_keys('\n')
            
#            searchTime =  random.randrange(30, 60)
            searchTime =  random.randrange(_timeRule[3][0]+addTime,_timeRule[3][1]+addTime)
            
            print('검색 체류 시간',searchTime)
            scrollDownTime(driver, searchTime)
            
        time.sleep(1)
        
        print('### 쇼핑')
#        text = '레진'
#        itemCode = '83197330370'
#        text = '사과'
#        itemCode = '82755608411'
        
        words = readCsv('../shopkeyword.txt')
        
        wordKey = random.randrange(0, len(words))
        
        text = words[wordKey][0]
        itemCode = words[wordKey][1]
        
        print(text, itemCode)
        
        
#        text = '귤'
#        itemCode = '82850708305'        
        
        ## 왠지 모르겠는데 실시간 검색어 이후 에러 ㅜ 한줄 실행시 잘됨
#        ActionChains(driver).send_keys(Keys.HOME).perform()
#        
#        time.sleep(0.5)
#        driver.find_element_by_xpath('//*[@id="_sch"]/section/div/h1/a[1]/i').click()
#        time.sleep(0.5)
#        driver.find_element_by_xpath('//*[@id="MM_logo"]/a/span').click()
#        time.sleep(0.5)
#        driver.find_element_by_xpath('//*[@id="MM_aside_shortcut_wrap"]/div[1]/div[1]/ol/li[5]/a').click()
#        time.sleep(0.5)
        
#        driver.find_element_by_xpath('//*[@id="sear"]').click()    
#            
#        for _key in text:
#            driver.find_element_by_xpath('//*[@id="sear"]').send_keys(_key)
#            time.sleep(0.3)
#        driver.find_element_by_xpath('//*[@id="sear"]').send_keys('\n')        
        
        
#        driver.get('https://m.naver.com/')
#        https://m.naver.com/aside/
#        https://m.shopping.naver.com/home/m/index.naver
        
        driver.find_element_by_xpath('//*[@id="nx_input_clear"]/i').click()
        
        for _key in text:
            driver.find_element_by_xpath('//*[@id="nx_query"]').send_keys(_key)
            time.sleep(0.3)
        driver.find_element_by_xpath('//*[@id="nx_query"]').send_keys('\n')
        
        time.sleep(1)
        
        clickXpathByClass('api_list_scroll_wrap', '쇼핑')
#        driver.find_element_by_xpath('//*[@id="_sch_tab"]/div[1]/div/div/ul/li[2]/a').click()

        time.sleep(1)
        
        
        rank = 0
        n = 1
        
        nexeFlag = True
        while(nexeFlag):
            
            for _ in range(5):
                ActionChains(driver).send_keys(Keys.END).perform()
                time.sleep(1)
        
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find_all(class_='product_list_item__2tuKA')
            
            for idx, _title in enumerate(title):
                
                element = driver.find_element(by='id', value=_title['id'])
                ActionChains(driver).move_to_element(element).perform()
                
                if str(_title).find('광고') == -1:
                    rank += 1    
                
                ## 찾은 경우
                if str(_title['id']).find(itemCode) != -1:
                    print('현재 상품 순위 :', rank)
                    driver.find_element(by='id', value=_title['id']).click()
                    nexeFlag = False
                    break
                
                
                ## 없는 경우
                if idx == len(title)-1:
                    n += 1
                    print('다음페이지로 이동', n)
                
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    numList = soup.find_all(class_='paginator_list_paging__2cmhX')
                
                    nextNum = numList[0].findNext('a')
                    while(True):
                        if n == int(nextNum.getText()):
                            break
                        nextNum = nextNum.findNext('a')
                    
                    xpath = xpath_soup(nextNum)
                    selenium_element = driver.find_element_by_xpath(xpath)
                    ActionChains(driver).move_to_element(selenium_element).perform()
                    selenium_element.click()
                   
                    
                if n >= 11:
                    nexeFlag = False
#                    print('최대 탐색 범위를 넘김')
                    
                    
                    raise ValueError('최대 shop 탐색 범위를 넘김')
                         
            
            
#        ActionChains(driver).send_keys(Keys.HOME).perform()
        time.sleep(1)    

        
# 한개씩 탐색하면서 추가로 나오는 것을 list에 추가해서 탐색하는 로직인데 에러가 있음        
#        rank = 0
#        
#        html = driver.page_source
#        soup = BeautifulSoup(html, 'html.parser')
#        title = soup.find_all(class_='product_list_item__2tuKA')
#        
#        _count = 0
##        for idx, _title in enumerate(title):
##        while(True):
#
##            print(len(title))
#            _title = title[_count]
#            element = driver.find_element(by='id', value=_title['id'])
#            ActionChains(driver).move_to_element(element).perform()
#            
##            _count += 1
#            
##            if str(_title).find('광고') == -1:
##                rank += 1    
##            
##            if str(_title['id']).find('82390439558') != -1:
##                print('현재 순위 :', rank)
##                break
#            
#            sizeTitle = len(title)
#            
#            html = driver.page_source
#            soup = BeautifulSoup(html, 'html.parser')
#            title += list(soup.find_all(class_='product_list_item__2tuKA'))
#            
#            title = list(set(title))
#            print(len(title))
#            
##            if len(title) == sizeTitle:
##                break
#            
#            _count += 1
            
#        itemTime =  random.randrange(30, 60)
        itemTime =  random.randrange(_timeRule[4][0]+addTime,_timeRule[4][1]+addTime)
        
        print('상품 체류 시간', itemTime)
        scrollDownTime(driver, itemTime)
        
        
        driver.find_element_by_xpath('//*[@id="REVIEW"]/a').click()
#        itemTime =  random.randrange(30, 50)
        itemTime =  random.randrange(_timeRule[5][0]+addTime,_timeRule[5][1]+addTime)
        print('리뷰 체류 시간', itemTime)
        scrollDownTime(driver, itemTime)
        
        
        driver.find_element_by_xpath('//*[@id="QNA"]/a').click()
#        itemTime =  random.randrange(30, 50)
        itemTime =  random.randrange(_timeRule[6][0]+addTime,_timeRule[6][1]+addTime)
        print('QNA 체류 시간', itemTime)
        scrollDownTime(driver, itemTime)
        
        #seller info
        driver.get(driver.current_url.split('?')[0]+'/seller')
#        itemTime =  random.randrange(10, 20)
        itemTime =  random.randrange(_timeRule[7][0]+addTime,_timeRule[7][1]+addTime)
        print('판매자 정보 체류 시간', itemTime)
        scrollDownTime(driver, itemTime)
        
#       driver.find_element(by='id', value=image[searchTime].findNext('img').attrs['id']).click()
        
            
        #쿠키삭제
        driver.delete_all_cookies()
        print('쿠키를 삭제 합니다')
        
        #인터넷 기록 삭제
        #https://pythondocs.net/selenium/%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%ED%81%AC%EB%A1%A4%EB%9F%AC-%EA%B8%B0%EB%B3%B8-%EC%82%AC%EC%9A%A9%EB%B2%95/#%EC%BF%A0%ED%82%A4_%EA%B0%92_%EC%96%BB%EA%B8%B0
        #driver.get('chrome://settings/clearBrowserData')
        
        
        driver.close()
        print('총 시간 (초)', time.time() - s)
        
    except ValueError as E:
        print('restart', E)
        driver.close()
    
    except Exception as E:
        print(E)

    
    

    
#    
#    
#    
#
#driver.find_elements_by_link_text(_title.getText())[0].click()
#
#search_box = driver.find_element(by='a.href', value=title[46].attrs['href'])
#
#title[46].findNext('img').attrs['src']
#
#
#driver.find_elements_by_link_text(title[46].get_text().replace())
#
#
#
#title[46].string
#
#
#type(title[46])
#
#
#driver.find_element_by_xpath('//*[@id="mflick"]/div/div[1]/div/div/div[1]/div[1]/div[3]/div[1]/div/div[4]/button').click()
#                              //*[@id="mflick"]/div/div[1]/div/div/div[1]/div[1]/div[3]/div[2]/div/div[4]/button
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#ActionChains(driver).send_keys(Keys.CONTROL).send_keys(Keys.SHIFT).send_keys('M').perform()
#
#ActionChains(driver).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).send_keys(Keys.DOWN).perform()
#
#
#driver.send_keys(Keys.F12)
#driver.find_element_by_css_selector('body').send_keys(Keys.F12)
#
#def getIds(driver):
#    #인플루언서
#    count = 1
#    print('#인플루언서')
#    while(True):
#        try:
#            _in = driver.find_element_by_xpath('//*[@id="_section_influencer"]/div/div[2]/div[2]/ul/li['+str(count)+']/div[1]/div[1]/div[2]/div[1]/div[1]/a').get_attribute('href')
#            _inText = driver.find_element_by_xpath('//*[@id="_section_influencer"]/div/div[2]/div[2]/ul/li[' + str(count) + ']/div[1]/div[1]/div[2]/div[1]/div[1]/a').text
#            _in = _in.split('?')[0].replace('https://in.naver.com/','')
#            #print(_inText,':',_in)
#            print(_in)
#            count += 1
#        except:
#            break
#
#    count = 1
#    print('#블로그')
#    ids = []
#    while(True):
#        try:
#            a = driver.find_element_by_xpath('//*[@id="main_pack"]/section[6]/div/div[2]/panel-list/div[1]/ul/li['+str(count)+']/div[1]/div/div[1]/div[2]/span/span/span[2]/a').get_attribute('href')
#            aText = driver.find_element_by_xpath('//*[@id="main_pack"]/section[6]/div/div[2]/panel-list/div[1]/ul/li[' + str(
#                count) + ']/div[1]/div/div[1]/div[2]/span/span/span[2]/a').text
#            a = a.replace('https://blog.naver.com/','')
#            #print(aText,':',a)
#            if a.find('http') == -1:
#                print(a)
#                count += 1
#                ids.append(a)
#            else:
#                #print(a)
#                count += 1
#                #ids.append(a)
#        except:
#            break
#
#    idText = {}
#    for i in range(len(ids)): 
#        url = 'https://blog.naver.com/' + ids[i]
#        driver.get(url)
#        driver.switch_to.frame('mainFrame')
#        name = driver.find_element_by_xpath('//*[@id="nickNameArea"]').text
#        title = str(driver.title).replace(' : 네이버 블로그','').replace('.','')
#
#        text = '안녕하세요 '+title+' 블로그 운영중이신 '+name+'님 이번에 저희 페이스팩토리에서 출시한 미스트제품을 소개드리고자 연락드립니다. 관심있으시면 연락 부탁드릴게요'
#        print(text)
#        idText[ids[i]] = text
#
#    return idText
#
#getIds(driver)
#
#
#### 이건 블로그
#html = driver.page_source
#soup = BeautifulSoup(html, 'html.parser')
#title = soup.find_all(class_='sub_txt sub_name')
#
#### 이건 제목
#html = driver.page_source
#soup = BeautifulSoup(html, 'html.parser')
#title = soup.find_all(class_='api_txt_lines total_tit _cross_trigger')
#
#
#
#
#
#
#
#
#
#len(title)
#
#driver.execute_script("return goOtherCR(this, 'a=rvw*f.writer&amp;r=32&amp;i=90000003_0000000000000033D573FADD&amp;u='+urlencode(https://m.blog.naver.com/dewhm))")
#
#
#driver.find_elements_by_link_text("새로보기")
#
#
#driver.
#driver.execute_script("window.scrollTo(0, 200)")
#
#driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)
#
#
#
#
#<a href="https://blog.naver.com/ggggggenie/222624784079" class="api_txt_lines total_tit _cross_trigger" data-cr-gdid="90000003_0000000000000033D5789ECF" target="_blank" onclick="return goOtherCR(this, 'a=rvw*f.link&amp;r=69&amp;i=90000003_0000000000000033D5789ECF&amp;u='+urlencode(this.href))">아비브 어성초 진정 <mark>미스트</mark> 추천 ! 스킨팩으로 쓰기도 좋음</a>
#
## id가 something 인 element 를 찾음
#some_tag = driver.find_elements_by_link_text("샤넬 헤어미스트 넘버5 향 추천 샤넬화장품 가격은?")
#
#driver.find_element_by_partial_link_text('바디미스트 수시로 뿌려요').click()
#
#
#
#driver.find_elements_by_tag_name("https://blog.naver.com/ggggggenie/222624784079")
#
#find_element_by_id('something')
#
## somthing element 까지 스크롤
#action = ActionChains(driver)
#action.move_to_element(some_tag).perform()
#
#
#
#int('0000000000000033D04671D9',16)
#
#title[0]
#log
####
#len(title)
#->> 얼마나
#
#<tr class=""><td class="title"><div class="wrap_td"><div class="meta_data"><span class="num pcol3"></span></div><span class="ell2 pcol2"><a href="https://blog.naver.com/PostView.naver?blogId=vkeo3136&amp;logNo=222631700254&amp;categoryNo=46&amp;parentCategoryNo=45&amp;viewDate=&amp;currentPage=1&amp;postListTopCurrentPage=1&amp;from=postList" class="pcol2 _setTop _setTopListUrl">미스트 추천 제일 효과본거</a></span><i class="cline"></i></div></td><td class="date"><div class="wrap_td"><span class="date pcol2">2022. 1. 26.</span><i class="cline"></i></div></td></tr>
#33D5E2271E
#222631700254
#
#
#
#
#
##인풀루언서
##포스트 분리
#
#
##쪽지쓰기
#url = 'https://note.naver.com/#%7B%22sHistoryFunction%22%3A%22write%22%2C%22sWriteType%22%3A%22new%22%2C%22oParameter%22%3A%7B%22targetUserId%22%3A%22%22%2C%22toMe%22%3A%220%22%7D%2C%22sUrl%22%3A%22%2Fjson%2Fwrite%2F%22%7D'
#driver.get(url)
#
#send_count = 0
#for i in range(2):
#    for _id,v in idText.items():
#        _id = 'iriyakana'
#
#        time.sleep(3)
#        # driver.find_element_by_xpath('// *[ @ id = "who"]').send_keys(_id)
#        driver.find_element_by_xpath('// *[ @ id = "who"]').click()
#        pyperclip.copy(_id)
#        driver.find_element_by_xpath('// *[ @ id = "who"]').send_keys(Keys.CONTROL, 'v')
#        time.sleep(3)
#
#        # driver.find_element_by_xpath('// *[ @ id = "writeNote"]').send_keys(v)
#        driver.find_element_by_xpath('// *[ @ id = "writeNote"]').click()
#        pyperclip.copy(v)
#        driver.find_element_by_xpath('// *[ @ id = "writeNote"]').send_keys(Keys.CONTROL, 'v')
#        time.sleep(2)
#
#        # driver.find_element_by_xpath('// *[ @ id = "cont_fix_area"] / div[6] / div[1] / a[1]').click()
#        driver.find_element_by_xpath('// *[ @ id = "cont_fix_area"] / div[6] / div[1] / a[1]').click()
#        time.sleep(1)
#
#
#        result = driver.switch_to.alert
#        result.accept()
#        time.sleep(2)
#
#        send_count += 1
#        print(send_count)
#
#
#
#    # driver.switch_to('mainFrame')
#    # iframes = driver.find_elements_by_css_selector('iframe')
#    # for iframe in iframes:
#    #     print(iframe.get_attribute('name'))
#
#
#
#
#
#
#//*[@id="blogTitleText"]
#
#/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/strong
#getIds(driver)
#
#bs = BeautifulSoup(driver.page_source, 'html.parser')
#bb = str(bs).split('\n')
#len(bb)
#
#
#len(result)
#result = bs.find_all('a')
#c = 0
#for k in result:
#    if str(k).find('https://blog.naver.com/') != -1:
#
#        temp = str(k).split('https://blog.naver.com/')[1]
#        end = temp.index('/')
#        print(temp[:end])
#        c+= 1
#
#
#
#
#
#
#
#
#
#
#select = result.select('td')
#select = [s.text for s in select]
#
#
#datalist = []
#for num in range(1,2):
#    url = 'https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW&page='+str(num)
#    driver.get(url)
#
#    for i in range(1,11):
#        a = driver.find_element_by_xpath('/html/body/div/table/tbody/tr['+str(i)+']/td[1]').text
#        a = DateToString(StringToDateV2(a, '%Y.%m.%d'))
#        b = driver.find_element_by_xpath('/html/body/div/table/tbody/tr['+str(i)+']/td[2]').text
#        # print(a,b)
#
#        dic = {}
#        dic['date'] = a
#        dic['price'] = float(b.replace(',',''))
#
#        key = a
#        datalist.append([key, dic])
#
#controller.insertBulk(datalist, 'usd')
#
#
#
#
#query = {"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[{"date":"desc"}],"aggs":{}}
#esUrl = 'http://search-profiling-krdnrvolweiwb24ylb53dbarje.ap-northeast-2.es.amazonaws.com/'
#esIndex = 'usd'
#usdjson = controller.getdetails_qurey(esIndex, query, esUrl)
#
#
#for pj in usdjson:
#    print(pj['_source']['date'],pj['_source']['price'])
#
#print(len(json['_source']))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#date
#/html/body/div/table/tbody/tr[7]/td[1]
#
#data
#/html/body/div/table/tbody/tr[1]/td[2]
#
#
#data = {}
#dataLen = {}
#
#nowdate = STARTDATE
#while(nowdate !=  ENDDATE):
#    nowdate = IncreaseDate(nowdate, 'day', 1)
#    print(nowdate)
#
#    #text = driver.find_element_by_xpath('//*[@id="listContents"]/div[2]/p').text
#    
#    driver.find_element_by_xpath('//*[@id="gijunYMD"]').clear()
#    time.sleep(0.3)
#    driver.find_element_by_xpath('//*[@id="gijunYMD"]').send_keys(nowdate)
#    time.sleep(0.3)
#    driver.find_element_by_xpath('//*[@id="frmPdf"]/p[1]/button').click()
#    time.sleep(0.5)
#    
#    try:
#        driver.find_element_by_xpath('//*[@id="btnPdfMore"]').click()
#        time.sleep(1)
#    except:
#        pass
#    
#    bs = BeautifulSoup(driver.page_source, 'html.parser')
#    
#    result = bs.find('tbody', id ='pdfResultList')
#    select = result.select('td')
#    select = [s.text for s in select]
#    
#    if len(select) > 1:
#        
#        # NO 종목명	종목코드	수량	비중(%)	평가금액(원)	현재가(원)	등락(원)
#        arr_ = [[],[],[],[],[],[],[],[]]
#        
#        cnt = 0
#        while(True):
#            try:
#                # arr_[0].append(select[cnt])
#                arr_[1].append(select[cnt+1])
#                arr_[2].append(select[cnt+2])
#                arr_[3].append(select[cnt+3])
#                arr_[4].append(select[cnt+4])
#                arr_[5].append(select[cnt+5])
#                arr_[6].append(select[cnt+6])
#                arr_[7].append(select[cnt+7])
#
#                cnt += 8
#            except:
#                break
#        
#        insertData = []
#        dic = {}
#        
#        dic['date'] = nowdate.replace('-','')
#        dic['name'] = arr_[1]
#        dic['code'] = arr_[2]
#        dic['count'] = arr_[3]
#        dic['per'] = arr_[4]
#        dic['allprice'] = arr_[5]
#        dic['price'] = arr_[6]
#        # dic['sprice'] = arr_[7]
#        
#
#        insertData.append([dic['date'], dic])
#            
#        controller.insertBulk(insertData, 'kodex150re')
#
#
#        # arr_name = []
#        # cnt = 1
#        # while(True):
#        #     try:
#        #         arr_name.append(select[cnt])
#        #         cnt += 8
#        #     except:
#        #         break
#        
#        # data[nowdate] = arr_name
#        # dataLen[nowdate] = len(arr_name)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#qurey = {"query":{"bool":{"must":[{"match":{"code":"233740"}}],"must_not":[],"should":[]}},"from":0,"size":400,"sort":[{ "date.keyword" : "desc" }],"aggs":{}}
#
#count = 0
#r_arr = controller.getdetails_qurey('day_db', qurey)
#value = {}
#
#for _arr in r_arr:
#    _arr = _arr['_source']
#    
#    # code.append(_arr['code']
#    close = (_arr['close'])
#    start = (_arr['open'])
#    
#    value[_arr['date']] = round((close/start - 1) * 100, 2)
#    
#
## dic['date'] = date
#
#
#before = []
#for k,v in data.items():
#    if before != []:
#        s1 = set(before)
#        s2 = set(v)
#        
#        del1 = s1 - s2
#        add1 = s2 - s1
#        
#        print(k,'add',add1,'del',del1, value.get(k.replace('-','')))
#        
#    before = v
#
#
#
#
#s1 = set(data['2021-06-29'])
#s2 = set(data['2020-06-30'])
#s1 - s2
#
#    
## #selenium 으로 속도가 너무 느림
## arr_name = []
## cnt = 0
## while(True):
#    
##     try:
##         cnt += 1
##         arr_name.append(driver.find_element_by_xpath('//*[@id="pdfResultList"]/tr['+str(cnt)+']/td[2]').text)
##     except:
##         break림
#
#
#
#
#
#//*[@id="pdfResultList"]/tr[1]
#//*[@id="pdfResultList"]/tr[2]
#
#html = driver.page_source
#soup = BeautifulSoup(html, 'html.parser')
#
#javascript_list = []
#for link in soup.find_all('a'):
#    _url = link.get('href')
#    try:
#        if _url.find('javascript:downFile(') != -1:
#            javascript_list.append(_url)
#    except:
#        pass
#
#cnt = 0;
#for link in javascript_list:
#    
#    driver.execute_script(link)
#    time.sleep(0.5)
#    cnt+=1
#    print(cnt,'/',len(javascript_list))
#
#
## key_list = []
## for link in soup.find_all('a'):
##     _url = link.get('href')
##     if _url.find('/dsaf001/main.do?rcpNo=') != -1:
##         key_list.append(_url.replace('/dsaf001/main.do?rcpNo=',''))




