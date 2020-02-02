#!/usr/bin/python3
#coding:utf-8

'''
    获得流感数据
'''

import sqlite3
import requests
import time
import hashlib
import os
import json
from . import Ulits
from .Email import Main as EmailMain, QQ as EmailQQ
import urllib

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

    if (len(info) > 0) == False :
        raise Exception("data empty", 1004)
    elif info[0][5] != 0 :
        raise Exception("repeat send", 1005)
    
    info = info[0]
    infoContent = json.loads(info[1])
    infoContent = json.loads(infoContent['data'])    

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

    # 距离上次新增
    confirmNew = 0
    suspectNew = 0
    cureNew = 0
    deadNew = 0

    # 获得最后一次get的数据
    fetch = db.executeQuery("SELECT * FROM info where id !=? order by id desc limit 1",(info[0],))
    oldInfo = fetch.fetchall()
    if len(oldInfo) > 0 :
        oldInfo = oldInfo[0]
        infoContent = json.loads(oldInfo[1])
        infoContent = json.loads(infoContent['data'])   
        oldChinaTotal = infoContent['chinaTotal']

        confirmNew = chinaTotal['confirm'] - oldChinaTotal['confirm']
        suspectNew = chinaTotal['suspect'] - oldChinaTotal['suspect']
        cureNew = chinaTotal['heal'] - oldChinaTotal['heal']
        deadNew = chinaTotal['dead'] - oldChinaTotal['dead']
    
    html = html.replace('{{confirm_new}}', str(confirmNew))
    html = html.replace('{{suspect_new}}', str(suspectNew))
    html = html.replace('{{cure_new}}', str(cureNew))
    html = html.replace('{{dead_new}}', str(deadNew))

    email.title = '新型冠状肺炎-最新动态'
    email.content = html

    logFailLog = []
    logSucLog = []
    logTime = time.time()

    # 获得所有邮件
    aes = Ulits.USE_AES()
    fetch = db.executeQuery("SELECT * FROM emails where is_notice == 1",())
    for row in fetch :
        # 生成取消链接
        cancelUrl = os.environ.get('DOMAIN_NAME')
        if cancelUrl == None :
            cancelUrl = 'https://gitee.com/first_pig/nCoV2019'
        else :
            cancelUrl = 'http://' + cancelUrl + '/cancel?html=1&code=' + urllib.parse.quote(aes.encrypt(row[1]))
        # 赋值定制内容
        email.content = html.replace('{{cancel_url}}', str(cancelUrl))
        try:
            if email.send(row[1]) :
                logSucLog.append(row[0])
            else :
                logFailLog.append(row[0])
        except Exception as identifier:
            logFailLog.append(row[0])

    # 更新用户信息
    if len(logSucLog) > 0 :
        db.executeUpdate(("UPDATE emails SET send_count = send_count + 1, last_send_time = ? WHERE id in (%s)" % ",".join(str(i) for i in logSucLog)), ([logTime],))

    # 更新标记
    db.executeUpdate("UPDATE info SET is_send = 1, send_time=? WHERE id =?", [(logTime, info[0])])
    db.close()
    
    if len(logFailLog) > 0 :
        return logFailLog
    else :
        return True

    



    
