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

from sa_func import *
from sa_db import *
from app_cookie import *
import pymysql.cursors
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_select_avatar(burl):

    box_content = ''

    try:
        user_uid = user_get_uid()

        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT avatar_id, nickname FROM users WHERE uid = '"+ str(user_uid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: avatar_id = row[0]; nickname = row[1]

        #avatar, from 1 to 19
        avatar_path = burl + "static/avatar/"; avatar_ext = ".png"
        avatar = avatar_path + str(avatar_id) + avatar_ext


        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '<img src="'+ str(avatar)+'" height="200">'
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content

def gen_createuser_avatar(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_title( appname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_select_avatar(burl) )
        r = set_page(r)
    except Exception as e: print(e)
    return r
