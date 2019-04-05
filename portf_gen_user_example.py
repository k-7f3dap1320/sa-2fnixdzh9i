# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import Flask, make_response, request, redirect
from sa_db import *
from sa_func import *
from app_cookie import *
from portf_save import *
from portf_gen_data import *

access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def gen_portf_user_example(burl,acm):

    resp = make_response( redirect(burl+'?dashboard=1&pop=1') )
    try:
        if acm == 'MA:':
            asset_class = '%%'
        else:
            asset_class = acm
        if user_is_login() == 1:
            connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT symbol_list.uid FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE instruments.asset_class LIKE '"+ asset_class +"' OR instruments.market LIKE '"+ asset_class +"' ORDER BY RAND()"
            print(sql)
            cr.execute(sql)
            rs = cr.fetchall()
            i = 1
            for row in rs:
                resp.set_cookie('portf_s_'+str(i), str(row[0]), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                i += 1
            portf_symbol = portf_insert_data()
            generate_portfolio(portf_symbol)

    except Exception as e: print(e)
    return resp
