# -*- coding: utf-8 -*-
"""
上海博物馆爬虫文件
@author: whl lxx

https://www.shanghaimuseum.net/mu/frontend/pg/index
090101

代码更新：

2020.04.
代码完成
2020.04.18
代码创建

"""

import requests
import os 
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
import time

def debugPrint(message): 
    if __name__ == "__main__":
        print(message)

def getMuseumData():
    datadict = {}  #用来存储爬取的网页信息
    datadict["M_ID"] = "090101"
    datadict["M_CName"] = "上海博物馆"
    datadict["M_EName"] = "Shanghai Museum"
    datadict["M_Batch"] = 1
    datadict["M_Address"] = "上海市黄浦区人民大道201号"
    
    

    # 主页内容
    baseurl = "https://www.shanghaimuseum.net"  #要爬取的网页链接
    datadict["M_Web"] = baseurl
    html = askURL(baseurl)  # 保存获取到的网页源码
    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # 开放时间
    for item in soup.find_all('div', class_="content" ):
        item = str(item)
        # print(item)
        linktime = re.findall(r'<p>(.*)<br/>', item)
        debugPrint(linktime)
        time0 = item[item.index("馆")+2 : item.index("后")]
        time = time0.replace('~','-')
        time = time.replace('，','-NULL-')
        print(time)
        datadict["M_OpeningTime"] = time

    # logo
    for item in soup.find_all('div', class_="shmu-top"):
        # print(item)
        item = str(item)
        il = re.findall(r'img src="(.*)"', item)[0]
        url = baseurl+il 
        datadict["M_Logo"] = url
        debugPrint(url)
        response=askPic(url)
        with open("./museums/img/footerlogo.png",'wb') as f:   
            f.write(response.content)

    # introduction
    url = "https://www.shanghaimuseum.net/mu/frontend/pg/infomation/history"
    html = askURL(url)  # 保存获取到的网页源码
    
    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")

    for item in soup.find_all("div", class_="shmu-detail shmu-detail-history"):
        item =str(item)
        # print(item)
        introduction_title = re.findall(r'<div class="title" style="text-indent: 2em;">(.*)</div>', item)
        debugPrint(introduction_title)
        item = re.sub(r'<br(\s+)?/>(\s+)?', "", item)   # 替换<br>
        texts = re.findall(r'<p>(.*。)</p>',item)
        # print(texts)
        s = ""
        for text in texts:
            s = s + text + "\n"
            debugPrint(text)
        datadict["M_Introduction"] = s
        
        imgSrc = re.findall(r'<img(?:.*)src="(.*jpg|png)"/>',item)
        for i in {0,1}:   
            imgSSrc = imgSrc[i]        
            imgSSrc = baseurl + "/mu/"+ imgSSrc
            debugPrint(imgSSrc)
 
    # 开放时间及票价
    url = "https://www.shanghaimuseum.net/mu/frontend/pg/service/admission"
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")

    # open("museum_spider/museums/temp/Opening.html",'w',encoding='utf-8').write(str(html))

    # html = open("temp/Opening.html",'r',encoding='utf-8').read()
    # print(html[0:100])

    items = soup.find_all("div", class_="shmu-detail shmu-detail-service")
    item = str(items)
    datadict["M_Ticket"] = "免费开放"
    
    item = re.sub(r'\xa0', ' ', item)   # 替换乱码
    item = re.sub(r'\u3000', ' ', item)   
    data1 = re.findall(r'<p>(.*。)</p>',item)
    debugPrint(data1)
    
    datadict["M_TicketInformation"] = data1
   
    items = soup.find_all("div", class_="openTimeBox")
    item = re.sub(r'<br/>', '</p>\n<p>', item)   # 替换<br>
    data = re.findall(r'<p>(.*)</p>',item) 
    # item = str(items[0])
    # data = re.findall(r'<p class="list".*>(.*)</p>',item)
    debugPrint(data)
    s = ""
    for i in {0,1,2}:
        s = s + data[i] + "\n"
    datadict["M_OpeningInformation"] = s

    jsondata = json.dumps(datadict, ensure_ascii=False,indent = 4)
    with open("./museums/M090101.json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    return datadict

def getCollectionsData():
    baseurl = "https://www.shanghaimuseum.net/mu/frontend/pg/article/id/CI0000"
    startnum = 5000
    endnum = startnum + 10
    
    for num in range(startnum, endnum):
        collectiondict = {}
        collectiondict["CRM_In"] = "090101"
        collectiondict["C_ID"] = "090101" + "-" + str(num)
        print("=====" + str(num))
        url = baseurl+str(num) 
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        # open('museum_spider/collections/temp.html', 'w', encoding='utf-8').write(str(html))
        s = ""
        srcs = []
        for item in soup.find_all("a", class_="shmu-box-content shmu-thumbnail shmu-thumbnail-no-image-resize"):
            # print(item)
            src = item.find_all("img")
            # print(src[0].string)
            src = re.findall('<img data-lazy="(.*?)"/>', str(src[0]))
            print(src[0])
            srcs.append(src[0])   
        srcs = list(set(srcs))
        for src in srcs:
            collectiondict["C_Pictuers"] = "https://www.shanghaimuseum.net/mu/"+src
        

        for item in soup.find_all("div",class_="shmu-columns"):
            # print(item)
            p = item.find_all("p")
            # print(p)
            for i in p:
                # print(i.text)
                s = s + i.text + '\n'
        print(s)
        collectiondict["C_Introduction"] = s

        for item in soup.find_all("div",class_="name"):
            print(item)
            title = item.text
            title = re.sub(r'\t','',title)
            title = re.sub(r'\n','',title)
        # print(title)
        collectiondict["C_Name"] = title
        jsondata = json.dumps(collectiondict, ensure_ascii=False,indent = 4 )
        with open("./collections/"+collectiondict["C_ID"]+".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)
    pass
# 已完成！！！！！啊啊啊啊啊
def getActivitiesData():
    baseurl = "https://www.shanghaimuseum.net/mu/frontend/pg/activity/activity-detail?id=1315"
    startnum = 25
    endnum = startnum + 4
    
    for num in range(startnum, endnum):
        activityDict = {}
        activityDict["A_ID"] = "090101" + "-" + str(num)
        print("=====" + str(num))
        url = baseurl+str(num) 
        html = askURL(url)
        soup = BeautifulSoup(html, "html.parser")
        # open('museum_spider/collections/temp.html', 'w', encoding='utf-8').write(str(html))
        s = ""
        srcs = []
        for item in soup.find_all("div", class_="shmu-main"):
            # print(item)
            src = item.find_all("img")
            # print(src[0].string)
            src = re.findall('<img src="(.*?)"/>', str(src[0]))
            print(src)
            srcs = str(src)
        activityDict["A_Pictuers"] = "https://www.shanghaimuseum.net/mu/"+srcs
        

        for item in soup.find_all("div",class_="activity-content"):
            # print(item)
            p = item.find_all("p")
            # print(p)
            for i in p:
                # print(i.text)
                s = s + i.text + '\n'
        s=str(s)
        # print(s)
        activityDict["A_Information"] = s

        for item in soup.find_all("div",class_="title"):
            # print(item)
            title = item.text
            title = re.sub(r'\t','',title)
            title = re.sub(r'\n','',title)
        print(title)
        activityDict["A_Name"] = title

        for item in soup.find_all("div",class_="content scroll-box"):
            # print(item)
            title = item.text
            title = re.sub(r'\t','',title)
            title = re.sub(r'\n','',title)
        title0 = title[title.index("间")+2 : title.index("地")]
        print(title0)
        activityDict["A_Date"] = title0

        jsondata = json.dumps(activityDict, ensure_ascii=False,indent = 4)
        with open("./activities/"+activityDict["A_ID"]+".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)
    pass
    
    
# 得到指定一个URL的网页内容
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
