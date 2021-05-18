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

def getUrlList(lst, newsURL):#列表保存的列表类型，里面存有链接；获得url链接
    html = getHTMLText(newsURL)
    soup = BeautifulSoup(html, 'html.parser') 
    a = soup.find_all('a')
    for i in a:
        try:
            global new_list
            new_list = []
            href = i.attrs['href']
            lst.append(re.findall(r"/activity/education/\d{6}\.html", href)[0])
        except:
            continue
    for j in lst:
        k = "https://www.dpm.org.cn" + j
        new_list.append(k)
    #print(lst)
    #print(new_list)
            
def getText(url):
    try:
        html = getHTMLText(url)
        topic = etree.HTML(html)
        texts = topic.xpath('/html/body/div[4]/div[3]/div//text()')
        texts = ''.join(texts)
        try:
            #with open("故宫博物馆.json","a+") as write_f:
             #   json.dump(texts,write_f,indent=4,ensure_ascii=False)
            jsondata = json.dumps(texts,indent=4,ensure_ascii=False)
            f = open("故宫博物馆.json","a+",encoding="utf-8")
            f.write(jsondata)  #追加写模式，每次运行若不删除“故宫博物馆.json”文档则内容会重复
            f.close()
            #print("文件已生成")
        except:
            print("文件未生成")
        print(texts)
    except:
        print("出错了")
    
def main():
    start_url = 'https://www.dpm.org.cn/activity/educations/p/'
    slist = []
    for i in range(10):  #共11个页面
        url = start_url + str(i) + ".html"
        html = getHTMLText(url)
        getUrlList(slist,url)
    for l in new_list:
        getText(l)

if __name__ == "__main__":
    count=0
    main()
    #f=open("故宫博物馆.json")
    #print(f.readline())
    #f.close()
    
