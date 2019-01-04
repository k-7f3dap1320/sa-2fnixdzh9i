# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
import string
import random

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_portf_suffix():
    return 'PRF:'

def get_uid(s):

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT uid FROM symbol_list WHERE symbol = '"+s+"'"
        cr.execute(sql)
        rs = cr.fetchall()
        uid = 0
        for row in rs:
            uid = row[0]
        cr.close()
        connection.close()
    except Exception as e: print(e)

    return uid

def get_random_str(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def get_selected_lang():
    return 'en'

def get_pct_change(ini_val,new_val):

    if not new_val == 0:
        if new_val < ini_val:
            r =  ( (ini_val - new_val) / ini_val ) * (-1)
        else:
            r = (new_val - ini_val) / new_val
    else:
        r = 0

    return r
