import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
import json

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        print("状态码错误")

def getUrlList(lst, newsURL):#获得url链接保存到列表
    html = getHTMLText(newsURL)
    soup = BeautifulSoup(html, 'html.parser') 
    a = soup.find_all('a')
    for i in a:
        try:
            global new_list
            new_list = []
            href = i.attrs['href']
            lst.append(re.findall(r"./\d{6}/t\d{8}_\d{5}\.html", href)[0])
        except:
            continue
    for j in lst:
        k = "http://www.jb.mil.cn/zxdt/" + j[2:]
        new_list.append(k)
    #print(lst)
    #print(new_list)
            
def getText(url):
    try:
        html = getHTMLText(url)
        topic = etree.HTML(html)
        texts = topic.xpath('/html/body/div[4]/div/div//text()')
        texts = ''.join(texts)
        try:
            #with open("故宫博物馆.json","a+") as write_f:
             #   json.dump(texts,write_f,indent=4,ensure_ascii=False)
            jsondata = json.dumps(texts,indent=4,ensure_ascii=False)
            f = open("中国人民革命军事博物馆.json","a+",encoding="utf-8")
            f.write(jsondata)  #追加写模式，每次运行若不删除“中国人民革命军事博物馆.json”文档则内容会重复
            f.close()
            #print("文件已生成")
        except:
            print("文件未生成")
        print(texts)
    except:
        print("出错了")
    
def main():
    start_url = 'http://www.jb.mil.cn/zxdt/'
    slist = []
    for i in range(49):  #共50个页面
        if i==0:
            url = start_url
        else:
            url = start_url + "index_" + str(i) + ".html"
        html = getHTMLText(url)
        getUrlList(slist,url)
    for l in new_list:
        getText(l)

if __name__ == "__main__":
    main()
    #f=open("军事博物馆.json")
    #print(f.readline())
    #f.close()
    
