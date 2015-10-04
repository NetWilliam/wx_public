# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
import logging
from lxml import etree
import pylibmc
from common import templates_root
from message import GetMessage,PostMessage
from module import music

class Weixin:
    def __init__(self):
        self.logger = web.ctx.environ['wsgilog.logger']
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
            if msg.content == u"音乐":
                music_obj = music.musicModule()
                music_info = music_obj.getRandomMusicList(1)[0]
                '''
                if music_info[music.INTRO] == "" && music_info[music.EXT_INFO] == "":
                    return msg.reply_text(music_info[music.NAME] + "\n" + music_info[music.AUTHOR] + "\n" + music_info[music.LINK])
                else if music_info[music.INTRO] == "" && music_info[music.EXT_INFO] != "":
                '''
                print music_info
                return msg.reply_text(music_info[music.INTRO] + "\n" + music_info[music.NAME] + " " + music_info[music.AUTHOR] + "\n" + music_info[music.LINK] + "\n" + music_info[music.EXT_INFO])
                #return msg.reply_text("wujiangwange http://music.163.com/#/m/song?id=355981 yujiyujinairuohe")
            else:
                return msg.reply_text("只响应 '音乐'")
        else:
            return msg.reply_text("现在只能响应文字消息, 其他的待开发")
