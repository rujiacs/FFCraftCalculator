# -*- coding:utf-8 -*- 
import sys
import time
import json
from bs4 import BeautifulSoup
import requests

itemindexfile = "itemindex.txt"

itemlist = []

# {'物品信息', '精选', '通过精选获得', '通过雇员探险获得', '用于制作', '用于理符任务',
#  '理符任务奖励', '怪物掉落', '通过兑换获得', '通过采集获得', '制作配方'}
source = set()

def loadItemList():
    with open(itemindexfile,'r') as indexfile:
        lines = indexfile.readlines()
        for line in lines:
            info = line.split(',')
            item = [info[0], info[1], info[2], ""]
            itemlist.append(item)
        # print("Totally", len(itemlist), "items")
        indexfile.close()


req_prefix = "https://ff14.huijiwiki.com"

header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", \
		'Connection': 'close'}

def fetchItemPage(url):
    req = requests.get(req_prefix + url, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    infos = soup.find_all('li', class_='toclevel-1')
    for info in infos:
        tag = info.find(class_='toctext').text
        # print(tag)
        source.add(tag)
    # print(source)
    # print(infos)

def fetchDetail():
    cnt = 0
    for item in itemlist:
        if cnt > 100:
            break
        fetchItemPage(item[2])
        time.sleep(0.1)
        cnt += 1
    print(source)


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python ./parsefromwiki.py <result file")
    else:
        datafile = str(sys.argv[1])
        loadItemList()
        fetchDetail()
