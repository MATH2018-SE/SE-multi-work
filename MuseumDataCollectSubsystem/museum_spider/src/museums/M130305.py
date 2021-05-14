# -*- coding: utf-8 -*-
"""
中央苏区（闽西）历史博物馆博物馆爬虫文件
@author: lxx

http://hsmxbwg.com/
130305

代码更新：

2020.05.10
代码完成
2020.05.10
代码创建

"""

import requests
import os 
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
import time

ID = "130305"
def debugPrint(message): 
    if __name__ == "__main__":
        print(message)

def getText(item, newline=False):
    item = re.sub(r"<br/>","",item, flags=re.I)
    item = re.sub(r"<br />","",item,flags=re.I)
    item = re.sub(r"<br>","",item,flags=re.I)
    item = re.sub(r"\r","",item)
    item = re.sub(r"\t","",item)
    item = re.sub(r"\xa0","",item)
    # item = re.sub(r"  ","",item)
    item = re.sub(r"\n\n","",item)
    item = re.sub(r"\u3000","",item)
    item = re.sub(r"&emsp;","",item)
    item = re.sub(r"&nbsp;","",item)
    il = re.findall(r'(?<=).*?(?=)', item)
    s = ""
    flag = 0
    flagp = 0
    for i in il:
        if i == '/' and flag != 0:
            flagp = 1
        else:
            flagp = 0
        if i == '<':
            flag = flag + 1
        elif i == '>':
            flag = flag - 1
        else:
            if flag == 0:
                s = s+i
            if flagp == 1:
                if newline:
                    s = s + '\n'
                pass 
    # print(s)    
    return s

