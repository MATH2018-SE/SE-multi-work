# -*- coding: utf-8 -*-
"""
故宫博物院爬虫文件
@author: HofCY
@version 创建时间：2020.05.02
https://www.dpm.org.cn/Home.html
010101

代码更新：

2020.05.09
代码完成
2020.05.02
代码创建

"""


# 引入的包自行引入，不做要求
# 服务器自行伪装，不做要求

import requests
from bs4 import BeautifulSoup
import re
import json
from requests_html import HTMLSession
from urllib.parse import urlencode
from selenium import webdriver
import socket
import urllib.request
from urllib import error



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
    datadict["M_ID"] = "010101"
    datadict["M_CName"] = "故宫博物院"
    datadict["M_EName"] = "The Palace Museum"
    datadict["M_Batch"] = 1
    datadict["M_Address"] = "北京市东城区景山前街4号"

    # 主页内容
    baseurl = "https://www.dpm.org.cn/Home.html"  # 要爬取的网页链接
    datadict["M_Web"] = baseurl
    html = askURL(baseurl)  # 保存获取到的网页源码
    # print(html[0:100])
    soup = BeautifulSoup(html, "html.parser")
    # open("../temp/Opening.html", 'w', encoding='utf-8').write(str(html))

    # 开放时间
    s = ""
    for item in soup.find_all('div', attrs={'class': 'li'}):
        s = s + str(item)
    # print(s)
    res = r'<h1>(.*?)</h1>'
    mm = re.findall(res, s, re.S | re.M)
    # print(mm)
    time = mm[0] + "-" + mm[1] + "-" + mm[2] + "-" + mm[3]
    # print(time)
    datadict["M_OpeningTime"] = time

    # logo
    for w in soup.find_all('div', attrs={'class': 'logo'}):
        w = str(w)
        # print(w)
        findlogo = r'src="(.*?)"'
        logo = re.findall(findlogo, w)
        # (logo)
        datadict["M_Logo"] = logo


    # 开放时信息
    url = 'https://www.dpm.org.cn/Visit.html#block6'
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    s = ""
    for item in soup.find_all('div', attrs={'class': 'block3'}):
        s = s + str(item)
    # print(s)
    res = r'<p>(.*?)</p>'
    mm = re.findall(res, s, re.S | re.M)
    mm = str(mm[0])
    a = re.compile(r'<[^>]+>', re.S)
    mm = a.sub("", mm)
    # print(mm)
    res1 = r'<h2>(.*?)</h2>'
    mm1 = re.findall(res1, s, re.S | re.M)
    # print(mm1)
    OpeningInformation = mm + mm1[1] + "。" + mm1[2] + "。"
    # print(OpeningInformation)
    datadict["M_OpeningInformation"] = OpeningInformation


    # introduction
    session = HTMLSession()
    url = 'https://www.dpm.org.cn/about/about_view.html'
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    r = session.get(url)
    s = ""
    for item in r.html.find('div.body'):
        item = item.text
        # print(item)
        item = item.split('\n')
    cp = re.findall(r'[0-9]', item[9])
    cpsl = ""
    for c in cp:
        cpsl = cpsl + str(c)
    # print(cpsl)
    text1 = item[2] + item[3] + "。" + item[4] + item[5] + "\n" + "故宫博物院拥有" + cpsl + "件藏品，" + item[10] + item[11] + "。" + item[13] + "\n"
    text2 = item[16] + item[17] + "\n"
    text3 = item[19] + "\n"
    text4 = ""
    for i in range(20, 28):
        if i % 2 == 0:
            text4 = text4 + item[i] + ":"
        else:
            text4 = text4 + item[i] + "。\n"
    text5 = ""
    for i in range(28, 33):
        text5 = text5 + item[i]
    text6 = "\n" + item[35] + "\n" + item[41] + item[42] + item[43] + "\n" + item[45] + item[46] + "。" + "\n"
    new_text = text1 + text2 + text3 + text4 + text5 + text6
    # print(new_text)
    datadict["M_Introduction"] = new_text

    # 图片
    for pic in soup.find_all('div', attrs={'class': 'ld_over_4'}):
        pic = pic.find_all('div', attrs={'class': 'img'})
        res = r'src="(.*?)"'
        pic = str(pic)
        pic = re.findall(res, pic)
        # print(pic)
    datadict["M_Pictures"] = pic


    # 门票
    session = HTMLSession()
    url = 'https://www.dpm.org.cn/Visit.html#block4'
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    r = session.get(url)
    s = ""
    for T in soup.find_all('div', attrs={'id': 'ticket'}):
        s = s + str(T)
    # print(s)
    res = r'<li>(.*?)</li>'
    xx = re.findall(res, s, re.S | re.M)
    # print(xx)
    datadict["M_Ticket"] = xx
    res1 = r'<span .*?>(.*?)</span>'
    yh = re.findall(res1, s, re.S | re.M)
    res2 = r'<li .*?>(.*?)</li>'
    # print(yh)
    yhc = re.findall(res2, s, re.S | re.M)
    # print(yhc)
    yhc1 = ""
    yhc2 = ""
    for i in range(0, 20):
        if i < 10:
            yhc1 = yhc1 + str(yhc[i]) + "\n"
        else:
            yhc2 = yhc2 + str(yhc[i]) + "\n"
    # print(yhc1)
    # print(yhc2)
    TicketInformation = yh[2] + ":\n" + yhc1 + "\n" + yh[3] + ":\n" + yhc2 + "\n" + "故宫接待中小学生集体参观免票试行办法"
    # print(TicketInformation)
    for TI in soup.find_all('div', attrs={'class': 'text'}):
        TicketInformation = TicketInformation + TI.text
        # print(TicketInformation)
    datadict["M_TicketInformation"] = TicketInformation


    # 交通指南
    session = HTMLSession()
    url = 'https://www.dpm.org.cn/Visit.html#block5'
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    r = session.get(url)
    s = ""
    for T in soup.find_all('div', attrs={'class': 'list now'}):
        s = s + str(T)
    # print(s)
    del_label = re.compile(r'<[^>]+>', re.S)
    s = del_label.sub("", s)
    s = s.replace('\t', '').replace(' ', '')
    # print(s)
    s = s.split('\n')
    t = {}
    n = 0
    Triffic = ""
    for i in s:
        if i != '':
            t[n] = i
            # print(n)
            # print(t[n])
            if t[n] != "更多详细路线":
                Triffic = Triffic + t[n] + "\n"
            n = n + 1
    # print(Triffic)
    datadict["M_Triffic"] = Triffic

    jsondata = json.dumps(datadict, ensure_ascii=False, indent=4)
    with open("museum_spider/museums/M010101.json", 'w', encoding='utf-8') as f:
        f.write(jsondata)

