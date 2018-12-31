# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from trail_retunrs_chart import *


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_box_risk_content(uid):

    box_content = ''

    try:

        box_content = '' +\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '            </div>'+\
        '        </div>'

    except Exception as e: print(e)

    return box_content


def get_box_trail_returns_content(uid):

    box_content = ''

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.fullname FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            fullname = row[0]

        l_title = fullname + ' trailing returns'
        box_content = '' +\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '               <div>'+ l_title +'</div>'+\
        get_trailing_returns(uid) +\
        '            </div>'+\
        '        </div>'


    except Exception as e: print(e)

    return box_content

def get_portf_risk_trail_returns(uid):
    return get_box_risk_content(uid) + get_box_trail_returns_content(uid)
