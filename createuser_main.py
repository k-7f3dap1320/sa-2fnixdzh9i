# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_head import *
from app_metatags import *
from app_title import *
from app_body import *
from bootstrap import *
from app_loading import *
from app_stylesheet import *
from awesomplete import *
from app_navbar import *
from font_awesome import *
from createuser_form import *
from sa_func import *
import pymysql.cursors
from sa_db import *
from app_cookie import *
import datetime
import time
access_obj = sa_db_access()
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def set_nickname():
    p1 = ''; p2 =''; num = ''
    r = ''
    try:
        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT part_one FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: p1 = row[0]
        sql = "SELECT part_two FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: p2 = row[0]
        num = str( get_random_num(99) )
        r = p1 + p2 + num
    except Exception as e: print(e)
    return r


def gen_createuser_page(uid,appname,burl,name,username,password):
    r = ''
    if uid == '0':
        r = get_head( get_loading_head() + get_title( appname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_user_creation_form(burl) )
        r = set_page(r)
    else:
        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT username FROM users WHERE uid = '"+ str(uid) +"' OR username LIKE '"+ str(username) +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        check_exists = ''
        for row in rs: check_exists = row[0]
        if check_exists == '':
            r = name + " " + username + " " + password + " " + uid
            nickname = set_nickname()
            d = datetime.datetime.now() ; d = d.strftime('%Y%m%d')
            referred_by_code = get_refer_by_code()
            sql = "INSERT INTO users(uid, name, nickname, username, password, created_on, referred_by_code) "+\
            "VALUES ('"+ str(uid) +"','"+ str(name) +"','"+ str(nickname) +"','"+ str(username) +"','"+ str(password) +"',"+ str(d) +", '"+ str(referred_by_code) +"' )"
            cr.execute(sql)
            connection.commit()
            set_sa_cookie(uid,referred_by_code)
            r = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + str(burl) + '" />') + get_body('','') )
        else:
            r = 'user exists'
        cr.close()
        connection.close()
    return r
