# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def get_portf_alloc(uid):

    signal_box = ''; pie_chart = ''

    try:

        signal_box = '' +\
        '        <div class="col-lg-8 col-md-8 col-sm-6 col-xs-12">'+\
        '            <div class="box-part">'+\
        '               <table class="table table-hover table-sm">'+\
        '                   <thead>'+\
        '                       <tr>'+\
        '                          <th scope="col">Order</th>'+\
        '                          <th scope="col">Quantity</th>'+\
        '                          <th scope="col">Ticker</th>'+\
        '                          <th scope="col">Entry @</th>'+\
        '                          <th scope="col">Expires on</th>'+\
        '                       </tr>'+\
        '                   </thead>'+\
        '                   <tbody>'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portfolios.order_type, portfolios.quantity, portfolios.symbol, portfolios.entry_level, portfolios.expiration, "+\
        "symbol_list.uid FROM portfolios JOIN symbol_list ON portfolios.portf_symbol = symbol_list.symbol "+\
        "WHERE symbol_list.uid=" + str(uid) + " ORDER BY portfolios.symbol"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs_s:
            order_type = row[0]
            quantity = row[1]
            symbol = row[2]
            entry_price = row[3]
            trade_expiration = row[4]

            if order_type == 'buy':
                badge = 'badge-success'
            else:
                badge = 'badge-danger'

            signal_box = signal_box +\
            '                       <tr>'+\
            '                          <th scope="row"><span class="badge '+ badge +'">Success</span></th>'+\
            '                          <td>'+ str(quantity)  +'</td>'+\
            '                          <td>'+ symbol +'</td>'+\
            '                          <td>'+ str(entry_price) +'</td>'+\
            '                          <td>'+ str(trade_expiration) +'</td>'+\
            '                       </tr>'
        signal_box = signal_box +\
        '                   </tbody>'+\
        '               </table>'+\
        '            </div>'+\
        '        </div>'
        cr.close()
        connection.close()


        pie_chart = '' +\
        '        <div class="col-lg-4 col-md-4 col-sm-6 col-xs-12">'+\
        '            <div class="box-part">'+\
        '            </div>'+\
        '        </div>'


    except Exception as e: print(e)


    return signal_box + pie_chart
