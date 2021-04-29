# -*- coding: utf-8 -*-
"""
中国电影博物馆爬虫文件
@author: HofCY
@version 创建时间：2020.04.21
http://www.cnfm.org.cn/
010402

代码更新：

2020.04.29
代码完成
2020.04.21
代码创建

"""


# 引入的包自行引入，不做要求
# 服务器自行伪装，不做要求

import requests
import os
from bs4 import BeautifulSoup
import re
import json
from requests_html import HTMLSession
from aip import AipOcr


# APP_ID='24072189'
# APP_KEY='1kVCOPzhb52M3By04nobdfIc'
# SECRET_KEY='qoc03Nsy0h9mVsRzbENfDa46kfH5IHvp'

def debugPrint(message):
    if __name__ == "__main__":
        print(message)

def getMuseumData():
    """
    获得博物馆及其子馆的介绍
    并生成数据字典
    先自行保存在一个位置
    """
    datadict = {}  # 用来存储爬取的网页信息
    datadict["M_ID"] = "010402"
    datadict["M_CName"] = "中国电影博物馆"
    datadict["M_EName"] = "China National Film Museum"
    datadict["M_Batch"] = 4
    datadict["M_Address"] = "北京市朝阳区南影路9号"

    # 主页内容
    baseurl = "http://www.cnfm.org.cn/"  # 要爬取的网页链接
    datadict["M_Web"] = baseurl
    html = askURL(baseurl)  # 保存获取到的网页源码
    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")
    open("temp/Opening.html", 'w', encoding='utf-8').write(str(html))

    # 开放时间
    for item in soup.find_all('body'):
        item = str(item)
    #print(item)
    res = r'<a .*?>(.*?)</a>'
    mm = re.findall(res, item, re.S | re.M)
    time0 = re.findall(r'：(.*?)9', mm[0])
    time01 = re.findall(r'五(.*?)（', mm[0])
    time1 = re.findall(r'，(.*?)9', mm[0])
    time11 = re.findall(r'日(.*?)（', mm[0])
    time2 = re.findall(r'（(.*?)停', mm[0])
    time = time0[0] + "：" + time01[0] + "-NULL-" + time2[0] + "\n" + time1[0] + "：" + time11[1] + "-NULL-" + time2[1] + "\n"
    datadict["M_OpeningTime"] = time
    datadict["M_OpeningInformation"] = mm[0]
    debugPrint(time) # 是否输出（？） h
    debugPrint(mm[0])


    # logo 在背景图上，暂未爬取

    # introduction
    session = HTMLSession()
    url = 'http://www.cnfm.org.cn/ybxxjs/ybjj.shtml'
    r = session.get(url)
    s = ""
    for text in r.html.find('p.MsoNormal'):
        s = s + text.text
        print(text.text)
    datadict["M_Introduction"] = s

    # 门票信息和开放信息
    datadict["M_Ticket"] = "暂无获取途径"
    session = HTMLSession()
    url = 'http://www.cnfm.org.cn/2020-07/15/cms18248article.shtml'
    r = session.get(url)
    s = ""
    i = 0
    for OTInformation in r.html.find('p.MsoNormal'):
        i = i+1
        if i>1 and i<29:
            s = s + OTInformation.text
            print(OTInformation.text)
    datadict["M_TicketInformation"] = s

    jsondata = json.dumps(datadict, ensure_ascii=False, indent=4)
    with open("../museums/M010402.json", 'w', encoding='utf-8') as f:
        f.write(jsondata)


def getCollectionsData():
    """
    获得博物馆藏品信息
    并生成数据字典
    先自行保存在一个位置
    """
    collectiondict = {}
    url = 'http://www.cnfm.org.cn/gcjp/gcjp.shtml'
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    i = 0
    for w in soup.find_all('p', attrs={ 'class':'font12 txtcenter'}):
        i = i+1
        w = str(w)
        # print(i)
        # print(w)
        findlink = r'<a href="(.*?)"'
        link = re.findall(findlink, w)
        # print(link)
        web = link
        link = str(link)
        findid = r'/cms(.*?)article'
        findname = r'target="_blank">(.*?)</a>'
        cid = re.findall(findid, link)
        cid = str(cid)
        collectiondict["C_ID"] = cid
        cname = re.findall(findname, w)
        cname = str(cname)
        collectiondict["C_Name"] = cname
        print(cid)
        print(cname)
        web1 = 'http://www.cnfm.org.cn'
        a = web[0]
        # print(a)
        link = web1 + str(a)
        # print(link)
        chtml = askURL(link)
        soup = BeautifulSoup(chtml, "html.parser")
        m = 1
        cip = {}
        for test in soup.find_all(attrs={'class':'article2_n'}):
            test = str(test)
            # print(test)
            for p in re.findall('src="(.*?)"', test):
                p = web1 + p
                # print(p)
                cip[m] = p
                m = m+1
                collectiondict["C_Introduction"] = str(cip)

        if i == 1:
            jsondata = json.dumps(collectiondict, ensure_ascii=False, indent=4)
            with open("../collections/C010402.json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
        else:
            jsondata = json.dumps(collectiondict, ensure_ascii=False, indent=4)
            with open("../collections/C010402.json", 'a', encoding='utf-8') as f:
                f.write(jsondata)
pass

def getActivitiesData():
    """
    获得博物馆活动信息
    并生成数据字典
    先自行保存在一个位置
    """
    activityDict = {}
    url = 'http://www.cnfm.org.cn/ybzl/ztzl.shtml'
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    i = 0
    for w in soup.find_all('p', attrs={'class': 'font16 txtcenter'}):
        i = i + 1
        w = str(w)
        # print(i)
        # print(w)
        findlink = r'<a href="(.*?)"'
        link = re.findall(findlink, w)
        # print(link)
        web = link
        link = str(link)
        findid = r'/cms(.*?)article'
        findname = r'target="_blank">(.*?)</a>'
        aid = re.findall(findid, link)
        aid = str(aid)
        activityDict["A_ID"] = aid
        aname = re.findall(findname, w)
        aname = str(aname)
        activityDict["A_Name"] = aname
        cuowu = [' ']
        cuowu = str(cuowu)
        if aname == cuowu:
            continue
        print(aid)
        print(aname)
        web1 = 'http://www.cnfm.org.cn'
        a = web[0]
        # print(a)
        if aid == '[]':
            link = a
            activityDict["A_Introduction"] = str(link) + "，VR全景连接"
        else:
            link = web1 + str(a)
        print(link)
        chtml = askURL(link)
        soup = BeautifulSoup(chtml, "html.parser")
        m = 1
        aip = {}
        for test in soup.find_all(attrs={'class': 'article2_n'}):
            test = str(test)
            # print(test)
            for p in re.findall('src="(.*?)"', test):
                p = web1 + p
                # print(p)
                aip[m] = p
                m = m + 1
                activityDict["A_Introduction"] = str(aip)

        if i == 1:
            jsondata = json.dumps(activityDict, ensure_ascii=False, indent=4)
            with open("../activities/A010402.json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
        else:
            jsondata = json.dumps(activityDict, ensure_ascii=False, indent=4)
            with open("../activities/A010402.json", 'a', encoding='utf-8') as f:
                f.write(jsondata)



    pass


# 得到指定一个URL的网页内容
def askURL(url):
    # head = headers[0]
    head = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
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
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
    }
    try:
        res = requests.get(url, headers=head)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
    except requests.RequestException as e:
        print(e)
    return res




if __name__ == "__main__":
    # getMuseumData()
    # getCollectionsData()
    getActivitiesData()