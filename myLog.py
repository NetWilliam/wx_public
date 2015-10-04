#!/usr/bin/env python

import sys, logging
from wsgilog import WsgiLog

log_format      = "[%(asctime)s] %(filename)s:%(lineno)d(%(funcName)s): [%(levelname)s] %(message)s"
date_format     = "%Y-%m-%d %H:%M:%S "
tofile_flag     = True
file_name       = "log/wx_public.log"
split_interval  = "d"
backup_num      = 30


class Log(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(self, application,
                         logformat = log_format,
                         datefmt = date_format,
                         tofile = tofile_flag,
                         file = file_name,
                         interval = split_interval,
                         backups = backup_num)
