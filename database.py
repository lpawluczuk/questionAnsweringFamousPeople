#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import json
import dataset
import files
import re
import copy

def initDatabaseConnetion():
    db = dataset.connect('sqlite:///people.db')
    return db['people']

def getDatabaseDict():
    table = initDatabaseConnetion()
    return table.all()

def initDatabaseFromJSON(jsonFilePath):
    table = initDatabaseConnetion()
    with open(jsonFilePath) as data_file:  
        data = json.load(data_file)

    rows = {}
    for d in data:
        name = d['name'] 
        if name in rows:
            row = rows[name]
            if 'birth' not in row and d['isBirth']:
                row['birth'] = getDateFromJSON(d)
            elif 'death' not in row and not d['isBirth']:
                row['death'] = getDateFromJSON(d)
        else:
            rows[name] = getDBRecordFromJSON(d)

    for row in rows.values():
        if 'birth' not in row:
            row['birth'] = ""
        elif 'death' not in row:
            row['death'] = ""
        table.insert_many(rows.values())

def getDateFromJSON(jsonObject):
    url = jsonObject['url']
    url_temp = url[url.index('-')+1:] 

    day = url_temp[:url_temp.index('-')]
    month = url_temp[url_temp.index('-')+1:-5]

    date = ""
    if 'date' in jsonObject:
        date = day + "-" + month + "-" + jsonObject['date']
    return date

def getDBRecordFromJSON(jsonObject):
    # print "Inserting: ", jsonObject['name']
    dbRecord = dict(name=jsonObject['name'], desc=jsonObject['desc'])

    date = getDateFromJSON(jsonObject)

    if jsonObject['isBirth']:
        dbRecord['birth'] = date
    else:
        dbRecord['death'] = date
    return dbRecord

if __name__ == "__main__":
    initDatabaseFromJSON(sys.argv[1])


