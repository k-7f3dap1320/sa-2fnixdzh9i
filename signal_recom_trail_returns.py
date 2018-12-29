# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from trail_returns_chart import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_chart_data(uid,p):
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname,instruments.y1, instruments.m6, instruments.m3, instruments.m1, instruments.w1, instruments.unit, instruments.is_benchmark "+\
    "FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        fullname = row[0]
        y1 = row[1]
        m6 = row[2]
        m3 = row[3]
        m1 = row[4]
        w1 = row[5]
        unit = row[6]
        is_benchmark = row[7]

    if unit == '%':
        y1 = round( y1*100 ,2 )
        m6 = round( m6*100 ,2 )
        m3 = round( m3*100 ,2 )
        m1 = round( m1*100 ,2 )
        w1 = round( w1*100 ,2 )
    cr.close()
    connection.close()

    if p == 'y1':
        data = str(y1) + ',"' + str(y1) +' '+ str(unit)  + '"'
    if p == 'm6':
        data = str(m6) + ',"' + str(m6) +' '+ str(unit)  + '"'
    if p == 'm3':
        data = str(m3) + ',"' + str(m3) +' '+ str(unit)  + '"'
    if p == 'm1':
        data = str(m1) + ',"' + str(m1) +' '+ str(unit)  + '"'
    if p == 'w1':
        data = str(w1) + ',"' + str(w1) +' '+ str(unit)  + '"'

    return data

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
    sql = "SELECT price_instruments_data.date FROM price_instruments_data JOIN symbol_list "+\
    "ON symbol_list.symbol = price_instruments_data.symbol WHERE symbol_list.uid=" + str(uid) +" "+\
    "ORDER BY date DESC LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        as_date = row[0]
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
