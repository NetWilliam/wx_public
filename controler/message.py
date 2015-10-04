# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import pylibmc
from common import templates_root,myTOKEN

class GetMessage:
    def __init__(self,data):
        self.signature=data.signature
        self.timestamp=data.timestamp
        self.nonce    =data.nonce
        self.echostr  =data.echostr
    
    def is_from_weixin(self):
        #字典序排序
        list=[myTOKEN,self.timestamp,self.nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        #sha1加密算法 
        hashcode=sha1.hexdigest()
        return hashcode == self.signature       
        
class PostMessage:
    def __init__(self,xmlMsg):
        self.render = web.template.render(templates_root)
        self.xml = etree.fromstring(xmlMsg)#进行XML解析
        
        self.msgType=self.xml.find("MsgType").text
        self.fromUser=self.xml.find("FromUserName").text
        self.toUser=self.xml.find("ToUserName").text
        #用字典替代switch
        {
          'text'    : self.parse_text ,
          "image"   : self.parse_image ,
          "voice"   : self.parse_voice,
          "video"   : self.parse_video,
          "location": self.parse_location,
          "link"    : self.parse_link,
        }[self.msgType]()

        #self.get
       
    #<xml>
    #<ToUserName><![CDATA[toUser]]></ToUserName>
    #<FromUserName><![CDATA[fromUser]]></FromUserName> 
    #<CreateTime>1348831860</CreateTime>
    #<MsgType><![CDATA[text]]></MsgType>
    #<Content><![CDATA[this is a test]]></Content>
    #<MsgId>1234567890123456</MsgId>
    #</xml>   
    def parse_text(self):
        self.content=self.xml.find("Content").text
  
    #<xml>
    #<ToUserName><![CDATA[toUser]]></ToUserName>
    #<FromUserName><![CDATA[fromUser]]></FromUserName>
    #<CreateTime>1348831860</CreateTime>
    #<MsgType><![CDATA[image]]></MsgType>
    #<PicUrl><![CDATA[this is a url]]></PicUrl>
    #<MediaId><![CDATA[media_id]]></MediaId>
    #<MsgId>1234567890123456</MsgId>
    #</xml>  
    def parse_image(self):
        self.picUrl=self.xml.find("PicUrl").text
        self.mediaId=self.xml.find("MediaId").text
    
    #<xml>
    #<ToUserName><![CDATA[toUser]]></ToUserName>
    #<FromUserName><![CDATA[fromUser]]></FromUserName>
    #<CreateTime>1357290913</CreateTime>
    #<MsgType><![CDATA[voice]]></MsgType>
    #<MediaId><![CDATA[media_id]]></MediaId>
    #<Format><![CDATA[Format]]></Format>
    #<MsgId>1234567890123456</MsgId>
    #</xml>        
    def parse_voice(self):
        self.format=self.xml.find("Format").text
        self.mediaId=self.xml.find("MediaId").text
    
    #<xml>
    #<ToUserName><![CDATA[toUser]]></ToUserName>
    #<FromUserName><![CDATA[fromUser]]></FromUserName>
    #<CreateTime>1357290913</CreateTime>
    #<MsgType><![CDATA[video]]></MsgType>
    #<MediaId><![CDATA[media_id]]></MediaId>
    #<ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
    #<MsgId>1234567890123456</MsgId>
    #</xml>
    def parse_video(self):
        self.thumbMediaId=self.xml.find("ThumbMediaId").text
        self.mediaId=self.xml.find("MediaId").text
    
    #<xml>
    #<ToUserName><![CDATA[toUser]]></ToUserName>
    #<FromUserName><![CDATA[fromUser]]></FromUserName>
    #<CreateTime>1351776360</CreateTime>
    #<MsgType><![CDATA[location]]></MsgType>
    #<Location_X>23.134521</Location_X>
    #<Location_Y>113.358803</Location_Y>
    #<Scale>20</Scale>
    #<Label><![CDATA[位置信息]]></Label>
    #<MsgId>1234567890123456</MsgId>
    #</xml>     
    def parse_location(self):
        self.location_X=self.xml.find("Location_X").text
        self.location_Y=self.xml.find("Location_Y").text   
        self.scale=self.xml.find("Scale").text   
        self.label=self.xml.find("Label").text   
    
    #<xml>
    #<ToUserName><![CDATA[toUser]]></ToUserName>
    #<FromUserName><![CDATA[fromUser]]></FromUserName>
    #<CreateTime>1351776360</CreateTime>
    #<MsgType><![CDATA[link]]></MsgType>
    #<Title><![CDATA[公众平台官网链接]]></Title>
    #<Description><![CDATA[公众平台官网链接]]></Description>
    #<Url><![CDATA[url]]></Url>
    #<MsgId>1234567890123456</MsgId>
    #</xml> 
    def parse_link(self):
        self.title=self.xml.find("Title").text
        self.description=self.xml.find("Description").text
        self.url=self.xml.find("Url").text

    def reply_text(self,content):
        return self.render.reply_text(self.fromUser,self.toUser,int(time.time()), content)
        
