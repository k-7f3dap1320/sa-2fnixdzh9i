# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
import string
import random
from app_cookie import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_user():
    return user_get_uid()

def get_avatar(burl,height):
    r = ''
    try:
        uid = user_get_uid()
        avatar_id = 0
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT avatar_id FROM users WHERE uid = '"+ str(uid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: avatar_id = row[0]
        if avatar_id != 0:
            r = '<img alt="" src="'+burl+'static/avatar/'+ str(avatar_id) +'.png" style="vertical-align: middle;border-style: none;width: '+ str(height) +'px;">'
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def is_subscribed_user():
    r = 0
    try:
        uid = user_get_uid()
        is_subscribed = 0
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT is_subscribed FROM users WHERE uid = '"+ str(uid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: is_subscribed = row[0]
        r = is_subscribed
    except Exception as e: print(e)
    return r

def redirect_if_not_logged_in(burl,redirect):
    r = ''
    try:
        if user_is_login() != 1:
            r = '<meta http-equiv="refresh" content="5; url='+burl+'signin/?redirect='+ redirect +'">'
        else:
            r = ''
    except Exception as e: print(e)
    return r

def get_user_numeric_id():
    r = ''
    try:
        uid = user_get_uid()
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT id FROM users WHERE uid = '"+ str(uid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_nickname():
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT nickname FROM users WHERE uid = '"+ get_user() +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

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

def get_uid_from_tvws(tvws):
    uid = 0
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT uid FROM symbol_list WHERE tradingview = '"+ str(tvws) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        uid = 0
        for row in rs:
            uid = row[0]
        cr.close()
        connection.close()
    except Exception as e: print(e)

    return uid

def get_user_default_profile():
    r = ''
    try:
        user_uid = get_user()

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT default_profile FROM users WHERE uid = '"+ user_uid +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        default_profile = ''
        for row in rs:
            default_profile = row[0]
        cr.close()
        connection.close()

        r = default_profile

    except Exception as e: print(e)
    return r

def get_random_str(n):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def get_random_num(n):
    max = int(n)
    return random.randint(1,max)

def get_lang():
    return request.cookies.get('lang')

def get_selected_lang():
    return get_lang()

def get_signal(uid):
    signal = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT badge FROM feed JOIN symbol_list ON symbol_list.symbol = feed.symbol "+\
        "WHERE symbol_list.uid=" + str(uid) + " AND feed.type=1 "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            badge = row[0]

        if (badge.find('-0') == -1 and badge.find('-1') == -1 and
        badge.find('-2') == -1 and badge.find('-3') == -1 and
        badge.find('-4') == -1 and badge.find('-5') == -1 and
        badge.find('-6') == -1 and badge.find('-7') == -1 and
        badge.find('-8') == -1 and badge.find('-9') == -1) :
            signal = 'b'
        else:
            signal = 's'
    except Exception as e: print(e)
    return signal

def get_elapsed_time(vminutes):
    r = ''
    try:
        r = 'now'
        if vminutes >0 and vminutes < 60: r = str(vminutes) + 'm ago'
        if vminutes >= 60 and vminutes < 1440: r = str( round(vminutes/60,0) ) + 'h ago'
        if vminutes >= 1440: r = str( round(vminutes/1440,0) ) + 'd ago'

    except Exception as e: print(e)
    return r

def go_to_url(q,return_what,uniqid):
    #---------------------------------
    # return_what = 'form' = '<form id="form_id_xxx"><input type="hidden" value="'+ str(q) +'" id="q"></form>'
    # return_what = link = 'href="javascript:{}" onclick="document.getElementById('form_id_xxx').submit(); return false;"'
    #---------------------------------
    r = ''
    try:
        r = 'url/?q=' + str(q)

        content = ''
        if return_what == 'form':
            content = '<form id="'+ str(uniqid) +'" " action="'+ 'url/' +'" method="post" target="_blank"><input type="hidden" value="'+ str(q) +'"></form>'
        if return_what == 'link':
            content = 'href="javascript:{}" onclick="document.getElementById(\''+ str(uniqid) +'\').submit(); return false;"'
        r = content
    except Exception as e: print(e)
    return r
