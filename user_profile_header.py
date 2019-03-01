# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from app_cookie import *


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_box_user_profile_header(burl):

    box_content = ''

    try:
        if user_is_login() == 1:
            uid = user_get_uid()
            connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT nickname, name from users WHERE uid='"+ str(uid) +"'"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                nickname = row[0]
                name = row[1]


            box_content = '<div class="box-uhead sa-uhead-box">' +\
            '   <div class="row sa-uhead-box">'+\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="box-part sa-center-content sa-uhead-box">'+\
            '<br><h4>Hello '+ name +'</h4><br><br>'+\
            '            </div>'+\
            '        </div>'+\
            '   </div>'+\
            '</div>'


            cr.close()
            connection.close()

    except Exception as e: print(e)

    return box_content
