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

    resp = make_response( redirect(burl+'genportf?step=2') )
    try:
        if acm == None:
            asset_class = '%%'
        else:
            asset_class = acm
        if user_is_login() == 1:
            connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT symbol_list.uid FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE instruments.symbol NOT LIKE '%"+ get_portf_suffix() +"%' AND (instruments.y1_signal > 0 AND instruments.m6_signal > 0 AND instruments.m3_signal > 0 AND instruments.m1_signal > 0) AND (instruments.asset_class LIKE '"+ asset_class +"' OR instruments.market LIKE '"+ asset_class +"') ORDER BY RAND() LIMIT 5"
            print(sql)
            cr.execute(sql)
            rs = cr.fetchall()
            i = 1
            for row in rs:
                resp.set_cookie('portf_s_'+str(i), str(row[0]), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                resp.set_cookie('portf_s_'+str(i)+'_conv', str('neutral'), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                resp.set_cookie('portf_s_'+str(i)+'_type', str('long/short'), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                i += 1
            if i < 5:
                sql = "SELECT symbol_list.uid FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
                "WHERE instruments.symbol NOT LIKE '%"+ get_portf_suffix() +"%' AND (instruments.y1_signal > 0) AND "+\
                "(instruments.asset_class LIKE '"+ asset_class +"' OR instruments.market LIKE '"+ asset_class +"') ORDER BY RAND() LIMIT 5"
                print(sql)
                cr.execute(sql)
                rs = cr.fetchall()
                for row in rs:
                    resp.set_cookie('portf_s_'+str(i), str(row[0]), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                    resp.set_cookie('portf_s_'+str(i)+'_conv', str('weak'), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                    resp.set_cookie('portf_s_'+str(i)+'_type', str('long/short'), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                    i += 1
            if i < 5:
                add_additional_asset = "FX:"
                sql = "SELECT symbol_list.uid FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
                "WHERE instruments.symbol NOT LIKE '%"+ get_portf_suffix() +"%' AND (instruments.y1_signal > 0 AND instruments.m6_signal > 0 AND instruments.m3_signal > 0 ) AND "+\
                "(instruments.asset_class LIKE '"+ add_additional_asset +"') ORDER BY RAND() LIMIT 5"
                print(sql)
                cr.execute(sql)
                rs = cr.fetchall()
                for row in rs:
                    resp.set_cookie('portf_s_'+str(i), str(row[0]), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                    resp.set_cookie('portf_s_'+str(i)+'_conv', str('weak'), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                    resp.set_cookie('portf_s_'+str(i)+'_type', str('long/short'), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
                    i += 1


    except Exception as e: print(e)
    return resp

def gen_portf_validate_content(burl):

    resp = make_response( redirect(burl+'?dashboard=1&pop=1') )
    try:
        portf_symbol = portf_insert_data()
        generate_portfolio(portf_symbol)
    except Exception as e: print(e)
    return resp
