# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import pylibmc
from common import templates_root
from message import GetMessage,PostMessage

class Weixin:
    def GET(self):
        #获取输入参数
        data = web.input()
        msg = GetMessage(data)
        if msg.is_from_weixin():
            return msg.echostr
            
    def POST(self):
        str_xml = web.data() #获得post来的数据
        msg = PostMessage(str_xml)
        if msg.msgType == "text":
            return msg.reply_text(msg.content)