# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from app_cookie import *
from sa_func import *
from tradingview_ticker import *


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_box_user_profile_header(burl):

    box_content = ''

    try:
        if user_is_login() == 1:
            uid = user_get_uid()
            connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT nickname, name FROM users WHERE uid='"+ str(uid) +"'"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                nickname = row[0]
                name = row[1]

            avatar_img = get_avatar(burl,60)


            box_content = '<div class="box-uhead sa-uhead-box">' +\
            '   <div class="row sa-uhead-box bg-dark">'+\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="box-part rounded sa-center-content sa-uhead-box" style="height: 75px;">'+\
            get_tradingview_ticker(uid) +\
            '            </div>'+\
            '        </div>'+\
            '   </div>'+\
            '</div>'


            cr.close()
            connection.close()

    except Exception as e: print(e)

    return box_content
