# -*- coding:utf-8 -*- 
import sys
import time
import json
from bs4 import BeautifulSoup
import requests

tmpfilename = "parser.tmp"


# 刻木 锻铁 铸甲 雕金 制革 裁衣 炼金 烹调
titlestr = [
    "%E5%88%BB%E6%9C%A8%E5%8C%A0%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8",
    "%E9%94%BB%E9%93%81%E5%8C%A0%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8",
    "%E9%93%B8%E7%94%B2%E5%8C%A0%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8",
    "%E9%9B%95%E9%87%91%E5%8C%A0%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8",
    "%E5%88%B6%E9%9D%A9%E5%8C%A0%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8",
    "%E8%A3%81%E8%A1%A3%E5%8C%A0%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8",
    "%E7%82%BC%E9%87%91%E6%9C%AF%E5%A3%AB%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8",
    "%E7%83%B9%E8%B0%83%E5%B8%88%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8"
]
jobstr = [
    "%E5%88%BB%E6%9C%A8%E5%8C%A0%7C",
    "%E9%94%BB%E9%93%81%E5%8C%A0%7C",
    "%E9%93%B8%E7%94%B2%E5%8C%A0%7C",
    "%E9%9B%95%E9%87%91%E5%8C%A0%7C",
    "%E5%88%B6%E9%9D%A9%E5%8C%A0%7C",
    "%E8%A3%81%E8%A1%A3%E5%8C%A0%7C",
    "%E7%82%BC%E9%87%91%E6%9C%AF%E5%A3%AB%7C",
    "%E7%83%B9%E8%B0%83%E5%B8%88%7C"
]
levelstr = ["1-5","6-10","11-15","16-20","21-25","26-30","31-35","36-40","41-45",\
            "46-50","51-55","56-60","61-65","66-70","71-75","76-80","81-85","86-90"]

            # 50*, 50**, 50***, 50****
starstr = ["50%E2%98%851","50%E2%98%852","50%E2%98%853","50%E2%98%854",\
            "60%E2%98%851","60%E2%98%852","60%E2%98%853","60%E2%98%854",\
            "70%E2%98%851","70%E2%98%852","70%E2%98%853","70%E2%98%854",\
            "80%E2%98%851","80%E2%98%852","80%E2%98%853","80%E2%98%854",\
            "90%E2%98%851"]
# starname = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1]

            # 第一到第八卷
bookstr = ["%E7%AC%AC%E4%B8%80%E5%8D%B7","%E7%AC%AC%E4%BA%8C%E5%8D%B7",\
            "%E7%AC%AC%E4%B8%89%E5%8D%B7","%E7%AC%AC%E5%9B%9B%E5%8D%B7",\
            "%E7%AC%AC%E4%BA%94%E5%8D%B7","%E7%AC%AC%E5%85%AD%E5%8D%B7",\
            "%E7%AC%AC%E4%B8%83%E5%8D%B7","%E7%AC%AC%E5%85%AB%E5%8D%B7",\
            # 半魔之卷
            "%E5%8D%8A%E9%AD%94%E4%B9%8B%E5%8D%B7"]
bookname = ["第一卷","第二卷","第三卷","第四卷","第五卷","第六卷","第七卷","第八卷","半魔之卷"]

req_prefix = "https://cdn.huijiwiki.com/ff14/api.php?format=json&action=parse&\
    disablelimitreport=true&prop=text&\
    title=%E5%88%BB%E6%9C%A8%E5%8C%A0%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8&\
    text=%7B%7B%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8%7C\
    job=%E5%88%BB%E6%9C%A8%E5%8C%A0%7C\
    level="

req_suffix = "%7D%7D&version=6.00.1&smaxage=864000&maxage=864000"

header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", \
		'Connection': 'close'}

def request(jobid, level, bookid = None):
    reqstr = req_prefix + "title=" + titlestr[jobid] \
            + "&text=%7B%7B%E9%85%8D%E6%96%B9%E5%88%97%E8%A1%A8%7Cjob=" \
            + jobstr[jobid] + "level=" + level \
            + req_suffix
    req = requests.get(reqstr,headers=header)
    # print(req.text)
    parse(req.text, bookid=bookid)

# item format: name, type, level, mlist
itemlist = []

filters = ("冰之碎晶","冰之水晶","冰之晶簇",\
        "水之碎晶","水之水晶","水之晶簇",\
        "火之碎晶","火之水晶","火之晶簇",\
        "土之碎晶","土之水晶","土之晶簇",\
        "风之碎晶","风之水晶","风之晶簇",\
        "雷之碎晶","雷之水晶","雷之晶簇")

def parse(resp, bookid=None):
    jsondata = json.loads(resp)['parse']['text']['*']
    with open(tmpfilename, "w") as tmpfile:
        tmpfile.write(jsondata)
        tmpfile.close()
    # print(jsondata)

    star = "0"
    book = ""
    if bookid != None:
        book = bookname[bookid]
    
    with open(tmpfilename, "r") as tmpfile:
        soup = BeautifulSoup(tmpfile, features='html.parser')
        rawitemlist = soup.find_all(class_="tabber-item")
        print("Totally", len(rawitemlist), "items")
        for rawitem in rawitemlist:
            
            type = rawitem['data-kind']
            name = rawitem.find_all('div', class_='item-baseinfo')[0].find(class_='item-name').text
            leveltmp = rawitem.find_all('span', class_='jp')[0].text[2:]
            tmpstrs = leveltmp.split(" ")
            level = tmpstrs[0]
            if len(tmpstrs) > 1:
                star = str(len(tmpstrs[1]))

            # name, type, level, star, book, metarials...
            item = [name, type, level, star, book]
            # print(rawitem.find_all('span', class_='item-baseinfo'))
            materials = rawitem.find_all('div', class_='item-recipe--material')
            for m in materials:
                mname = m.find('span', class_='item-name')
                if mname == None or mname.text in filters:
                    continue
                mnum = m.find('span', class_='item-number')
                if mnum == None:
                    continue
                item.append(mname.text)
                item.append(mnum.text[2:])
            itemlist.append(item)
        tmpfile.close()

def writedata(file):
    with open(file, "a") as outfile:
        for item in itemlist:
            str = ','.join(item)
            # print(str)
            outfile.write(str + u'\n')
        outfile.close()

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python ./parsefromwiki.py <result file")
    else:
        datafile = str(sys.argv[1])
        job = 7
        for level in levelstr:
            request(job, level)
            time.sleep(0.5)
        for star in starstr:
            request(job, star)
            time.sleep(0.5)
        for bookid in range(0,len(bookstr)):
            request(job, bookstr[bookid], bookid=bookid)
            time.sleep(0.5)
        writedata(datafile)
        # request(0, bookstr[0], bookid=0)
    # request(0,0)