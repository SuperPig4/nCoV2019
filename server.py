#!/usr/bin/python3
# -*- coding:utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib
import re
import time
from Core import Ulits

data = {'msg': '', 'code':0}
host = ('localhost', 8888)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        if '?' in self.path :
            queryString = urllib.parse.unquote(self.path.split('?',1)[1])
            params = urllib.parse.parse_qs(queryString)        
        else :
            params = {}

        # 添加邮箱
        if  '/add' in self.path:
            if ('email' in params) == False :
                data['msg'] = '请输入邮箱'
            elif Ulits.is_valid_email(params['email'][0]) == False :
                data['msg'] = '邮箱不合法'
            else :
                data['msg'] = 'ok'
                data['code'] = 1
                email = params['email'][0]
                db = Ulits.DBTool()
                dataIsAdd = db.executeQuery("SELECT * FROM emails WHERE email=?" ,(email,))
                if len(dataIsAdd.fetchall()) == 0 :
                    if db.executeUpdate("INSERT INTO emails (email, create_time) \
                        VALUES (?,?)", [(email, time.time())]) == False :
                        data['msg'] = '添加失败,请稍后重试'
                        data['code'] = 0
                db.close()
            self.wfile.write(json.dumps(data).encode())
            

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()