def getMuseumData():
    datadict = {}  #用来存储爬取的网页信息
    datadict["M_ID"] = "130305"
    datadict["M_CName"] = "中央苏区（闽西）历史博物馆"
    datadict["M_EName"] = "Central Soviet Area (Minxi) History"
    datadict["M_Batch"] = 3
    datadict["M_Address"] = "福建省龙岩市北环西路51号"

    #官网主页相关内容
    baseurl = "http://hsmxbwg.com/"  #要爬取的网页链接
    datadict["M_Web"] = baseurl 
    html = askURL(baseurl)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # logo 
    src = soup.find("div",class_="header").find("img")["src"]
    src = str(src)
    # print(src)
    datadict["M_Logo"] = baseurl[0:-1] + '/static/sanwei/images/logo.png'

    # 博物馆开放时间及门票
    i = 0
    time = []
    item = soup.find("div", class_="footer backgroundImageStyle").find("div",class_="middle").find("div",class_="right")
    for pi in item.find_all("p"):    
        pi = getText(pi.text) 
        # print(item)
    time.append("开放时间：")
    time.append(pi)
    # print(time)
    # print(booking)
    datadict["M_Openingtime"] = pi
    datadict["M_OpeningInformation"] = time
    datadict["M_Ticket"] = "免费开放"
    # 门票信息 
    # exit()
    url = "http://hsmxbwg.com/60/"
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    item = soup.find("tbody")
    j = 0
    text =[]
    for pi in item.find_all("tr"):
        j += 1
        pi = getText(pi.text)
        text.append(pi)
        if j > 4:
            break
    # print(text)
    datadict["M_Booking"] = pi[0]
    datadict["M_Ticketinformation"] = text
    # exit()
    # 博物馆图片(list)
    url = "http://hsmxbwg.com/25/"
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    src = []
    for pi in soup.find("div", class_="swiper-wrapper").find_all("div",class_="swiper-slide"):
        srcs = pi.find("img")["src"]
        src.append(item)
    # print(src)
    p = []
    for pi in src:
        pi = baseurl[0:-1] + str(pi)
        p.append(pi)
    # print(p)
    datadict["M_Pictures"] = p
    # print(p)
    # 博物馆介绍
    src.clear()
    j =0
    for item in soup.find("div", class_="mxylcl_con").find_all("p"):
        # print("===========")
        item = getText(item.text)
        src.append(item) 
        j += 1
        if j > 3:
            break
    # print(src)
    # p = []
    # for pi in src:
    #     if len(pi) >= 10:
    #         p.append(pi)
        # srcs = re.findall('<img src="(.*?)"/>', str(src))
    datadict["M_Introduction"] = src 

    jsondata = json.dumps(datadict, ensure_ascii=False,indent = 4)
    with open("./museums/M130305.json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    return datadict

def getCollectionsData():
    baseurl = "http://hsmxbwg.com/"
    index = "http://hsmxbwg.com/{}/"

    for pi in {'43','44','45','46'}:
        index = index.format(pi)
        html = askURL(index)

        soup = BeautifulSoup(html,"html.parser")
    # print(soup)
        href = []
        src = []
        title = []
        for item in soup.find("div", class_="list").find_all("div",class_="item"):
            for srcs in item.find("a").find_all("img"):
                srcs = srcs["src"]
            src.append(baseurl[0:-1] + srcs)

            href0 = str(item.find("a")) 
            # item = str(item)
            href0 = re.findall(r'<a.*?href="(.*?)"', href0)
            href0 = str(href0[0])
            href.append(baseurl[0:-1] + href0)

            title0 = item.find("a").text
            title0 = re.sub(r"\n","",title0)
            title.append(title0)
        # print(href)
        n = len(href) 
        # exit()
        for i in range(n):
            url = href[i]
            html = askURL(url)
            soup = BeautifulSoup(html,"html.parser")
            # print(type(href))
            collectiondict = {}
            collectiondict["CRM_In"] = ID
            Id = re.findall(r'http.*/(.*?).shtml', url)
            collectiondict["C_ID"] = ID + '-' + str(Id[0])

            item = soup.find("div", class_="content")
            item = getText(item.text)
            txt = []
            txt.append("藏品描述：")
            txt0 = item.split()
            # print(txt)
            for pi in txt0:
                if len(pi) > 10:
                    
                    txt.append(pi)

            collectiondict["C_Name"] = title[i]
            collectiondict["C_Pictures"] = src[i]
            collectiondict["C_Introduction"] = txt

            jsondata = json.dumps(collectiondict, ensure_ascii=False,indent = 4 )
            with open("./collections/C"+collectiondict["C_ID"]+".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
            # exit()
        pass
    pass

def getActivitiesData():
# 该博物馆详情页面暂时打不开，仅展示网络链接
    baseurl = "http://hsmxbwg.com/"
    index = "http://hsmxbwg.com/34/"
    html = askURL(index)
    soup = BeautifulSoup(html, "html.parser")
        # print("hhh")
    href = []
    src = []
    title = []
    data = []
    for item in soup.find("div", class_="list").find_all("div",class_="item"):
        srcs = item.find("div",class_="info").find("img")["src"]
        src.append(baseurl[0:-1] + srcs)

        href0 = str(item.find("a")) 
        # item = str(item)
        href0 = re.findall(r'<a.*?href="(.*?)"', href0)
        href0 = str(href0[0])
        href.append(href0)

        title0 = item.find("div",class_="title txtHide").find("a").text
        title0 = re.sub(r"\n","",title0)
        title.append(title0)
        
        data0 = item.find("div",class_="time").text
        data0 = data0.split()
        data0 = '-'.join((data0[1],data0[0]))
        data.append(data0)
    # print(title)
    # print(href)
    n = len(title)
    for i in range(n):
        activityDict = {}
        activityDict["ARM_In"] = ID
        activityDict["A_ID"] = ID + "-" + str(i+1)
        activityDict["A_Name"] = title[i]
        activityDict["A_Date"] = data[i]
        activityDict["A_Pictures"] = src[i]
        activityDict["A_Information"] = baseurl[0:-1]+href[i]

        jsondata = json.dumps(activityDict, ensure_ascii=False,indent = 4)
        with open("./activities/A"+activityDict["A_ID"]+".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)
        # exit()
    pass


def askURL(url):
    # head = headers[0]
    head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 80.0.3987.122 Safari / 537.36'
    }
    html = ""
    try:
        res = requests.get(url, headers=head)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        html = res.text
    
    except requests.RequestException as e:
        print(e)

    return html

def askPic(url):
    head = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
    }
    try:
        res = requests.get(url, headers=head)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
    except requests.RequestException as e:
        print(e)
    return res

if __name__ == "__main__":
    getMuseumData()
    getCollectionsData()
    getActivitiesData()