# -*- coding: utf-8 -*-
"""
井冈山革命博物馆博物馆爬虫文件
@author: lxx

http://www.jgsgmbwg.com/
140101

代码更新：

2020.05.12
代码完成
2020.05.11
代码创建

"""

import requests
import os 
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
import time

ID = "140101"
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
    datadict["M_ID"] = "140101"
    datadict["M_CName"] = "井冈山革命博物馆"
    datadict["M_EName"] = "Museum of Revolution in Jinggang Mountains"
    datadict["M_Batch"] = 1
    datadict["M_Address"] = "江西省井冈山茨坪红军南路"

    #官网主页相关内容
    baseurl = "http://www.jgsgmbwg.com/"  #要爬取的网页链接
    datadict["M_Web"] = baseurl 
    html = askURL(baseurl)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # logo 及博物馆图片
    datadict["M_Logo"] = 'http://www.jgsgmbwg.com/templates/default/images/logo.png'
    item = soup.find("div", class_="slides")
    srcs = item.find("img",alt="井冈山革命博物馆")["src"]
    # print(src)
    src = baseurl[0:-1] + str(srcs[0])
    datadict["M_Pictures"] = src
    # 博物馆开放时间及门票\门票信息 

    url = "http://www.jgsgmbwg.com/newsshow.php?cid=19&id=6730"
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    item = soup.find("div",id="textarea")
    text =[]
    for pi in item.find_all("p",class_="MsoNormal"):
        pi = getText(pi.text)
        text.append(pi)
    # print(text)for pi in item.find_all(""):
    # print(text)
    # exit()
    time = []
    time.append("开放时间：")
    time.append(text[3])
    p = re.findall(r'(.*。)', text[1])
    time.append(str(p[0]))
    p = re.findall(r'每周二至周日(.*)，', text[3])
    # print(time)
    # print(booking)
    datadict["M_Openingtime"] = str(p[0])
    datadict["M_OpeningInformation"] = time
    datadict["M_Ticket"] = "免费开放"
    datadict["M_Booking"] = "请关注官网及微信公众号"
    datadict["M_Ticketinformation"] = text[5:7]
    # exit()

    # 博物馆介绍
    url = "http://www.jgsgmbwg.com/about.php?cid=3"
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    src = []
    j =0
    for item in soup.find("div", class_="subCont").find_all("p"):
        # print("===========")
        item = getText(item.text)
        src.append(item) 
        j += 1
        if j > 4:
            break
    # print(src)
    # p = []
    # for pi in src:
    #     if len(pi) >= 10:
    #         p.append(pi)
        # srcs = re.findall('<img src="(.*?)"/>', str(src))
    datadict["M_Introduction"] = src 

    jsondata = json.dumps(datadict, ensure_ascii=False,indent = 4)
    with open("./museums/M140101.json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    return datadict

def getCollectionsData():
    baseurl = "http://www.jgsgmbwg.com/"
    index = "http://www.jgsgmbwg.com/bwg.php?cid=6"
    html = askURL(index)
    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    href = []
    src = []
    title = []
    item = soup.find("div", class_="subCont").find("ul",class_="product_list")
    for item in item.find_all("li"):   
        srcs = item.find("a").find("img")["src"]
        src.append(baseurl[0:-1] + srcs)

        href0 = str(item.find("a")) 
        # item = str(item)
        href0 = re.findall(r'<a.*?href="(.*?)"', href0)
        href0 = str(href0[0])
        href0 = re.sub('&amp;', '&', href0)
        href.append(baseurl + href0)

        title0 = item.find("p").find("a").text
        title0 = re.sub(r"\n","",title0)
        title.append(title0)
    # print(href)
    n = len(href) 
    print(href)
    for i in range(n):
        url = href[i]
        # print(url)
        # driver.get(url) # 通过get()方法，打开一个url站点
        html = askURL(url)
        soup = BeautifulSoup(html,"html.parser")
        # print(soup)
        collectiondict = {}
        collectiondict["CRM_In"] = ID
        Id = re.findall(r'http.*&id=(.*)', url)
        collectiondict["C_ID"] = ID + '-' + str(Id[0])

        item = soup.find("span", class_="style1")
        item = getText(item.text)
        # print(item)
        txt = []
        txt.append("藏品描述：")
        # txt0 = item.split()
        # # print(txt)
        # for pi in txt0:
        #     if len(pi) > 10:
                
        txt.append(item)

        collectiondict["C_Name"] = title[i]
        collectiondict["C_Pictures"] = src[i]
        collectiondict["C_Introduction"] = txt

        jsondata = json.dumps(collectiondict, ensure_ascii=False,indent = 4 )
        with open("./collections/C"+collectiondict["C_ID"]+".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)
        # exit()
    pass

def getActivitiesData():
# 该博物馆未公布活动信息，此处只展示相关常设展览
    baseurl = "http://www.jgsgmbwg.com/"
    index = "http://www.jgsgmbwg.com/jzjj.php?cid=44"
    html = askURL(index)
    soup = BeautifulSoup(html, "html.parser")
        # print("hhh")
    href = []
    item = soup.find("div", class_="subCont").find("ul",class_="news_list2")
    # print(item)
    # print(type(item))
    for li in item.find_all("li"):
        href0 = str(li.find("span",class_="title").find("a")) 
        # item = str(item)
        href0 = re.findall(r'<a.*?href="(.*?)"', href0)
        href0 = str(href0[0])
        href0 = re.sub('&amp;', '&', href0)
        href.append(baseurl + href0)
    # print(title)
    # print(href)
    n = len(href)
    data = []
    for i in range(n):
        url = href[i+1]
        print(url)
        html = askURL(url)
        soup = BeautifulSoup(html,"html.parser")

        # print(soup)
        item = soup.find("div",class_="listConts")# .find("div")
        # print(item)
        title0 = item.find("h1",class_="title").text
        title0 = re.sub(r"\n","",title0)

        srcs = item.find("img")["src"]
        src = baseurl[0:-1] + srcs
        j = 0
        for pi in item.find_all("p"):
            j += 1
            data0 = getText(pi.text) 
            print(data0)
            if len(data0) > 15:
                data.append(data0)
            if j >3:
                break
        pass

        activityDict = {}
        activityDict["ARM_In"] = ID
        activityDict["A_ID"] = ID + "-" + str(i+1)
        activityDict["A_Name"] = title0
        activityDict["A_Pictures"] = src
        activityDict["A_Information"] = data

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