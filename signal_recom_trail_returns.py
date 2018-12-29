# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from trail_returns_chart import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_recomm(uid):

    recomm_box = ''

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.recommendation FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        recommendation = row[0]

    l_title = 'Technical analysis & recommendation'

    recomm_box = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part sa-signal-recomm-trail-ret">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    '               <div>'+ recommendation +'</div>'+\
    '            </div>'+\
    '        </div>'

    cr.close()
    connection.close()

    return recomm_box

def get_chart_box(uid):

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT price_instruments_data.date, instruments.fullname FROM price_instruments_data JOIN symbol_list "+\
    "ON symbol_list.symbol = price_instruments_data.symbol "+\
    "JOIN instruments ON instruments.symbol = symbol_list.symbol "+\
    "WHERE symbol_list.uid=" + str(uid) +" "+\
    "ORDER BY date DESC LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        as_date = row[0]
        fullname = row[1]
    cr.close()
    connection.close()

    l_as_date = 'Trailing returns as of '+ as_date.strftime("%d-%b-%Y")
    l_title = fullname + ' trailing returns'

    r = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part sa-signal-recomm-trail-ret">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    get_trailing_returns(uid) +\
    '            </div>'+\
    '        </div>'

    return r

def get_sign_recommend_trail_returns(uid):

    r =''

    try:

        r = get_recomm(uid) + get_chart_box(uid)

    except Exception as e: print(e)

    return r
