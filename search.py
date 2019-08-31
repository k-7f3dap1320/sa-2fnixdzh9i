# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from app_head import *
from app_body import *
from app_page import *
from sa_func import *


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_search_result(q):

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT url FROM feed WHERE search LIKE '%"+ str(q) +"%'"
        cr.execute(sql)
        rs = cr.fetchall()
        url = ''
        c = ''

        for row in rs:
            url = row[0].replace('{burl}','')
            c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + str(url) + '" />') + get_body('','') )

        if c == '':
            c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=/?s=0" />') + get_body('','') )

        cr.close()
        connection.close()
    except Exception as e: print(e)
    return c