def getCollectionsData():
    """
    获得博物馆藏品信息
    并生成数据字典
    先自行保存在一个位置
    :rtype: object
    """
    collectiondict = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
    }
    session = HTMLSession()
    url = 'https://www.dpm.org.cn/explore/collections.html'
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    web = ""
    for w in soup.find('div', attrs={'class': 'box'}):
        web = web + str(w)
    # print(web)
    findlink = r'<a href="(.*?)"'
    link = re.findall(findlink, web)
    # print(link)
    web = link[0:23]
    # print(web)
    web1 = 'http://www.dpm.org.cn'
    i = 0
    for lb in web:
        i = i + 1
        # print(i)
        # print(a)
        lb = lb.replace('collection', 'searchs')
        # print(a)
        # if i == 2:
            # break
        # 调试不同藏品类别
        baseurl = web1 + str(lb) + "?"  # 编辑不同类别藏品的基础网址
        # print(baseurl)
        parameters = {
            "category_id": 90,
            "p": 1
        }  # 用于爬取总页数的参数
        clink = baseurl + urlencode(parameters)
        # print(clink)
        html = askURL(clink)
        soup = BeautifulSoup(html, "html.parser")
        for w in soup.find_all('div', attrs={'class': 'pages'}):
            w = str(w)
            # print(w)
            findpages = r'.html">(.*?)</a>'
            pages = re.findall(findpages, w)
            # print(pages)
            pages = pages[len(pages)-1]
            # print(pages)
        for page in range(1, int(pages) + 1):
            if page == 3:
                break
            # 控制调试页码
            # 藏品过多，每类选取部分爬取
            parameters = {
                "category_id": 90,
                "p": page
            }  # 参数
            clink = baseurl + urlencode(parameters)
            try:
                r = requests.get(clink, headers=headers)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                cphtml = r.text
            except:
                # print(clink)
                # print('链接失败')
                continue
            cpsoup = BeautifulSoup(cphtml, "html.parser")
            z = 0
            for cp in cpsoup.find_all('div', attrs={'class': 'table1'}):
                z = z + 1
                if z == 2:
                    break
                cp = str(cp)
                # print(cp)
                findid = r'id="(.*?)"'
                cidh = re.findall(findid, cp)
                # print(cidh)
                # findname = r'target="_blank">(.*?)<'
                # cnameh = re.findall(findname, cp)
                # print(cnameh)
                findlink = r'<a href="(.*?)"'
                clink = re.findall(findlink, cp)
                # print(clink)
                cpsl = 0
                for cid in cidh:
                    cpsl = cpsl + 1
                    # if cpsl == 2:
                    # break
                    cname = cpsoup.find_all('a', attrs={'id': cid})
                    cname = str(cname)
                    del_label = re.compile(r'<[^>]+>', re.S)
                    cname = del_label.sub("", cname)
                    cname = cname.replace('\n', '').replace(' ', '').replace(']', '').replace('[\r', '')
                    # print(cname)
                    cid = str(cid)
                    # print(cid)
                    cid = "010101-" + cid
                    # print(cid)
                    collectiondict["C_ID"] = cid
                    collectiondict["C_Name"] = cname
                    webc = web1 + clink[cpsl - 1]
                    r = session.get(webc)
                    aa = 0
                    try:
                        res = requests.get(webc, headers=headers)
                        res.raise_for_status()
                        res.encoding = res.apparent_encoding
                        webchtml = r.text
                    except:
                        # print(webc)
                        # print('链接失败')
                        continue
                    webcsoup = BeautifulSoup(webchtml, "html.parser")
                    for text in r.html.find('div.content_edit'):
                        aa = aa + 1
                        text = text.text
                        del_label = re.compile(r'<[^>]+>', re.S)
                        text = del_label.sub("", text)
                        text = text.replace('\u3000', '').replace(' ', '')
                        s = text.split('\n')
                        # print(s)
                        text = re.findall(r'(.*?)TAG标签耗时：', text)
                        if len(s) >= 2 and len(text) != 0:
                            s[len(s) - 1] = text[0]
                        elif len(s) == 1 and len(text) != 0:
                            s[len(s) - 1] = text[0]
                        # print(aa)
                        # print(text)
                        # print(s)
                    collectiondict["C_Introduction"] = s
                    for pic in webcsoup.find_all('div', attrs={'class': 'pic'}):
                        pic = str(pic)
                        # print(pic)
                        findpic = r'src="(.*?)"'
                        pic = re.findall(findpic, pic)
                        cpic = str(pic[0])
                        # print(cpic)
                        if cpic.find('https://img.dpm.org.cn') == -1:
                            cpic = 'https://img.dpm.org.cn' + cpic
                        # 如果网址不完全，就补充全
                        # print(cpic)
                    res.close()
                    collectiondict["C_Pictures"] = cpic
                    collectiondict["CRM_In"] = "010101"
                    '''if i == 1 and page == 1 and cpsl == 1:'''
                    jsondata = json.dumps(collectiondict, ensure_ascii=False, indent=4)
                    with open("museum_spider/collections/C" + collectiondict["C_ID"] + ".json", 'w', encoding='utf-8') as f:
                        f.write(jsondata)
                    '''else:
                        jsondata = json.dumps(collectiondict, ensure_ascii=False, indent=4)
                        with open("../collections/C" + collectiondict["C_ID"] + ".json", 'a', encoding='utf-8') as f:
                            f.write(jsondata)'''
            r.close()




