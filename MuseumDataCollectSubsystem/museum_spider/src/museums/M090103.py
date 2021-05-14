# -*- coding: utf-8 -*-
"""
python文件说明
中国共产党第一次全国代表大会会址纪念馆爬虫文件
@Time    :   2021/05/09 09:39:59
@Author  :   <zy> 
@Version :   Annconda3

代码更新说明
2020.05.10
代码完成


"""

import requests
import os 
from bs4 import BeautifulSoup
import re
import json
import time

ID = "090103"

def debugPrint(message): 
    if __name__ == "__main__":
        print(message)

# 得到指定一个URL的网页内容
def askURL(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
    }
    html = ""
    try:
        res = requests.get(url, headers=head)
        res.raise_for_status()
        if res.apparent_encoding == 'gb2312':
            res.encoding = 'gbk'
        else:
            res.encoding = res.apparent_encoding
        html = res.text

    except requests.RequestException as e:
        print(e)

    return html

# 博物馆信息
def getMuseumData():
    datadict = {}  # 存储博物馆信息

    datadict["M_ID"] = ID
    datadict["M_CName"] = "中国共产党第一次全国代表大会会址纪念馆"
    datadict["M_EName"] = "Site of the first National Congress of the Communist Party of China"
    datadict["M_Web"] = "http://www.zgyd1921.com/zgyd/node3/index.html"  
    datadict["M_Address"] = "上海市黄浦区黄陂南路374号"
    datadict["M_Batch"] = 1  
    datadict ["M_Ticket"] = "免费"
    datadict["M_Triffic"] = "地铁一号线（黄陂南路站）、地铁十号线（新天地站）、公交24路、109路和926路等线"

    # M_pic
    num = ["0495792","0088824","3074821","1377545","3423076"]
    baseurl = "http://www.zgyd1921.com/images/thumbnailimg/month_1709/20170928035"
    for i in num:
        Pic = baseurl + str(i) + ".jpg"
        datadict["M_Pictures"] = Pic 

    # 开放信息
    url = "http://www.zgyd1921.com/zgyd/node3/n44/u1ai694.html"
    html = askURL(url)  
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="grey14 lh30"):
        datadict["M_OpeningTime"] = item.text[132:164]
        datadict["M_OpeningInformation"] = item.text[91:364]  
        datadict["M_Booking"] = item.text[799:1000]  
        datadict["M_TicketInformation"] =  item.text[172:237]  

    # 博物馆简介
    url = "http://www.zgyd1921.com/zgyd/node3/n5/n6/ulai19.html"
    html = askURL(url)  
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div",class_="d940"):
        datadict["M_Introduction"] = item.text

    # 把博物馆信息写入文件夹
    soup = BeautifulSoup(html, "html.parser")
    jsondata = json.dumps(datadict, ensure_ascii=False)
    with open("museum_spider/museums/M" + ID + ".json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    pass

# 藏品信息
def getCollectionsData():

    # 藏品图片
    C_pictures = []
    M_url = "http://www.zgyd1921.com"
    baseurl = "http://www.zgyd1921.com/zgyd/node3/n17/n18/index.html" # 藏品首页图片网址
    html = askURL(baseurl)  
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("ul",class_="piclist2"):
        for src in soup.find_all("img"):
            C_pictures.append(M_url + src["src"])

    baseurl = "http://www.zgyd1921.com/zgyd/node3/n17/n18/index"
    for i in range(1,5,1):
        url = baseurl + str(i) + ".html"
        html = askURL(url) 
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("ul",class_="piclist2"):
            for src in soup.find_all("img"):
                C_pictures.append(M_url + src["src"])

    # 藏品名称和介绍
    count = 0
    baseurl = "http://www.zgyd1921.com/zgyd/node3/n17/n18/ulai"
    for i in range(152,185,1):
        url = baseurl + str(i) + ".html"
        html = askURL(url)  
        soup = BeautifulSoup(html, "html.parser")

        collectiondict = {}  # 存储每个藏品信息
        collectiondict["C_ID"] = ID + "-" + str(i)
        collectiondict["CRM_In"] = ID
        collectiondict["C_picturea"] = C_pictures[count]
        count = count+1
        for item in soup.find_all("div",class_="d940"):
            for name in soup.find_all("div",class_="grey24 lh30 fc"):
                collectiondict["C_Name"] = name.text
            collectiondict["C_Information"] = item.text[36:500]
    
        soup = BeautifulSoup(html, "html.parser")

        jsondata = json.dumps(collectiondict, ensure_ascii=False)
        with open("./museum_spider/collections/C" + collectiondict["C_ID"] + ".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)
        pass

# 活动信息
def getActivitiesData():

    # 活动名称和介绍
    baseurl = "http://www.zgyd1921.com/zgyd/node3/n11/n15/ulai"
    for i in range(74,80,1):
        url = baseurl + str(i) + ".html"
        html = askURL(url)      
        soup = BeautifulSoup(html, "html.parser")

        Adict = {}
        Adict["A_ID"] = ID + "-" + str(i)
        Adict["ARM_In"] = ID 

        for item in soup.find_all("div",class_="d940"):
            for tittle in soup.find_all("div",class_="grey24 lh30 fc"):
                Adict["A_Name"] = tittle.text
            Adict["A_Introduction"] = item.text[40:500]

        jsondata = json.dumps(Adict, ensure_ascii=False)
        with open("museum_spider/activities/A" + Adict["A_ID"] + ".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)

        pass

if __name__ == "__main__":
    # getMuseumData()
    getCollectionsData()
    # getActivitiesData()
