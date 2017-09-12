# -*- coding:utf-8 -*-
import httpclient
import random
import hashlib
import json
import sys

#sys.setdefaultencoding("utf-8")

url = 'openapi.youdao.com'
key = 'rR6Q4dsOPzU4B5EwoJ0LK6mXCIyBXeTQ'

def getParams(q,appKey,fromText,toText):
    salt = random.randint(0,9)
    source = (appKey + q + str(salt) + key).encode('utf-8')
    md5 = hashlib.md5(source)
    sign = md5.hexdigest()
    params = dict()
    params['q'] = q.encode('utf-8')
    params['from'] = fromText
    params['to'] = toText
    params['appKey'] = appKey
    params['salt'] = salt
    params['sign'] = sign.upper()
    return params

def getTranslation(q,appKey,fromText='auto',toText='auto'):
    params = getParams(q,appKey,fromText,toText)
    response = httpclient.post(url,params)
    items = list()
    if response.status == 200:
        items = getItemList(response.read())
    else:
        items.append(getItem('网络不给力，一会再试吧',''))
    if len(items) == 0:
        items.append(getEmptyItem())

    jsonBean = {}
    jsonBean['items'] = filter(lambda x: x is not None, items)
    return json.dumps(jsonBean)

def getItemList(json_str):

    data = json.loads(json_str)
    items = list()
    errorCode = data['errorCode'].encode('utf-8')
    basic = data.get('basic')
    if errorCode == '0' and basic:

        items.append(getPhonetic(basic))

        explains = basic.get('explains')
        if len(explains) == 0:
            items.append(getEmptyItem())

        else:
            for explain in explains:
                items.append(getItem(explain.encode('utf-8'),'简明释义'))

        webs = data['web']
        items.extend(getWebMean(webs))

        translation = data['translation']
        items.append(getItem(translation[0].encode('utf-8'), '翻译'))
        return items
    return list()

def getPhonetic(data):

    uk = data.get('uk-phonetic')
    us = data.get('us-phonetic')
    phonetic = ''
    if uk:
        phonetic += '英音：' + uk.encode('utf-8')

    if us:
        if (len(phonetic) > 0):
            phonetic += ' | '
        phonetic += '美音：' + us.encode('utf-8')

    if(len(phonetic) > 0):
        return getItem(phonetic,'发音')
    else:
        return None

def getWebMean(webs):
    if webs:
        items = list()
        for web in webs:
            values = web['value']
            valuesStr = ''
            if values:
                for value in values:
                    if (len(valuesStr) > 0):
                        valuesStr += ' , '
                    valuesStr += value
                items.append(getItem(valuesStr,'网络释义'))

        return items
    else:
        return None


def getEmptyItem():
    return getItem('木有结果','这个单词有点厉害，有道词典也查不出来啊')

def getItem(title,subtitle):
    if title:
        item = {}
        item['title'] = title
        item['subtitle'] = subtitle
        item['icon'] = getIcon()
        return item
    else:
        return None

def getIcon():
    icon = {}
    icon['path'] = 'icon.png'
    return icon

def query(q,appKey='6220a8c774fdb324'):
    str = getTranslation(q.decode('utf-8'),appKey)
    if str:
        print str
    return str

if __name__ == '__main__':
    print query('feabse')

