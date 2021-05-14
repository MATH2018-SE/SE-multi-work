# -*- coding: utf-8 -*-
"""
中国闽台缘博物馆博物馆爬虫文件
@author: lxx

http://www.mtybwg.org.cn/index.aspx
130104

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

ID = "130104"
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
    item = re.sub(r"  ","",item)
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
    datadict["M_ID"] = "130104"
    datadict["M_CName"] = "中国闽台缘博物馆"
    datadict["M_EName"] = "China Museum for Fujian Taiwan kinship"
    datadict["M_Batch"] = 1
    datadict["M_Address"] = "福建泉州北清东路212号"

    #官网主页相关内容
    baseurl = "http://www.mtybwg.org.cn/"  #要爬取的网页链接
    datadict["M_Web"] = baseurl 
    html = askURL(baseurl)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    
    datadict["M_Logo"] = "http://www.mtybwg.org.cn/templates/mty/images/logo.jpg"

    # 博物馆开放时间及门票
    i = 0
    time = []
    item = soup.find("div", class_="top").find("ul",class_="notice").find("p")
    item = item.find("span").text
    # print(item)
    # time = item.split()
    # print(time)
    time0 = re.findall(r'开放时间：(.*）)', item)
    # print(time0)
    # exit()
    datadict["M_Openingtime"] = time0[0]
    datadict["M_Ticket"] = "免费开放"
    # 门票信息 
    url = "http://www.mtybwg.org.cn/about/detail/249.aspx"
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    item = soup.find("ul",class_="detailcon")
    # print(item)
    # item = str(item)
    time = []
    # time = re.findall(r'<(.*。)', string)
    for pi in item.find_all(style="white-space:normal;line-height:32px;margin:0cm 0cm 0pt;"):
        pi = getText(pi.text)
        time.append(pi)
    # print(time)
    datadict["M_OpeningInformation"] = time[0:2]
    datadict["M_Booking"] = time[17:20]
    datadict["M_TicketInformation"] = time[16]
    datadict["M_Triffic"] = time[10:14]

    # 博物馆图片(list)
    url = "http://www.mtybwg.org.cn/about/924.aspx"
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    src = []
    for item in soup.find("ul", class_="detailcon").find_all("img"):
        src.append(item["src"])
    p = []
    for pi in src:
        pi = baseurl[0:-1] + pi
        p.append(pi)
    # print(p)
    datadict["M_Pictures"] = p
    # print(p)
    # 博物馆介绍
    src.clear()
    for item in soup.find("ul", class_="detailcon").find_all("p",class_="MsoNormal"):
        # print("===========")
        item = getText(item.text)
        src.append(item) 
    # print(src)
    p = []
    for pi in src:
        if len(pi) >= 10:
            p.append(pi)
        # srcs = re.findall('<img src="(.*?)"/>', str(src))
    datadict["M_Introduction"] = p 

    jsondata = json.dumps(datadict, ensure_ascii=False,indent = 4)
    with open("./museums/M130104.json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    return datadict
    exit()

def getCollectionsData():
    baseurl = "http://www.mtybwg.org.cn/"
    index = "http://www.mtybwg.org.cn/cangpin.aspx"
    html = askURL(index)

    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    # exit()
    href = []
    for item in soup.find("div", class_="rightcon").find("ul",class_="falllist animated").find_all("li"):
        href0 = item.find("a",class_="pic")["href"]
        href.append(href0)
    # print(href)
    # exit()
    n = len(href)  
    for href1 in href:
        url = href1
        html = askURL(url)
        soup = BeautifulSoup(html,"html.parser")

        hrefa = []
        for item in soup.find("div", class_="rightcon").find("ul",class_="falllist falllist2 animated").find_all("li"):
            href0 = item.find("a")["href"]
            hrefa.append(baseurl[0:-1] + href0)
        # print(hrefa)
        for href2 in hrefa:
            url = href2
            html = askURL(url)
            soup = BeautifulSoup(html,"html.parser")
            # print(type(href))
            collectiondict = {}
            collectiondict["CRM_In"] = ID
            Id = re.findall(r'http.*/(.*?).aspx', url)
            # print(Id)
            collectiondict["C_ID"] = ID + '-' + str(Id[0])

            item = soup.find("ul", class_="infolist")
                # print(item)
            title = re.findall(r'<h1>(.*)</h1>', str(item))
            title = str(title)

            src = str(item.find_all("img"))
            src = re.findall(r'<img.*src="(.*?)"', src)

            txt0 = item.find("div",class_="pluscon").find("ul", class_="con").text
            txt0 = getText(txt0)
            # txt0 = txt0.split()
            #     # print(txt0)
            txt = []
            txt.append("藏品描述：")
            txt.append(txt0)
            

            collectiondict["C_Name"] = title
            collectiondict["C_Pictures"] = baseurl[0:-1] + src[0]
            collectiondict["C_Introduction"] = txt

            jsondata = json.dumps(collectiondict, ensure_ascii=False,indent = 4 )
            with open("./collections/C"+collectiondict["C_ID"]+".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
            # exit()
        pass
    pass

def getActivitiesData():
    baseurl = "http://www.mtybwg.org.cn/"
# 展览
    index = "http://www.mtybwg.org.cn/zhanlan.aspx"
    html = askURL(index)

    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    # exit()
    href = []
    for item in soup.find("div", class_="rightcon").find("ul",class_="falllist animated").find_all("li"):
        href0 = item.find("a",class_="pic")["href"]
        href.append(href0)
    # print(href)
    # exit()
    n = len(href) - 1 
    for href1 in href:
        if href1 == "http://vr1.mtybwg.org.cn/20160316/":
            break
        url = href1
        html = askURL(url)
        soup = BeautifulSoup(html,"html.parser")

        hrefa = []
        for item in soup.find("div", class_="rightcon").find("ul",class_="falllist animated").find_all("li"):
            href0 = item.find("a")["href"]
            hrefa.append(baseurl[0:-1] + href0)
        # print(hrefa)
        for href2 in hrefa:
            url = href2
            html = askURL(url)
            soup = BeautifulSoup(html,"html.parser")
            # print(type(href))

            activityDict = {}
            activityDict["ARM_In"] = ID
            
            Id = re.findall(r'http.*/(.*?).aspx', url)
            activityDict["A_ID"] = ID + '-' + str(Id[0])

            item = soup.find("ul", class_="infolist")
                # print(item)
            title = re.findall(r'<h1>(.*)</h1>', str(item))
            title = str(title)

            src = str(item.find_all("img"))
            src = re.findall(r'<img.*src="(.*?)"', src)

            txt0 = item.find("ul",class_="detailcon").find("p", class_="MsoNormal").text
            txt0 = getText(txt0)
            # txt0 = txt0.split()
            #     # print(txt0)
            txt = []
            txt.append("活动描述：")
            txt.append(txt0)
            
            
            activityDict["A_Name"] = title
            activityDict["A_Type"] = "1"
            activityDict["A_Pictures"] = baseurl[0:-1] + src[0]
            activityDict["A_Information"] = txt

            jsondata = json.dumps(activityDict, ensure_ascii=False,indent = 4)
            with open("./activities/A"+activityDict["A_ID"]+".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
            # exit()
            
        pass
    pass
# 教育及学术活动（——微信推送格式，故只存链接）
    baseurl = "http://www.mtybwg.org.cn/"
    index = "http://www.mtybwg.org.cn/{}/0-1.aspx"
    # html = askURL(index)

    
    for pi in {"xueshu","xuanjiao"}:
        index0 = index.format(i)
        html = askURL(index0)
        # print(index0)
        soup = BeautifulSoup(html, "html.parser")
        # print("hhh")
        item = soup.find("ul", class_="infolist").find("ul",class_="iflist")
        href = []
        title = []
        if pi == "xuanjiao":
                type = "3"
        else:
            type = "2"
        for li in item.find_all("li"):
            # print("=3=3=3=3=3=3=")
            # print(li)
            if li.text == "":
                pass
            else:
                href.append(li.find("a")["href"]) 
                title.append(li.text)
    # print(title)
    # print(href)
        n = len(title)
        for i in range(n):
            activityDict = {}
            activityDict["ARM_In"] = ID
            activityDict["A_ID"] = ID + "-" + str(i+1)
            activityDict["A_Name"] = title[i]            
            activityDict["A_Type"] = type
            activityDict["A_Information"] = baseurl[0:-1]+href[i]

            jsondata = json.dumps(activityDict, ensure_ascii=False,indent = 4)
            with open("./activities/A"+activityDict["A_ID"]+".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
            exit()
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