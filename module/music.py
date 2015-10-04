#!/usr/bin/env python

import sql_conf
import pymysql.cursors
import pprint

MUSIC_ID    = 0
AUTHOR      = 1
NAME        = 2
INTRO       = 3
LINK        = 4
EXT_INFO    = 5

class musicModule(object):
    def __init__(self):
        self.connect = pymysql.connect(host = sql_conf.sql_host,
                                       user = sql_conf.sql_user,
                                       password = sql_conf.sql_pswd,
                                       db = sql_conf.sql_database)
        return
    def __del__(self):
        return
    def getRandomMusicList(self, count = 1):
        '''
        with self.connect.cursor() as cursor:
            sql_cmd = ''
            cursor.execute(sql_cmd)
        self.connection.commit()

        with self.connect.cursor() as cursor:
            sql_cmd = ''
            cursor.execute(sql_cmd)
            result = cursor.fetchone()
            print(result)
        '''
        with self.connect.cursor() as cursor:
            cursor.execute("set names utf8")
            """
            sql_cmd = ("SELECT * FROM %s WHERE music_id >= "
                      "(SELECT floor(RAND() * (SELECT MAX(music_id) FROM %s))) "
                      "ORDER BY music_id LIMIT %s" % (sql_conf.sql_music_table_name,
                                                      sql_conf.sql_music_table_name,
                                                      count))
                                                      """
            sql_cmd = ("SELECT * FROM %s ORDER BY RAND() LIMIT %s" % (sql_conf.sql_music_table_name,
                                                                      count))
            cursor.execute(sql_cmd)
            result = cursor.fetchall()
            list_result = []
            for row in result:
                row_list = []
                for field in row:
                    if isinstance(field, str):
                        new_field = field.decode('utf-8')
                    else:
                        new_field = field
                    row_list.append(new_field)
                list_result.append(row_list)
            #pprint.pprint(list_result)
            #map(lambda li: map(lambda x: print(x.decode('utf-8')), li), list_resut)
            return list_result
    def addMusic(self, author, name, intro, link, ext_info):
        return
    def modMusic(self, music_id, author, name, intro, link, ext_info):
        return
    def delMusic(self, music_id):
        return
    def getMusict(self, item_id):
        return

if __name__ == "__main__":
    mu = musicModule()
    mu.getRandomMusicList(3)
    mu.getRandomMusicList(1)
