# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from trail_returns_chart import *
from sa_func import *


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_box_risk_content(uid):

    box_content = ''

    try:

        lang = get_selected_lang()

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portf_risk_consider FROM `recommendations` WHERE lang='"+ lang +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            text_content = row[0]

        sql = "SELECT instruments.account_reference, instruments.unit FROM instruments "+\
        "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
        "WHERE symbol_list.uid=" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            account_reference = row[0]
            unit = row[1]

        dollar_amount = 0
        percentage = 0

        text_content = text_content.replace('{account_reference}', str(account_reference) )
        text_content = text_content.replace('{unit}', str(unit) )
        text_content = text_content.replace('{dollar_amount}', str(dollar_amount) )
        text_content = text_content.replace('{percentage}', str(percentage) )

        l_title = 'Risk considerations'

        box_content = '' +\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-signal-recomm-trail-ret">'+\
        '               <div><h6>'+ l_title +'</h6></div>'+\
        '                   <div>'+ text_content +'</div>'+\
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

        l_title = fullname + ' portfolio trailing returns'
        box_content = '' +\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-signal-recomm-trail-ret">'+\
        '               <div><h6>'+ l_title +'</h6></div>'+\
        get_trailing_returns(uid) +\
        '            </div>'+\
        '        </div>'
        cr.close()
        connection.close()

    except Exception as e: print(e)

    return box_content

def get_portf_risk_trail_returns(uid):
    return get_box_risk_content(uid) + get_box_trail_returns_content(uid)
