# -*- coding: utf-8 -*-
"""
成都武侯祠博物馆爬虫文件
@author: whl

http://www.wuhouci.net.cn/index.html
230103

"""

import requests
import os 
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver # 导入webdriver包
import time


def debugPrint(message): 
    if __name__ == "__main__":
        print(message)

ID = "230103"

def getText(item, newline=False):
    item = re.sub(r"<br/>","",item, flags=re.I)
    item = re.sub(r"<br />","",item,flags=re.I)
    item = re.sub(r"<br>","",item,flags=re.I)
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
    datadict["M_ID"] = ID
    datadict["M_CName"] = "成都武侯祠博物馆"
    datadict["M_EName"] = "Chengdu Wuhou Shrine"
    datadict["M_Batch"] = 1
    datadict["M_Address"] = "四川省成都市武侯祠大街231号"
    # datadict["M_Web"] = "http://www.wuhouci.net.cn/index.html"
    

    # 主页内容
    baseurl = "http://www.wuhouci.net.cn/index.html"  #要爬取的网页链接
    datadict["M_Web"] = baseurl
    html = askURL(baseurl)  # 保存获取到的网页源码
    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")


    # logo
    datadict["M_Logo"] = "http://www.wuhouci.net.cn/resources/assets/images/logoBlack.png?v=1"
    debugPrint(datadict["M_Logo"])



    ######################################################## 票务
    url = "http://www.wuhouci.net.cn/pwxx.html"
    html = askURL(url)  # 保存获取到的网页源码
    # open("temp.html",'w',encoding='utf-8').write(html)
    # html = open("temp.html",'r',encoding='utf-8').read()
    
    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")
    # print(html)
    datadict = {}
    items = soup.find_all("div", class_="ticketTopBox")
    titles = []
    texts = []
    for item in items:
        item = str(item)
        item = re.sub(r'<br/>',' ',item)
        # print(item)
        title = re.findall(r'<div class="l">(.*?)</div>',item)
        titles.extend(title)
        # print(title)
        text = re.findall(r'<p>(.*?)</p>',item)
        texts.extend(text)
        # print(text)

    datadict["M_OpeningTime"] = "9:00-17:00-NULL-18:00"
    datadict["M_OpeningInformation"] = texts[0:1]
    # print(texts[0])
    datadict["M_Ticket"] = "50元/人"
    datadict["M_TicketInformation"] = texts[2:]
    # print(texts[1:])

    items = soup.find_all("div", class_="ticketInfo")
    for item in items:
        item = str(item)
        il = re.findall(r'<p.*?>(.*?)</p>',item)
        # print(il)

    datadict["M_TicketInformation"].extend(il)
    

    ############################################### introduction
    url = "http://www.wuhouci.net.cn/about.html"
    html = askURL(url)  # 保存获取到的网页源码
    # open("temp.html",'w',encoding='utf-8').write(html)
    # html = open("temp.html",'r',encoding='utf-8').read()

    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")
    # print(html)
    for item in soup.find_all("div", class_="aboutBox boxWidth"):
        # item = str(item)
        # s = item.text 
        # print(item.text)
        datadict["M_Introduction"] = item.text

        il = re.findall(r'src="(.*?[.JPG|.jpg|.png|.PNG])"', str(item))
        src = [baseurl + i[3:] for i in il]
        debugPrint(src)
        datadict["M_Pictures"] = src

    ######################################### M_Triffic
    url = "http://www.wuhouci.net.cn/jtzy.html"
    html = askURL(url)  # 保存获取到的网页源码
    # open("temp.html",'w',encoding='utf-8').write(html)
    # html = open("temp.html",'r',encoding='utf-8').read()
    
    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="trafficBox boxWidth"):
        # print(item.text)
        datadict["M_Triffic"] = item.text

    jsondata = json.dumps(datadict, ensure_ascii=False)
    with open("museum_spider/museums/M" + ID +".json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    pass


def getCollectionsData():
    baseurl = "http://www.wuhouci.net.cn/"
    index = "http://www.wuhouci.net.cn/wwjc.html"
    html = askURL(index)
    # print(html)
    pageurl = "http://www.wuhouci.net.cn/wwjc-detail.html#id="

    driver = webdriver.Edge()
    driver.minimize_window()
    time.sleep(5) # 暂停5秒钟

    num = []
    for page in [1,2]:
        url = "http://www.wuhouci.net.cn/wwjc.html?page="+str(page)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="grid__item"):
            data_id = re.findall(r'data-id="(.*?)"', str(item))
            num.append(eval(data_id[0]))
    
    for n in num:
        collectiondict = {}
        url = pageurl + str(n)
        collectiondict["C_ID"] = ID+"-"+str(n)
        collectiondict["CRM_In"] = ID
        # driver.maximize_window() # 最大化浏览器

        driver.get(url) # 通过get()方法，打开一个url站点
        html = driver.page_source
        asoup = BeautifulSoup(html, 'html.parser')
        texts = []
        
        for item in asoup.find_all("div", class_="sw-news-bottom"):
            s = re.findall(r'url\((.*?)\);', str(item))
            print(s)
            collectiondict["C_Pictures"] = baseurl + s[0][1:]
            
            for p in item.find_all("p"):
                texts.append(p.text)
                # print(p.text)
        print(texts)
        collectiondict["C_Name"] = texts[0]
        collectiondict["C_Introduction"] = texts
        jsondata = json.dumps(collectiondict, ensure_ascii=False)
        with open("museum_spider/collections/C"+collectiondict["C_ID"]+".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)
    
    driver.close()

    pass

def getActivitiesData():
    MaxPage = 1  # 最大翻页
    MaxNum = 10  # 最大爬取数

    baseurl = "http://www.wuhouci.net.cn"
    indexurl = "http://www.wuhouci.net.cn/ztzl.html"
    headurl = "http://www.wuhouci.net.cn/ztzl-detail.html#id="
    # options = webdriver.ChromeOptions()
    # options.debugger_address = "127.0.0.1:5555"
    driver = webdriver.Edge()
    # driver = webdriver.Chrome()
    
    
    driver.minimize_window()
    # driver.maximize_window()
    time.sleep(1)
    driver.get(indexurl)
    es = driver.find_element_by_class_name("boxs")
    time.sleep(1)
    # print(es)
    if es is not list:
        es = [es]
    data_ids = []
    for i in range(min(len(es), MaxPage)):
        es[i].click()  
        es = driver.find_elements_by_class_name("boxs")
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="vNewsList"):
            data_id = re.findall(r'data-id="(.*?)"', str(item))
            data_ids.extend(data_id)
    
    data_ids = data_ids[0:min(MaxNum, len(data_ids))]
    for data_id in data_ids:
        adict = dict()
        adict["A_ID"] = ID + "-" + data_id
        adict["ARM_In"] = ID
        
        
        url = headurl + data_id 
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="vdetail"):
            adict["A_Name"] = item.find_all("div", class_="title")[0].text
            # print(adict["A_Name"])
            field = item.find_all("div", class_="LSw swiper-container swiper-container-horizontal")[0]
            src = re.findall(r'<img src="(.*?)"/>', str(field))[0:-1]
            adict["A_Picture"] = [baseurl + s for s in src]
            # print(adict["A_Picture"])
            # time
            adict["A_Date"] = re.findall(r'<summary class="sPR timer">(.*?)</summary>', str(item))[0]
            
            s = ""
            for i in item.find_all("li", class_=""):
                s = s + i.text + '\n'
            #  
            # print(s)
            for i in item.find_all("div", class_="vcontent commonDetail"):
                s = s + i.text + '\n'
            # print(s)
            adict["A_Information"] = s
            
            jsondata = json.dumps(adict, ensure_ascii=False)
            with open("museum_spider/activities/A"+adict["A_ID"]+".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)

    time.sleep(5)
    driver.close()
    driver.quit()
    exit()
    n = startnum
    while n >= endnum:
        adict = dict()
        adict["A_ID"] = ID + "-" + str(n)
        adict["ARM_In"] = ID
        debugPrint("===="+adict["A_ID"])
        url = baseurl + "showinfo.asp?id=" + str(n) + "&bigclass=25"
        # print(url)
        html = askURL(url)  # 保存获取到的网页源码
        # open("temp.html",'w',encoding='utf-8').write(html)
        # html = open("temp.html",'r',encoding='utf-8').read()
        
        # print(html[0:100])
        soup = BeautifulSoup(html, "html.parser")
        # print(html)

        items = soup.find_all("td")
        # count = 0
        # for item in items:
        #     print("==========", count)
        #     print(item)
        #     count = count + 1
        
        item =str(items[32])
        s = getText(item)
        debugPrint(s)
        adict["A_Name"] = s

        item =str(items[33])
        s = getText(item)
        s = s[0:-21]
        adict["A_Information"] = s
        debugPrint(s)
        n = n -1

        jsondata = json.dumps(adict, ensure_ascii=False)
        with open("museum_spider/activities/A"+adict["A_ID"]+".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)


    pass 

# 得到指定一个URL的网页内容
def askURL(url):
    # head = headers[0]
    head = {
        'User-Agent':'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
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
        open('temp.html','w',encoding=res.encoding).write(html)
    
    except requests.RequestException as e:
        print(e)

    return html




if __name__ == "__main__":
    # getMuseumData()
    # getCollectionsData()
    getActivitiesData()
