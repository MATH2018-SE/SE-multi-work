# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import sqlite3
import xlwt
from lxml import etree

def main():
    baseurl = "http://www.chnmuseum.cn/zx/gbxw/"
    #1.爬取数据
    datalist = getData(baseurl)
    savepath = ".\\中国国家博物馆.xls"
    #3.保存数据
    #saveData(savepath)
    
    #askURL("http://www.jb.mil.cn/zxdt/index_1.html")

#新闻详情链接的规则
findLink = re.compile(r'<a target="_blank" href="./(.*?)" title')    #创建正则表达式对象，表示规则（字符串模式）

#新闻标题
findTitle = re.compile(r'">(.*)</a>')

#新闻发布时间
findTime = re.compile(r'<span>(.*)</span>')

#爬取新闻文本
findContent = re.compile(r'<span>(.*?)</span>')


#爬取数据
def getData(baseurl):
    datalist=[]
    for i in range(0,1):      #调用获取页面信息的函数：4次
        if i == 0:
            url = baseurl + "index.shtml" 
        else:
            url = baseurl + "index_" + str(i) + ".shtml"
        html = askURL(url)      #保存获取到的网页源码

        #2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div',class_="gmg_nullb"):    #查找符合要求的字符串，形成列表
            #print(item)   #测试查看新闻item全部信息
            data = []    #保存一条新闻的所有信息
            item = str(item)
            #每一页每条新闻的详细的超链接
            link = re.findall(findLink, item)    #re库用来通过正则表达式查找指定字符串
            #print("http://www.whgmbwg.com/"+link)
            #print(link)
            for i in link:
                link = "http://www.chnmuseum.cn/zx/gbxw/"+str(i)
                #print(link)
                content = getContent(link)
                print (content)
    return datalist


#获取新闻内部内容
def getContent(conurl):
    html = askURL(conurl)    #解析新闻内部数据
    topic = etree.HTML(html)
    texts = topic.xpath('/html/body/div[3]//text()')    #通过xpath爬取新闻内容
    texts = ''.join(texts)    #将列表格式转换字符串
    #print(texts)
    
    return texts

#得到指定一个url的网页内容
def askURL(url):
    #模拟浏览器头部信息，向网页服务器发送消息
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49"}
    #用户代理表示告诉网页我们是什么类型的机器浏览器，本质上是告诉浏览器，我们可以接受什么水平的信息
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html=response.read().decode("utf-8")
        #print(html)
    except urllib.request.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        
    return html


#保存爬取内容（暂定）
def saveData(savepath):
    pass
    

if __name__ == "__main__":
    main()