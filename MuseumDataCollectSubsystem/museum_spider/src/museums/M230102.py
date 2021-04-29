# -*- coding: utf-8 -*-
"""
三星堆博物馆爬虫文件
@author: whl

http://sxd.cn/
230102

"""

import requests
import os 
from bs4 import BeautifulSoup
import re
import json


ID = "230102"


def getMuseumData():
    datadict = {}  #用来存储爬取的网页信息
    datadict["M_ID"] = ID
    datadict["M_CName"] = "三星堆博物馆"
    datadict["M_EName"] = "Sanxingdui Museum"
    datadict["M_Batch"] = 1
    datadict["M_Address"] = "四川省广汉市西安路133号"
    datadict["M_Web"] = "http://sxd.cn/"
    

    # 主页内容
    baseurl = "http://sxd.cn/"  #要爬取的网页链接
    datadict["M_Web"] = baseurl
    html = askURL(baseurl)  # 保存获取到的网页源码
    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")


    # logo
    datadict["M_Logo"] = baseurl + "photo/logo.png"
    # print(datadict["M_Logo"])



    ############################################### introduction
    url = "http://sxd.cn/showinfo.asp?id=1526&bigclass=5"
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
    item =str(items[37])
    nsoup = BeautifulSoup(item, "lxml")
    # print(nsoup.text[0:-35])
    datadict["M_Introduction"] = nsoup.text[0:-35]

    # print(item)
    il = re.findall(r'src="(.*?[.JPG])"', item)
    src = [baseurl + i[3:] for i in il]
    # print(src)
    datadict["M_Pictures"] = src

    ######################################### M_Triffic
    url = "http://sxd.cn/showinfo.asp?id=19&bigclass=31"
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
    item =str(items[31])
    nsoup = BeautifulSoup(item, "lxml")
    # print(nsoup.text[0:-35])
    datadict["M_Triffic"] = nsoup.text[0:-35]

    ######################################################## 票务
    url = "http://sxd.cn/showinfo.asp?id=18&bigclass=31"
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
    
    item =str(items[31])
    nsoup = BeautifulSoup(item, "lxml")
    # print(nsoup.text[0:-35])
    datadict["M_TicketInformation"] = nsoup.text[0:-35]
    datadict["M_OpeningTime"] = "8:30-17:00-NULL-18:00"
    datadict["M_OpeningInformation"] = ""

    jsondata = json.dumps(datadict, ensure_ascii=False)
    with open("museum_spider/museums/M" + ID +".json", 'w', encoding='utf-8') as f:
        f.write(jsondata)
    # exit()
    pass


def getCollectionsData():
    
    baseurl = "http://sxd.cn/"
    collectionClass = [4,5,6,43]
    
    url2 = "http://www.sxd.cn/showinfojp.asp?id="
    for i in collectionClass:
        url = "http://sxd.cn/list_2.asp?bigclass=29&smallclass="+str(i)+"&Page=1"
        html = askURL(url)
        # open("temp.html",'w', encoding='utf-8').write(str(html))
        # html = open("temp.html", 'r', encoding='utf-8').read()
        items = re.findall(r'<a href="javascript:dlgopen\(\'(.*?)\',([0-9]+)\)" title=".*?">',html)
        for item in items:
            collectiondict = {}
            collectiondict["C_ID"] = ID+"-"+item[1]
            # print("======="+collectiondict["C_ID"]+"  "+str(item))
            collectiondict["CRM_In"] = ID
            collectiondict["C_Name"] = item[0]
            url = url2 + item[1]

            html = askURL(url)
            html = str(html)
            # open("temp.html",'w', encoding='utf-8').write(str(html))
            # html = open("temp.html", 'r', encoding='utf-8').read()
            src = re.findall(r'src="(.*?[.jpg|.JPG|.png|.PNG])"', html)
            # print(src)
            collectiondict["C_Pictures"] = baseurl + src[0]

            soup = BeautifulSoup(html, "html.parser")
            items = soup.find_all("td")
            # print(items[0].text)
            collectiondict["C_Introduction"] = items[0].text
            
            jsondata = json.dumps(collectiondict, ensure_ascii=False)
            with open("museum_spider/collections/C"+collectiondict["C_ID"]+".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)

    pass

def getActivitiesData():
    baseurl = "http://sxd.cn/"
    url = "http://sxd.cn/list_1.asp?bigclass=25&smallclass=45"
    html = askURL(url)
    # open("temp.html",'w', encoding='utf-8').write(str(html))
    # html = open("temp.html", 'r', encoding='utf-8').read()
    # soup = BeautifulSoup(html, "html.parser")
    html = str(html)
    il = re.findall(r'<a href="(.*?)" title="(.*?)">(.*?)</a>', html)
    num = re.findall(r'showinfo.asp\?id=([0-9]+)&bigclass=[0-9]+', il[0][0])[0]
    startnum = eval(num)
    endnum = startnum - 10

    n = startnum
    while n >= endnum:
        adict = dict()
        adict["A_ID"] = ID + "-" + str(n)
        adict["ARM_In"] = ID
        # print("===="+adict["A_ID"])
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
        
        # print(items[32].text)
        adict["A_Name"] = items[32].text
        # print(items[33].text[0:-30])
        adict["A_Information"] = items[33].text[0:-30]
        # exit()
        n = n -1
        if adict["A_Name"] != "":
            jsondata = json.dumps(adict, ensure_ascii=False)
            with open("museum_spider/activities/A"+adict["A_ID"]+".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
        else:
            # print("空")
            pass 


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
        res.encoding = 'gbk'
        # open("temp.html",'w',encoding='gbk').write(res.content.decode('gbk','ignore'))
        # html = open("temp.html",'r',encoding='gbk').read()
        html = res.text
        
    except requests.RequestException as e:
        print(e)

    return html




if __name__ == "__main__":
    # getMuseumData()
    getCollectionsData()
    # getActivitiesData()
