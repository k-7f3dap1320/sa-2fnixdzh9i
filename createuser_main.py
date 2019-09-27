# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_head import *
from app_ogp import *
from app_footer import *
from app_metatags import *
from app_title import *
from app_body import *
from bootstrap import *
from app_loading import *
from app_stylesheet import *
from awesomplete import *
from tablesorter import *
from app_navbar import *
from font_awesome import *
from createuser_form import *
from sa_func import *
import pymysql.cursors
from sa_db import *
from app_cookie import *
import datetime
import time
from googleanalytics import *

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
        cr.close()
        connection.close()
        num = str( get_random_num(99) )
        r = p1 + p2 + num
    except Exception as e: print(e)
    return r


def gen_createuser_page(uid,appname,burl,name,username,password,from_ip):
    r = ''
    if uid == '0':
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl,0) + get_user_creation_form(burl) + get_page_footer(burl) )
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
            name = name.lower()
            nickname = set_nickname()
            d = datetime.datetime.now() ; d = d.strftime('%Y%m%d')
            referred_by_code = get_refer_by_code()
            avatar_id = get_random_num(19)
            email_subscription = 'ALL'
            password = get_hash_string(password)
            sql = "INSERT INTO users(uid, name, nickname, username, password, created_on, referred_by_code, avatar_id, from_ip,lang,email_subscription) "+\
            "VALUES ('"+ str(uid) +"','"+ str(name) +"','"+ str(nickname) +"','"+ str(username) +"','"+ str(password) +"',"+ str(d) +", '"+ str(referred_by_code) +"', "+ str(avatar_id) +", '"+ str(from_ip) + "', '"+ str( get_lang() )  +"', 'ALL' )"
            cr.execute(sql)
            connection.commit()
            r = set_sa_cookie(uid, set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + 'n/?step=a" />') + get_body('','') ) )
        else:
            r = 'user already exists :P !'
        cr.close()
        connection.close()
    return r
