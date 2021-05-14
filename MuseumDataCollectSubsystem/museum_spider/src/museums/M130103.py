# -*- coding: utf-8 -*-
"""
福建省泉州海外交通史博物馆爬虫文件
@author: lxx

http://www.qzhjg.cn/html/index.html
130103

代码更新：

2020.05.10
代码完成
2020.05.09
代码创建

"""

import requests
import os 
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
import time

ID = "130103"
def debugPrint(message): 
    if __name__ == "__main__":
        print(message)

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
    datadict["M_ID"] = "130103"
    datadict["M_CName"] = "福建省泉州海外交通史博物馆"
    datadict["M_EName"] = "Quanzhou Maritime Museum Fujian"
    datadict["M_Batch"] = 1
    datadict["M_Address"] = "泉州市丰泽区东湖街425号"

    #官网主页相关内容
    baseurl = "http://www.qzhjg.cn/"  #要爬取的网页链接
    datadict["M_Web"] = baseurl + "/html/index.html"
    html = askURL(baseurl)  # 保存获取到的网页源码
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # logo 
    src = soup.find("div",class_="logo").find("a").find("img")["src"]
    src = str(src)
    # print(src)
    datadict["M_Logo"] = baseurl + src

    # 博物馆开放时间及门票
    i = 0
    time = []
    booking = []
    for item in soup.find("div", class_="footer_hd").find_all("dl",class_="col_info"):
        item = str(item)
        # print(item)
        linktime = re.findall(r'<dd>(.*?)</dd>', item)
        if i == 1:
            time.append(linktime[2])
            time.append(linktime[0])
            time.append(linktime[1])
        # print(time)
        if i == 2:
            time.append(linktime[2])
            time.append(linktime[0])
            time.append(linktime[1])
        if i == 3:
            booking.append(linktime[0])
            booking.append(linktime[1])
        i += 1
    # print(time)
    # print(booking)
    datadict["M_Openingtime"] = "夏令时，8：30—17：30；\n冬令时，8：30—17：00；\n详细请见开放信息"
    datadict["M_OpeningInformation"] = time
    datadict["M_Booking"] = booking
    datadict["M_Ticket"] = "免费开放"
    # 门票信息 
    
    text = "海交馆春节也不关门，更别说其他时间了，欢迎五湖四海的朋友们参观。博物馆自2008年之后便实行了免费开放，海交馆也是全年免费开放，但为了更好地维护、保养文物，我们每周一闭馆（节假日照常开放）。"
    # print(text)
    datadict["M_Ticketinformation"] = text

    # 博物馆图片(list)
    url = "http://www.qzhjg.cn/html/hjgjj.html"
    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    src = []
    for item in soup.find("div", class_="detail_con").find_all("img"):
        src.append(item["src"])
    p = []
    for pi in src:
        pi = baseurl + pi
        p.append(pi)
    # print(p)
    datadict["M_Pictures"] = p
    # print(p)
    # 博物馆介绍
    src.clear()
    for item in soup.find("div", class_="detail_con").find_all("p"):
        # print("===========")
        src.append(item.text) 
    # print(src)
    p = []
    for pi in src:
        if len(pi) >= 10:
            p.append(pi)
        # srcs = re.findall('<img src="(.*?)"/>', str(src))
    datadict["M_Introduction"] = p 

    jsondata = json.dumps(datadict, ensure_ascii=False,indent = 4)
    with open("./museums/M130103.json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    return datadict

def getCollectionsData():
    baseurl = "http://www.qzhjg.cn/"
    index = "http://www.qzhjg.cn/html/dcwc/index.html"
    html = askURL(index)

    soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    href = []
    for item in soup.find("div", class_="thumbList").find("ul",class_="clearfix").find_all("li"):
        href0 = str(item.find("a")) 
        # item = str(item)
        href0 = re.findall(r'<a.*?href="(.*?)"', href0)
        href0 = str(href0[0])
        href.append(baseurl[0:-1] + href0)

    n = len(href)  
    for href1 in href:
        url = href1
        html = askURL(url)

        driver = webdriver.Chrome()
        driver.minimize_window()
        time.sleep(1)
        driver.get(href1)
        html = driver.page_source
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        collectiondict = {}
        collectiondict["CRM_In"] = ID
        Id = re.findall(r'http.*/(.*?).html', url)
        collectiondict["C_ID"] = ID + '-' + str(Id[0])
        src = soup.find("div", class_="picshowtop").find("a").find("img")["src"]
        # print(src)
        src = baseurl[0:-1] + src
            # 博物馆官网未公布详细藏品描述
        title = soup.find("div",class_="picshowtxt_right").text

        collectiondict["C_Name"] = title
        collectiondict["C_Pictures"] = src
        collectiondict["C_Introduction"] = href1

        jsondata = json.dumps(collectiondict, ensure_ascii=False,indent = 4 )
        with open("./collections/C"+collectiondict["C_ID"]+".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)

    pass

def getActivitiesData():
    baseurl = "http://www.qzhjg.cn/"
    index = "http://www.qzhjg.cn/html/{}/index.html"# 各类活动
# 教育活动及学术活动   
    href = []
    title = []
    for pi in {"jy","ky"}:
        index = index.format(pi)
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # driver = webdriver.Chrome(executable_path='<path-to-chrome>', options=options)
        driver = webdriver.Chrome()
        driver.minimize_window()
        time.sleep(1)
        driver.get(index)

        html = driver.page_source
        # print(html)
        driver.close()
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        item = soup.find("div", class_="articleBox_list").find("ul")
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
        n = min(len(title),20) 
        for i in range(n):
            if pi == "jy":
                type = "3"
            else:
                type = "2"
            activityDict = {}
            activityDict["ARM_In"] = ID
            activityDict["A_ID"] = ID + "-" + type + str(i+1)
            activityDict["A_Name"] = title[i]
            activityDict["A_Type"] = type
            # print(pi)
            # if pi == "jy":
            #     activityDict["A_Type"] = "3"
            # else:
            #     activityDict["A_Type"] = "2"
            # 详情页
            url = baseurl[0:-1]+href[i]  #要爬取的网页链接
            # print("==========="+url)
            # exit()
            html = askURL(url)  # 保存获取到的网页源码
            soup = BeautifulSoup(html, "html.parser")
            txt = []
            for item in soup.find("div", class_="detail_con").find_all("p"):
                # print(item)
                txt0 = item.text
                txt0 = getText(txt0)
                # print(txt0)
                if len(txt0) >= 15:
                    txt.append(txt0)
            # print(txt)
            src = []
            for item in soup.find_all("div", class_="detail_con"):
                # print(item)
                src = re.findall(r'src="(.*?)"', str(item))   
            # print(src)           
            srcs = []
            for pi in src:
                pi = str(pi)
                if src != '':
                    srcs.append(baseurl[0:-1] + pi) 
            activityDict["A_Name"] = title[i]
            activityDict["A_Pictures"] = srcs
            activityDict["A_Information"] = txt[0:5]


            jsondata = json.dumps(activityDict, ensure_ascii=False,indent = 4)
            with open("./activities/A"+activityDict["A_ID"]+".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
            # exit()
# 临时展览(从列表页爬取结果)
    type = '1'
    index = index.format('zl')
    driver = webdriver.Chrome()
    driver.minimize_window()
    time.sleep(1)
    driver.get(index)

    html = driver.page_source
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    title = []
    href = []
    src = []
    inform = []
    item = soup.find("div", class_="exhibitionList").find("ul")
    for li in item.find_all("li"):
        # print("=3=3=3=3=3=3=")
        # print(li)
        title0 = li.find("div",class_="info").find("h3").text
        title0 = re.findall(r'(.*)...', title0)
        title.append(str(title0))
        href0 = li.find("div",class_="thumb").find("a")["href"]
        href.append(baseurl[0:-1] + href0)
        src0 = li.find("div",class_="thumb").find("img")["src"]
        src.append(baseurl[0:-1] + src0)
        inform0 = li.find("div",class_="info").find("p").text
        inform.append(inform0)
    # print(title)
    # print(href)
    n = len(title)
    for i in range(n):
        activityDict = {}
        activityDict["ARM_In"] = ID
        activityDict["A_ID"] = ID + "-" + type + str(i+1)
        activityDict["A_Name"] = title[i]
        activityDict["A_Type"] = type
        activityDict["A_Name"] = title[i]
        activityDict["A_Pictures"] = src[i]
        activityDict["A_Information"] = href[i] + '\n' + inform[i]


        jsondata = json.dumps(activityDict, ensure_ascii=False,indent = 4)
        with open("./activities/A"+activityDict["A_ID"]+".json", 'w', encoding='utf-8') as f:
            f.write(jsondata)
        # exit()
    driver.close()
    driver.quit()
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
    # getMuseumData()
    # getCollectionsData()
    getActivitiesData()