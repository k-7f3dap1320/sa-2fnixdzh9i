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

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portfolios.order_type, portfolios.quantity, portfolios.symbol, portfolios.entry_level, portfolios.expiration, "+\
        "symbol_list.uid FROM portfolios JOIN symbol_list ON portfolios.portf_symbol = symbol_list.symbol "+\
        "WHERE symbol_list.uid=" + str(uid) + " ORDER BY portfolios.symbol"
        cr.execute(sql)
        rs = cr.fetchall()
        signal_box_data = ''
        for row in rs:
            order_type = row[0]
            quantity = row[1]
            symbol = row[2]
            entry_price = row[3]
            trade_expiration = row[4]
            exp_date_str = trade_expiration.strftime("%d-%b-%Y")

            if order_type == 'buy':
                badge = 'badge-success'
            else:
                badge = 'badge-danger'
            signal_box_data = signal_box_data + '' +\
            '                       <tr>'+\
            '                          <th scope="row"><span class="badge '+ badge +'">'+ order_type +'</span></th>'+\
            '                          <td>'+ str(quantity)  +'</td>'+\
            '                          <td>'+ symbol +'</td>'+\
            '                          <td>'+ str(entry_price) +'</td>'+\
            '                          <td>'+ exp_date_str +'</td>'+\
            '                       </tr>'
        cr.close()
        connection.close()

        signal_box = '' +\
        '        <div class="col-lg-8 col-md-8 col-sm-6 col-xs-12">'+\
        '            <div class="box-part">'+\
        '               <table class="table table-hover table-sm sa-table-sm">'+\
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
        signal_box = signal_box + signal_box_data
        signal_box = signal_box + '' +\
        '                   </tbody>'+\
        '               </table>'+\
        '            </div>'+\
        '        </div>'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT count(1) FROM `portfolios` JOIN symbol_list ON portfolios.portf_symbol = symbol_list.symbol WHERE symbol_list.uid=" + str(uid)
        cr.execute(sql); rs = cr.fetchall()
        for row in rs:
            num_rec = row[0]
        num_rec = round( 255 / num_rec, 0)

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portfolios.alloc_fullname, portfolios.order_type, portfolios.dollar_amount "+\
        "FROM `portfolios` JOIN symbol_list ON portfolios.portf_symbol = symbol_list.symbol WHERE symbol_list.uid=" + str(uid) + " "+\
        "ORDER BY portfolios.dollar_amount"
        cr.execute(sql)
        rs = cr.fetchall()
        pie_chart_data = ''
        pie_chart_option = ''
        i = 0
        count_buy = 0
        count_sell = 0
        sell_color_R = 255; sell_color_G = 0; sell_color_B = 0
        buy_color_R = 198; buy_color_G = 255; buy_color_B = 0

        for row in rs:
            alloc_fullname = row[0]
            order_type = row[1]
            dollar_amount = row[2]
            if i == 0:
                pie_chart_data = '["'+ alloc_fullname +'", '+ str(dollar_amount) +']'
            else:
                pie_chart_data = pie_chart_data + ', ' + '["'+ alloc_fullname +'", '+ str(dollar_amount) +']'
            if order_type == 'buy':
                if buy_color_B > num_rec:
                    buy_color_R = buy_color_R - num_rec
                if buy_color_G > num_rec:
                    buy_color_G = buy_color_G - num_rec
                if buy_color_B > num_rec:
                    buy_color_B = buy_color_B - num_rec
                if i == 0:
                    pie_chart_option = '{'+ str(i) +':{color:"rgb('+ str(buy_color_R) +','+ str(buy_color_G) +','+ str(buy_color_B) +')"}}'
                else:
                    pie_chart_option = pie_chart_option + ', {'+ str(i) +':{color:"rgb('+ str(buy_color_R) +','+ str(buy_color_G) +','+ str(buy_color_B) +')"}}'
            if order_type == 'sell':
                if buy_color_B > num_rec:
                    buy_color_R = buy_color_R - num_rec
                if buy_color_G < (255 - num_rec):
                    buy_color_G = buy_color_G + num_rec
                if buy_color_B < (255 - num_rec):
                    buy_color_B = buy_color_B + num_rec
                if i == 0:
                    pie_chart_option = '{'+ str(i) +':{color:"rgb('+ str(sell_color_R) +','+ str(sell_color_G) +','+ str(sell_color_B) +')"}}'
                else:
                    pie_chart_option = pie_chart_option + ', {'+ str(i) +':{color:"rgb('+ str(sell_color_R) +','+ str(sell_color_G) +','+ str(sell_color_B) +')"}}'

            i += 1

        pie_chart_title = 'Portfolio Allocation'
        pie_chart_x = "Allocation"
        pie_chart_y = "Dollar Amount"
        pie_chart = '' +\
        '        <div class="col-lg-4 col-md-4 col-sm-6 col-xs-12">'+\
        '           <div class="box-part">'+\
        '               <script type="text/javascript">'+\
        '                   google.charts.load("current", {packages:["corechart"]});'+\
        '                   google.charts.setOnLoadCallback(drawChart);'+\
        '                   function drawChart() {'+\
        '                       var data = google.visualization.arrayToDataTable(['+\
        '                       ["'+ pie_chart_x +'", "'+ pie_chart_y +'"],'
        pie_chart = pie_chart + pie_chart_data
        pie_chart = pie_chart + '' +\
        '                       ]);'+\
        '                       var options = {'+\
        '                           title: "'+ pie_chart_title +'",'+\
        '                           pieHole: 0.2,'+\
        '                           legend: "none",'+\
        '                           pieSliceText: "percentage",'
        '                           slices: ' + pie_chart_option  + ''+\
        '                           legend: {position:"labeled", textStyle: {fontSize: 11}}'+\
        '                       },'+\
        '                       var chart = new google.visualization.PieChart(document.getElementById("piechart"));'+\
        '                       chart.draw(data, options);'+\
        '                   }'+\
        '               </script>'+\
        '           </div>'+\
        '        </div>'


    except Exception as e: print(e)


    return signal_box + pie_chart
