# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 02:01:34 2022

@author: SAKURA-WR
"""

import requests

import os
import sys
sys.path.append('C:\\git')

import datetime
#from yhlibe import controller as controller

import csv
import json
esType = 'data'

bulkSize = 1000

esUrl = 'http://3.37.243.132:8806/dksdbgus/'


def insertBulk(datalist, esIndex, esUrl = esUrl):

    make = ''
    with requests.Session() as session:
        for i in range(len(datalist)):
            
            _id = str(datalist[i][0])
            make += "{ \"index\" : { \"_index\" : \""+esIndex+"\", \"_type\" : \""+esType+"\", \"_id\" : \""+_id+"\" } }\r\n"+str(json.dumps(datalist[i][1]))+"\r\n"
            if (i != 0 and i%bulkSize == 0 ) or i == len(datalist)-1:
                print('input',i+1,'개')
                
                url = esUrl +'_bulk'
                headers = {'content-type': "application/x-ndjson"}
                response = session.request("POST", url, data=make.encode(encoding='utf-8'), headers=headers, verify=False, proxies={})
                # print(response,'200이면 성공')
                
                if str(response).find('200') == -1:
                    print('error', response.text)
                #print(response.text)
                make = ''




def saveCsv(name, arr):
    f = open(name, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f, delimiter='\t')
    for a in arr:
        wr.writerow(a)
    f.close() 

def readCsv(path):
    f = open(path, 'r', encoding='utf-8')
    cin = csv.reader(f, delimiter='\t')
    temp = [row for row in cin]
    f.close()
    return temp

def readCsv2(path):
    f = open(path, 'r', encoding='utf-8')
    cin = csv.reader(f, delimiter=',')
    temp = [row for row in cin]
    f.close()
    return temp

def DateToString2(value):
    if value == 'now':
        value = datetime.datetime.now()
  
    # String = str(year)+str(month)+str(day)    
    String = value.strftime('%Y-%m-%dT%H:%M:%S')
    String2 = value.strftime('%Y%m%d%H%M%S')
    return String, String2 

a = 0

# esUrl = 'http://3.37.243.132:59920/'




findName = {}
p = os.popen("cd ../ && dir /b/s")
listFile = p.readlines()

listUseFiles = []

for file in listFile:
    if file.find('1_쪽지 발송 양식_') != -1:
        listUseFiles.append((file).replace('\n',''))

print(len(listUseFiles))



for i, FileName in enumerate(listUseFiles):
    idx = 0
    _type = FileName.split('[')[1].split(']')[0]
    
    datalist = []
    memo = readCsv(FileName)
    
    text = ''
    for _me in memo:
        try:
            _me = _me[0]
            
            if _me == '<E>':
                _id = ((i+1) * 100) + idx + 1
                dic = {}
                dic['id'] = _id
                dic['value'] = text
                dic['type'] = _type
                datalist.append([_id, dic])
                text = ''
                idx += 1
            else:
                text += _me + '<S>'
        except:
            text += '<S>'
        
    insertBulk(datalist, 'cubist_naver_message', esUrl)    




datalist = []
memo = readCsv('./2_명언or브랜드 한마디.txt')
for idx, _me in enumerate(memo):
    text = _me[0] + '<S>'
    _id = idx+1
    dic = {}
    dic['id'] = _id
    dic['value'] = text
    datalist.append([_id, dic])

    insertBulk(datalist, 'cubist_naver_memo', esUrl)    
    



datalist = []
memo = readCsv2('./3_네이버아이디.txt')
for idx, _me in enumerate(memo):
    _id = idx+1
    dic = {}
    dic['id'] = _id
    dic['value'] = _me[0]
    dic['state'] = _me[1]
    datalist.append([_id, dic])
        
    
    insertBulk(datalist, 'cubist_naver_sid', esUrl)    



# keyword = [['ceooyw0120','네이버12!'],
# ['belnoi37110','53fa6fx3'],
# ['hwitchg3768','6364234p004u'],
# ['eccaid3043','8f07hb8025j'],
# ['tcoali46426','22h58m3wv5k'],
# ['vindi71827','52ix2d75734']]

# datalist = []
# for idx, _me in enumerate(keyword):
#     _id = idx+1
#     dic = {}
#     dic['id'] = _id
#     dic['value'] = _me[0]
#     dic['state'] = _me[1]
#     datalist.append([_id, dic])
    
# controller.insertBulk(datalist, 'cubist_naver_keyword6', esUrl)


# keyword = [['필링기','1021'],
#  ['괄사','1010'],
#  ['뷰티석션','785'],
#  ['요가 마스크','910'],
#  ['MTS 롤러','1020'],
#  ['파라핀','1012']
# ]

datalist = []
memo = readCsv('./4_검색더보기.txt')
for idx, _me in enumerate(memo):
    _id = idx+1
    dic = {}
    dic['id'] = _id
    dic['value'] = _me[0]
    datalist.append([_id, dic])
        
    
    insertBulk(datalist, 'cubist_naver_search_add', esUrl)    



datalist = []
memo = readCsv2('./5_키워드.txt')
for idx, _me in enumerate(memo):
    _id = idx+1
    dic = {}
    dic['id'] = _id
    dic['value'] = _me[0]
    dic['state'] = _me[1]
    dic['keyword'] = _me[2]
    dic['type'] = _me[3]
    
    datalist.append([_id, dic])
    
    insertBulk(datalist, 'cubist_naver_keyword', esUrl)




