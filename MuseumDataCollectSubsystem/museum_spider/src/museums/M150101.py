# -*- coding: utf-8 -*-
"""
青岛市博物馆爬虫文件
@author: zy

http://www.qingdaomuseum.com/
150101

"""

import requests
import os
from bs4 import BeautifulSoup
import re
import json
from os import write

ID = "150101"

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
#博物馆信息
def getMuseumData():
    datadict = {}  # 用来存储爬取的网页信息
    datadict["M_ID"] = ID
    datadict["M_CName"] = "青岛市博物馆"
    # datadict["M_EName"] = "Sanxingdui Museum"
    datadict["M_Batch"] = 1
    datadict["M_Address"] = "山东省青岛市崂山区梅岭东路51号"
    datadict["M_Web"] = "http://www.qingdaomuseum.com/"

    # 主页内容
    baseurl = "http://www.qingdaomuseum.com/"  # 要爬取的网页链接
    datadict["M_Web"] = baseurl
    html = askURL(baseurl)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")

    # logo
    datadict["M_Logo"] = "http://www.qingdaomuseum.com/uploads/images/logo.png"
    # print(datadict["M_Logo"])

    # 参观指南
    url = "http://www.qingdaomuseum.com/service/free"
    html = askURL(url)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    # print(html)
    s = ""
    for item in soup.find_all("div", class_="cfzn01"):
        # print(item.text)
        for il in item.find_all("p"):
            # print(il.text)
            s = s + il.text + '\n'
    # print(s)
    datadict["M_TicketInformation"] = s
    datadict["M_OpeningTime"] = "9:00-NULL-16:30-17:00"  #开馆时间-停止售票时间（本馆免费NULL）-截止入馆时间-闭馆时间
    datadict["M_OpeningInformation"] = "5月至10月 Am9：00~Pm17：00（Pm16：30停止入场）","11月至次年4月 Am9：00~16：30（Pm16：00停止入场）","每周一闭馆（法定节假日除外）"

    jsondata = json.dumps(datadict, ensure_ascii=False)
    with open("museum_spider/museums/M" + ID + ".json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    # exit()
    pass
#藏品爬取
def getCollectionsData():
    # baseurl = "http://www.qingdaomuseum.com/"
    count = 0
    url = "http://www.qingdaomuseum.com/collection"
    html = askURL(url)
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    
    for item in soup.find_all("div", class_="zgzb_ss"):
        count = count + 1

        C_name = ""
        for title in item.find_all("h3"):
            # print(title.text) 
            C_name = title.text 
        # print(item)
        C_Intro = ""
        for text in item.find_all("p"):
            C_Intro = C_Intro + text.text + '\n'
            # print(s)
        C_pic = []
        for src in item.find_all("img"):
            C_pic.append(src["src"])
        # C_pic = list(set(C_pic))
        # print(srcs)
        # exit()

        collectiondict = {}

        collectiondict["C_Name"] = C_name

        collectiondict["C_Introduction"] = C_Intro
        
        collectiondict["C_ID"] = ID + "-" + "1" + "-" +str(count)

        collectiondict["CRM_In"] = ID
        
        collectiondict["C_Pictures"] = C_pic[0]

        soup = BeautifulSoup(html, "html.parser")

        jsondata = json.dumps(collectiondict, ensure_ascii=False)
        with open("./museum_spider/collections/C" + collectiondict["C_ID"] + ".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)
    pass
#爬取活动
def getActivitiesData():
    # baseurl = "http://www.qingdaomuseum.com/"
    A_id = [502,490,489,487,457,463]
    
    # print(html)
    # exit()
    
    for i in A_id:
        url = "http://www.qingdaomuseum.com/education/detail/"+str(i)
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all("div", class_="hd_n"):
            # print(item.text)
            # exit()
            # <a href="http://www.qingdaomuseum.com/education/detail/502">style=" display:block; width:100%;"></a>
            A_name =""
            for title in item.find_all("b"):
                A_name = title.text 
                # print(title.text)
                # exit() 
            A_Infor = ""
            for text in item.find_all("div",class_="hd_nr"):
                A_Infor =  text.text 
                # print(A_Infor)
                # exit()
            A_pic = []
            for src in item.find_all("img"):
                A_pic.append(src["src"])
                # print(A_pic)
            #     exit()
            # A_pic = list(set(A_pic))
            
            adict = {}

            adict["A_ID"] = ID + "-" + str(i)

            adict["ARM_In"] = ID
    
            adict["A_Name"] = A_name

            adict["A_Information"] = A_Infor

            adict["A_Picture"] = A_pic

            jsondata = json.dumps(adict, ensure_ascii=False)
            with open("museum_spider/activities/A" + adict["A_ID"] + ".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)

        pass

if __name__ == "__main__":
    # getMuseumData()
    # getCollectionsData()
    getActivitiesData()

# print(soup.text)