#!/usr/bin/env python
# coding: utf-8

# In[11]:


import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey="%2BgSJiYQdX8owt%2FK7o6rZZoA91LR%2FJpfqT9Ihv8wX78Ud2tpcmZ5Ea2pMATbF3KyvXQASZiTIkdC577OPA9rO3g%3D%3D"

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] URL Request Success"% datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] URL Request Error : %s"% (datetime.datetime.now(),url))
        return None

def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameters = "?_type=json&serviceKey=" + ServiceKey   #인증키
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + nat_cd
    parameters += "&ED_CD=" + ed_cd
    
    url = service_url + parameters
    
    responseDecode = getRequestUrl(url)
    
    if responseDecode == None:
        return None
    else:
        return json.loads(responseDecode)

def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    dataEND = "{0}{1:0>2}".format(str(nEndYear),str(12))
    isDataEnd = 0 #데이터 끝 확인용 flag. 저장된 값이 1이면 반복 종료(braek)
    
    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13):
            if(isDataEnd == 1): break
            yyyymm = "{0}{1:0>2}".format(str(year),str(month))
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)
            
            if jsonData['response']['header']['resultMsg'] == 'OK':
                if jsonData['response']['body']['items'] == '':
                    isDataEnd = 1 #데이터 끝 flag 설정
                    dataEND = "{0}{1:0>2}".format(str(year),str(month-1))
                    print("데이터 없음\n제공되는 통계데이터는 %s년 %s월까지 입니다." 
                          %(str(year),str(month-1)))
                    break
                print(json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))
                natName = jsonData['response']['body']['items']['item']['natKorNm']
                natName = natName.replace(' ','')
                num = jsonData['response']['body']['items']['item']['num']
                ed = jsonData['response']['body']['items']['item']['ed']
                print('[ %s_%s : %s]'%(natName, yyyymm, num))
                print('--------------------------------------')
                
                jsonResult.append({'nat_name':natName, 'nat_cd':nat_cd, 
                                   'yyyymm':yyyymm, 'visit_cnt:':num})
                result.append([natName, nat_cd, yyyymm, num])
                
    return(jsonResult, result, natName, ed, dataEND)
                
def main():
    print("<< 국내 입국한 외국인의 통계 데이터를 수집합니다. >>")
    nat_cd = input('국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275) : ')
    nStartYear =int(input('데이터를 몇 년부터 수집할까요? : '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? : '))
    ed_cd = "E"     #E : 방한외래관광객, D : 해외 출국
    
    jsonResult, result, natName, ed, dataEND = getTourismStatsService(
        nat_cd, ed_cd, nStartYear, nEndYear)
    if natName == '':
        print("데이터가 전달되지 않았습니다. 공공데이터 포털의 서비스 상태를 확인하세요.")
    else:
        with open('%s_%s_%d_%s.json' %(natName, ed, nStartYear, dataEND), 'w', encoding='utf-8') as outfile:
            jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(jsonFile)
        
        columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
        result_df = pd.DataFrame(result, columns= columns)
        result_df.to_csv('%s_%s_%d_%s.csv' %(natName, ed, nStartYear, dataEND),
                        index=False, encoding='cp949')

if __name__ == '__main__':
    main()
        


# In[3]:


import requests

ServiceKey="+gSJiYQdX8owt/K7o6rZZoA91LR/JpfqT9Ihv8wX78Ud2tpcmZ5Ea2pMATbF3KyvXQASZiTIkdC577OPA9rO3g=="


url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
params ={'serviceKey' : ServiceKey, 'YM' : '201201', 'NAT_CD' : '112', 'ED_CD' : 'E' }

response = requests.get(url, params=params)
print(response.content)

