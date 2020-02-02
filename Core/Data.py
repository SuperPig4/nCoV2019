#!/usr/bin/python3
#coding:utf-8

'''
    获得流感数据
'''

import sqlite3
import requests
import time
import hashlib
import json
from . import Ulits
from .Email import Main as EmailMain, QQ as EmailQQ

# 获得数据
def get() :
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(round(time.time() * 1000))
    result = requests.get(url)
    if result.status_code != 200 :
        raise Exception("http code %s" % result.status_code, 1001)
    
    resultJson = result.json()
    info = json.loads(resultJson['data'])

    # 判断是否重复
    md5Handle = hashlib.md5()
    # md5Handle.update(json.dumps(info['chinaTotal']).encode(encoding='utf-8'))
    md5Str = str(info['chinaTotal']['confirm'] + info['chinaTotal']['suspect'] + info['chinaTotal']['dead'] + info['chinaTotal']['heal'])
    md5Handle.update(md5Str.encode(encoding='utf-8'))
    md5 = md5Handle.hexdigest()
    
    db = Ulits.DBTool()
    dataIsAdd = db.executeQuery("SELECT * FROM info WHERE md5=?" ,(md5,))
    if len(dataIsAdd.fetchall()) > 0 :
        db.close()
        raise Exception("data repeat", 1002)
    
    if db.executeUpdate("INSERT INTO INFO (info, md5, create_time) \
    VALUES (?,?,?)", [(result.text, md5, time.time())]) == False :
        db.close()
        raise Exception("data insert fail", 1003)
    
    db.close()
    return True


# 发送
def send() :
    # 获得最新info
    db = Ulits.DBTool()
    fetch = db.executeQuery("SELECT * FROM info order by id desc limit 1",())
    info = fetch.fetchall()
    raise Exception("data empty", 1004)
    if (len(info) > 0) == False :
        raise Exception("data empty", 1004)
    elif info[0][5] != 0 :
        raise Exception("repeat send", 1005)
    
    info = info[0]
    infoContent = json.loads(info[1])
    infoContent = json.loads(infoContent['data'])
    # print(type(infoContent['data']))
    # print(infoContent['chinaTotal'])

    # 获得所有邮件
    fetch = db.executeQuery("SELECT * FROM emails where is_notice == 1",())

    QQ = EmailQQ.QQClass()
    email = EmailMain.MainClass()
    email.set_entity(QQ)

    # 处理发送内容
    htmlFp = open('Core/Email/Template/index.html','r',encoding='utf-8')
    html = htmlFp.read()
    htmlFp.close()

    chinaTotal = infoContent['chinaTotal']
    html = html.replace('{{confirm}}', str(chinaTotal['confirm']))
    html = html.replace('{{suspect}}', str(chinaTotal['suspect']))
    html = html.replace('{{cure}}', str(chinaTotal['heal']))
    html = html.replace('{{dead}}', str(chinaTotal['dead']))
    html = html.replace('{{time}}', str(infoContent['lastUpdateTime']))

    email.title = '新型冠状肺炎-最新动态'
    email.content = html

    logFailLog = []
    logTime = time.time()
    for row in fetch :
        if email.send(row[1]) :
            db.executeUpdate("UPDATE emails SET last_send_time = ? WHERE id =?", [(logTime, row[0])])
        else :
            logFailLog.append(row[0])

    # 更新标记
    db.executeUpdate("UPDATE info SET is_send = 1, send_time=? WHERE id =?", [(logTime, info[0])])
    db.close()
    
    if len(logFailLog) > 0 :
        return logFailLog
    else :
        return True

    



    
