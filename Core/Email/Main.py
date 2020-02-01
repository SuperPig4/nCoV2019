#!/usr/bin/python3
#coding:utf-8

import os

class MainClass : 
    
    # 电子邮箱实体
    __emailEntity = None
    # 内容实体
    # __contentEntity = None
    # 标题
    title = 'title'
    # 内容
    content = 'content'

    def set_entity(self, emailEntity) :
        self.__emailEntity = emailEntity

    def send(self, to) : 
        self.__emailEntity.set_title(self.title)
        self.__emailEntity.set_content(self.content)
        return self.__emailEntity.send(to)
    