pass

def getActivitiesData():
    """
    获得博物馆活动信息
    并生成数据字典
    先自行保存在一个位置
    """
    activityDict = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
    }

    # 展览
    baseurl = 'https://www.dpm.org.cn/searchs/exhibition.html?'
    browser = webdriver.Chrome()
    browser.minimize_window()
    for page in range(1, 21):
        if page == 2:
            break
        # 调试不同页码
        parameters = {
            "category_id": 169,
            "old_year": 1,
            "order_datetimes": 1,
            "showstype": 301,
            "pagesize": 12,
            "p": page
        }  # 参数
        aplink = baseurl + urlencode(parameters)
        # print(aplink)
        browser.get(aplink)
        browser.implicitly_wait(30)
        aphtml = browser.page_source
        # print(aphtml)
        apsoup = BeautifulSoup(aphtml, "html.parser")
        z = 0
        zsid = 0
        atime = apsoup.find_all('div', attrs={'class': 'desc'})
        for ap in apsoup.find_all('div', attrs={'class': 'img'}):
            z = z + 1
            # if z == 4:
                # break
            ap = str(ap)
            ap = ap.replace('\n', '')
            # print(ap)
            findlink = r'<a href="(.*?)"'
            alink = re.findall(findlink, ap)
            # print(alink)
            findname = r'title=(.*?)>'
            aname = re.findall(findname, ap)
            # print(aname[0])
            findid = r'exhibitShare/(.*?)$'
            aid = re.findall(findid, alink[0])
            if len(aid) != 0:
                aid = "010101-1-" + str(aid[0])
                # print(aid)
                activityDict["A_ID"] = aid
                activityDict["A_Name"] = aname[0]
                activityDict["A_Type"] = 1
                session = HTMLSession()
                r = session.get(alink[0])
                s = ""
                aaa = 0
                for text in r.html.find('div.text_info'):
                    aaa += 1
                    # print(aaa)
                    text = text.text
                    s = s + text
                    # print(s)
                    activityDict["A_Introduction"] = s
            else:
                zsid = zsid + 1
                aid = "010101-1-" + str(zsid)
                # print(aid)
                activityDict["A_ID"] = aid
                activityDict["A_Name"] = aname
                activityDict["A_Type"] = 1
                activityDict["A_Introduction"] = str(alink) + "，VR全景连接"
            time = str(atime[z-1])
            # print(time)
            time = time.replace(' ', '')
            findtime = r'</p><p>(.*?)<span'
            time = re.findall(findtime, time)
            # print(time[0])
            activityDict["A_Date"] = time[0]
            activityDict["ARM_In"] = "010101"
            '''if z == 1 and page == 1:'''
            jsondata = json.dumps(activityDict, ensure_ascii=False, indent=4)
            with open("museum_spider/activities/A" + activityDict["A_ID"] + ".json", 'w', encoding='utf-8') as f:
                f.write(jsondata)
            '''else:
                jsondata = json.dumps(activityDict, ensure_ascii=False, indent=4)
                with open("../activities/A" + activityDict["A_ID"] + ".json", 'a', encoding='utf-8') as f:
                    f.write(jsondata)'''

    browser.close()


    # 学术
    baseurl = 'https://www.dpm.org.cn/learning/dynamic.html?'
    browser = webdriver.Chrome()
    browser.minimize_window()
    for page in range(1, 6):
        # if page == 2:
            # break
        # 调试不同页码
        parameters = {
            "p": page
        }  # 参数
        aplink = baseurl + urlencode(parameters)
        # print(aplink)
        try:
            req = urllib.request.Request(aplink, None, headers=headers)
            response = urllib.request.urlopen(req, timeout=5)
            the_page = response.read()
        except socket.timeout as e:
            continue
        except error.HTTPError as e:
            continue
        # 防出错？
        browser.get(aplink)
        browser.implicitly_wait(30)
        aphtml = browser.page_source
        # print(aphtml)
        apsoup = BeautifulSoup(aphtml, "html.parser")
        z = 0
        for ap in apsoup.find_all('div', attrs={'id': 'lists'}):
            z = z + 1
            if z == 2:
                break
            ap = str(ap)
            ap = ap.replace('\n', '')
            # print(ap)
            findlink = r'href="(.*?)"'
            alink = re.findall(findlink, ap)
            # print(alink)
            adsl = 0
            for aurl in alink:
                adsl += 1
                # if adsl == 2:
                    # break
                if adsl % 2 != 0:
                    continue
                findid = r'detail/(.*?).html'
                aid = re.findall(findid, aurl)
                if len(aid) == 0:
                    continue
                aid = "010101-2-" + aid[0]
                # print(aid)
                aurl = 'https://www.dpm.org.cn/' + str(aurl)
                # print(aurl)
                session = HTMLSession()
                r = session.get(aurl)
                s = ""
                aaa = 0
                ahtml = askURL(aurl)
                # print(ahtml)
                asoup = BeautifulSoup(ahtml, "html.parser")
                aname = asoup.find('h1', attrs={'class': 'title2'})
                aname = str(aname)
                del_label = re.compile(r'<[^>]+>', re.S)
                aname = del_label.sub("", aname)
                aname = aname.replace('\r\n', '')
                # print(aname)
                activityDict["A_ID"] = aid
                activityDict["A_Name"] = aname
                activityDict["A_Type"] = 2
                for text in r.html.find('div.content_edit'):
                    aaa += 1
                    # print(aaa)
                    text = text.text
                    s = s + text
                s = s.replace('\n', '')
                # print(s)
                activityDict["A_Introduction"] = s
                atime = asoup.find_all('div', attrs={'class': 'inf'})
                time = str(atime)
                # print(time)
                time = del_label.sub("", time)
                # print(time)
                activityDict["A_Date"] = time
                activityDict["ARM_In"] = "010101"
                jsondata = json.dumps(activityDict, ensure_ascii=False, indent=4)
                with open("museum_spider/activities/A" + activityDict["A_ID"] + ".json", 'w', encoding='utf-8') as f:
                    f.write(jsondata)
    browser.close()



    # 教育
    baseurl = 'https://www.dpm.org.cn/activity/educations.html'
    browser = webdriver.Chrome()
    browser.minimize_window()
    for page in range(1, 12):
        if page == 2:
            break
        # 调试不同页码
        parameters = {
            "p": page
        }  # 参数
        aplink = baseurl + urlencode(parameters)
        # print(aplink)
        browser.get(aplink)
        browser.implicitly_wait(30)
        aphtml = browser.page_source
        # print(aphtml)
        apsoup = BeautifulSoup(aphtml, "html.parser")
        z = 0
        for ap in apsoup.find_all('div', attrs={'id': 'lists'}):
            z = z + 1
            if z == 2:
                break
            ap = str(ap)
            ap = ap.replace('\n', '')
            # print(ap)
            findlink = r'href="(.*?)"'
            alink = re.findall(findlink, ap)
            # print(alink)
            adsl = 0
            for aurl in alink:
                adsl += 1
                # if adsl == 2:
                    # break
                # if adsl % 2 != 0:
                    # continue
                findid = r'education/(.*?).html'
                aid = re.findall(findid, aurl)
                if len(aid) == 0:
                    continue
                aid = "010101-3-" + aid[0]
                # print(aid)
                aurl = 'https://www.dpm.org.cn/' + str(aurl)
                # print(aurl)
                session = HTMLSession()
                r = session.get(aurl)
                s = ""
                aaa = 0
                ahtml = askURL(aurl)
                # print(ahtml)
                asoup = BeautifulSoup(ahtml, "html.parser")
                aname = asoup.find('h1', attrs={'class': 'title1'})
                aname = str(aname)
                del_label = re.compile(r'<[^>]+>', re.S)
                aname = del_label.sub("", aname)
                # aname = aname.replace('\r\n', '')
                # print(aname)
                activityDict["A_ID"] = aid
                activityDict["A_Name"] = aname
                activityDict["A_Type"] = 3
                for text in r.html.find('div.article'):
                    aaa += 1
                    # print(aaa)
                    text = text.text
                    s = s + text
                s = s.replace('\n', '')
                # print(s)
                activityDict["A_Introduction"] = s
                atime = asoup.find_all('div', attrs={'class': 'inf'})
                time = str(atime)
                # print(time)
                time = del_label.sub("", time)
                # print(time)
                activityDict["A_Date"] = time
                activityDict["ARM_In"] = "010101"
                jsondata = json.dumps(activityDict, ensure_ascii=False, indent=4)
                with open("museum_spider/activities/A" + activityDict["A_ID"] + ".json", 'w', encoding='utf-8') as f:
                    f.write(jsondata)
    browser.close()





    pass


# 得到指定一个URL的网页内容
def askURL(url):
    # head = headers[0]
    head = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
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
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'
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