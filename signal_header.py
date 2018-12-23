# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_sign_header(uid):

    descr_box = ''

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.symbol, instruments.w_forecast_change, instruments.w_forecast_display_info, "+\
        "instruments.trade_1_type, instruments.trade_1_entry, instruments.trade_1_tp, instruments.trade_1_sl, "+\
        "instruments.trade_3_type, instruments.trade_3_entry, instruments.trade_3_tp, instruments.trade_3_sl "+\
        "FROM instruments JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
        " WHERE symbol_list.uid=" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            symbol = row[0]
            w_forecast_change = row[1]
            w_forecast_display_info = row[2]
            trade_1_type = row[3]
            trade_1_entry = row[4]
            trade_1_tp = row[5]
            trade_1_sl = row[6]
            trade_3_type = row[3]
            trade_3_entry = row[4]
            trade_3_tp = row[5]
            trade_3_sl = row[6]

        sql = "SELECT price_instruments_data.date, price_instruments_data.price_close  "+\
        "FROM price_instruments_data JOIN symbol_list ON price_instruments_data.symbol = symbol_list.symbol "+\
        "WHERE symbol_list.uid=" + str(uid)
        " ORDER BY date DESC LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            price_date = row[0]
            price_close = row[1]


        if float(w_forecast_change) >= 0:
            signal = '<span class="btn btn-outline-success">Buy</span>'
            entry = trade_1_entry
            tp = trade_1_tp
            sl = trade_1_sl
        else:
            signal = '<span class="btn btn-outline-danger">Sell</span>'
            entry = trade_3_entry
            tp = trade_3_tp
            sl = trade_3_sl

        hd_price =  'Price (' + price_date.strftime("%d-%b-%Y") + ')'
        hd_signal = 'Signal'
        hd_entry = 'Entry @'
        hd_tp = 'Target price'
        hd_sl = 'Stop loss'

        c_price = str(price_close)
        c_signal = signal
        c_entry = str(entry)
        c_tp = str(tp)
        c_sl = str(sl)


        descr_box = '' +\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '               <table class="table table-sm sa-table-sm">'+\
        '                   <tbody>'+\
        '                       <tr>'+\
        '                           <td>'+ hd_price +'</td>'+\
        '                           <td>'+ hd_signal +'</td>'+\
        '                           <td>'+ hd_entry +'</td>'+\
        '                           <td>'+ hd_tp +'</td>'+\
        '                           <td>'+ hd_sl +'</td>'+\
        '                       </tr>'+\
        '                       <tr>'+\
        '                           <td><h5>'+ c_price +'<h5></td>'+\
        '                           <td><h6>'+ c_signal +'</h6></td>'+\
        '                           <td><h6>'+ c_entry +'</h6></td>'+\
        '                           <td><h6>'+ c_tp +'</h6></td>'+\
        '                           <td><h6>'+ c_sl +'</h6></td>'+\
        '                       </tr>'+\
        '                   </tbody>'+\
        '               </table>'+\
        '            </div>'+\
        '        </div>'


        cr.close()
        connection.close()
    except Exception as e: print(e)

    return descr_box
