# -*- coding:utf-8 -*- 
import sys
import time
import json
from bs4 import BeautifulSoup
import requests

tmpfilename = "parser.tmp"

req_prefix = "https://cdn.huijiwiki.com/ff14/api.php?format=json&action=parse&\
    disablelimitreport=true&prop=text&title=QuestSearch&ver=6.00.1&smaxage=1000&maxage=1000&\
    text=%7B%7BItemSearch%7Cjob%3D0%7Ckind%3D6%7Ccategory%3D0%7Crarity%3D0%7Cversion%3D0"
req_suffix = "%7D%7D"

header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", \
		'Connection': 'close'}

def request(page):
    pagestr = ""
    if page > 1:
        pagestr = "%7Cpage%3D" + str(page)
    reqstr = req_prefix + pagestr + req_suffix
    req = requests.get(reqstr,headers=header)
    # print(req.text)
    parse(req.text)

# item format: name, type, href
itemlist = []

def parse(resp):
    jsondata = json.loads(resp)['parse']['text']['*']
    with open(tmpfilename, "w") as tmpfile:
        tmpfile.write(jsondata)
        tmpfile.close()
    # print(jsondata)
    
    with open(tmpfilename, "r") as tmpfile:
        soup = BeautifulSoup(tmpfile, features='html.parser')
        rawitemlist = soup.find_all("div", class_="item-baseinfo")
        print("Totally", len(rawitemlist), "items")
        for rawitem in rawitemlist:
            # print(rawitem)
            href = rawitem.find('a')
            name = href.text
            link = href['href']
            # print(href)
            type = rawitem.find_all('div', class_="item-category")[0].text
            # print(name, type, link)
            item = [name, type, link]
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
        for page in range(1,73):
            request(page)
            time.sleep(0.3)
        writedata(datafile)
    # request(0,0)