# -*- coding:utf-8 -*- 
import sys
import xlrd
import time
import json
from bs4 import BeautifulSoup
import requests

header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", \
		'Connection': 'close'}

recipefile = "recipe.xlsx"

recipelist = []
itemset = {}

def loadRecipe():
    tables = xlrd.open_workbook(recipefile)
    # ['名称', '类型', '职业', '等级', '星级', '秘籍', '材料1', '数量1',
    #  '材料2', '数量2', '材料3', '数量3', '材料4', '数量4', '材料5',
    #  '数量5', '材料6', '数量6', '材料7', '数量7']
    mindex = [6,8,10,12,14,16,18]
    for sheet in tables.sheets():
        for row in range(1,sheet.nrows):
            # load recipe
            recipe = sheet.row_values(row)
            if len(recipe[0]) == 0:
                continue
            recipe_id = len(recipelist)
            recipelist.append(recipe)

            # add product to itemset
            product = recipe[0]
            if product in itemset:
                if 'recipe' in itemset[product]:
                    itemset[product]['recipe'].append(recipe_id)
                else:
                    itemset[product]['recipe'] = [recipe_id]
            else:
                itemset[product] = {
                    'id'        : len(itemset),
                    'name'      : product,
                    'recipe'    : [recipe_id]
                }
            
            # add materials to itemset
            for i in mindex:
                item = recipe[i]
                if len(item) == 0:
                    continue
                if item not in itemset:
                    itemset[item] = {
                        'id'    : len(itemset),
                        'name'  : item
                    }

    # print(itemset)
    print(len(recipelist), len(itemset))

def handleShop(item):
    print("shop", item)
    # tmp = soup.find_all('span', class_="mw-headline")
    # print(tmp)
    # req = requests.get(url, headers=header)
    # soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup)


def handleGather(item):
    print("Gather", item)

def handleEmployee(item):
    print("Employee", item)

handlers = {
    "通过商店购买"      : handleShop,
    "通过采集获得"      : handleGather,
    "通过雇员探险获得"  : handleEmployee,
}

def fetchDetail(item):
    req_prefix = "https://ff14.huijiwiki.com/wiki/物品:"

    filters = {"物品信息","任务奖励","理符任务奖励","用于任务","用于制作"}
    req = requests.get(req_prefix + item, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup)
    # infos = soup.find_all('li', class_='toclevel-1')
    infos = soup.find_all('span', class_='mw-headline')
    for info in infos:
        # type = info.find(class_='toctext').text
        type = info.text
        if type in filters:
            continue
        # href = info.find('a')['href']
        if type not in handlers:
            print(type, item)
            raise Exception("Unknown source")
        handlers[type](item)
    # print(infos)

def handleUnknown():
    cnt = 0
    fetchDetail("枫木原木")
    # for item in itemset.keys():
    #     if 'recipe' not in itemset[item]:
    #         fetchDetail(item)
            
    #         cnt += 1
    #         if cnt > 1:
    #             break


if __name__ == "__main__":
    loadRecipe()
    handleUnknown()