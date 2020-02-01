#!/usr/bin/python3
#coding:utf-8

# 约束类

'''
    发送失败
    11001
'''

import abc
class Interfacex(metaclass=abc.ABCMeta):
    # 标题
    __title = 'title'
    # 内容
    __content = 'content'

    '''
        发送
        @param 
        @param to 接受方
    '''
    @abc.abstractmethod
    def send(self, to) :
        raise NotImplementedError

    def set_content(self, text) :
        self.__content = text
    
    def get_content(self) :
        return self.__content
    
    def set_title(self, text) :
        self.__title = text
    
    def get_title(self) :
        return self.__title