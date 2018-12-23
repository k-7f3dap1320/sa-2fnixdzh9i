# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_alt_orders(uid):

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.trade_1_entry, instruments.trade_1_tp, instruments.trade_1_sl, instruments.trade_1_type, "+\
    "instruments.trade_2_entry, instruments.trade_2_tp, instruments.trade_2_sl, instruments.trade_2_type, "+\
    "instruments.trade_3_entry, instruments.trade_3_tp, instruments.trade_3_sl, instruments.trade_3_type, "+\
    "instruments.trade_4_entry, instruments.trade_4_tp, instruments.trade_4_sl, instruments.trade_4_type, "+\
    "instruments.decimal_places FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs_s:
        trade_1_entry = row[0]; trade_1_tp = row[1]; trade_1_sl = row[2]; trade_1_type = row[3]
        trade_2_entry = row[4]; trade_2_tp = row[5]; trade_2_sl = row[6]; trade_2_type = row[7]
        trade_3_entry = row[8]; trade_3_tp = row[9]; trade_3_sl = row[10]; trade_3_type = row[11]
        trade_4_entry = row[12]; trade_4_tp = row[13]; trade_4_sl = row[14]; trade_4_type = row[15]
        decimal_places = row[16]

    cr.close()
    connection.close()


    hd_order = "Order"
    hd_entry = "Entry @"
    hd_tp = "Target price"
    hd_sl = "Stop loss"

    buy_badge = '<span class="badge badge-success">buy</span>'
    sell_badge = '<span class="badge badge-danger">sell</span>'
    table_content = ''

    # Trade 1
    table_content = table_content +'<tr>'
    if trade_1_type == 'buy':
        table_content = table_content + '<th scope="row">'+ buy_badge +'</th>'
    else:
        table_content = table_content + '<th scope="row">'+ sell_badge +'</th>'
    table_content = table_content +\
    '   <td>'+ str(  round(trade_1_entry, decimal_places) ) +'</td>'+\
    '   <td>'+ str(  round(trade_1_tp, decimal_places) ) +'</td>'+\
    '   <td>'+ str(  round(trade_1_sl, decimal_places) ) +'</td>'+\
    '</tr>'
    # Trade 2
    table_content = table_content +'<tr>'
    if trade_2_type == 'buy':
        table_content = table_content + '<th scope="row">'+ buy_badge +'</th>'
    else:
        table_content = table_content + '<th scope="row">'+ sell_badge +'</th>'
    table_content = table_content +\
    '   <td>'+ str(  round(trade_2_entry, decimal_places) ) +'</td>'+\
    '   <td>'+ str(  round(trade_2_tp, decimal_places) ) +'</td>'+\
    '   <td>'+ str(  round(trade_2_sl, decimal_places) ) +'</td>'+\
    '</tr>'
    # Trade 3
    table_content = table_content +'<tr>'
    if trade_3_type == 'buy':
        table_content = table_content + '<th scope="row">'+ buy_badge +'</th>'
    else:
        table_content = table_content + '<th scope="row">'+ sell_badge +'</th>'
    table_content = table_content +\
    '   <td>'+ str(  round(trade_3_entry, decimal_places) ) +'</td>'+\
    '   <td>'+ str(  round(trade_3_tp, decimal_places) ) +'</td>'+\
    '   <td>'+ str(  round(trade_3_sl, decimal_places) ) +'</td>'+\
    '</tr>'
    # Trade 4
    table_content = table_content +'<tr>'
    if trade_4_type == 'buy':
        table_content = table_content + '<th scope="row">'+ buy_badge +'</th>'
    else:
        table_content = table_content + '<th scope="row">'+ sell_badge +'</th>'
    table_content = table_content +\
    '   <td>'+ str(  round(trade_4_entry, decimal_places) ) +'</td>'+\
    '   <td>'+ str(  round(trade_4_tp, decimal_places) ) +'</td>'+\
    '   <td>'+ str(  round(trade_4_sl, decimal_places) ) +'</td>'+\
    '</tr>'

    r = ''+\
    '<table class="table table-sm">'+\
    '<thead>'+\
    '    <tr>'+\
    '      <th scope="col">'+ hd_order +'</th>'+\
    '      <th scope="col">'+ hd_entry +'</th>'+\
    '      <th scope="col">'+ hd_tp +'</th>'+\
    '      <th scope="col">'+ hd_sl +'</th>'+\
    '    </tr>'+\
    '  </thead>'+\
    '  <tbody>'+\
    table_content +\
    ' </tbody>'+\
    '</table>'

    return r



def get_sign_ta_chart(uid):

    try:
        signal_box = ''; tech_chart = ''

        signal_box = '' +\
        '        <div class="col-lg-4 col-md-6 col-sm-6 col-xs-12">'+\
        '            <div class="box-part">'+\
        get_alt_orders(uid) +\
        '            </div>'+\
        '        </div>'

        tech_chart = '' +\
        '        <div class="col-lg-8 col-md-6 col-sm-6 col-xs-12">'+\
        '            <div class="box-part">'+\
        '            </div>'+\
        '        </div>'
    except Exception as e: print(e)

    return signal_box + tech_chart
