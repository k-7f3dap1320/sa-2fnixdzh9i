# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def get_portf_alloc(uid,burl):

    signal_box = ''; pie_chart = ''

    try:

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portfolios.order_type, portfolios.quantity, portfolios.symbol, portfolios.entry_level, portfolios.expiration, portfolios.alloc_fullname, portfolios.strategy_order_type, symbol_list.uid FROM portfolios "+\
        "JOIN symbol_list ON symbol_list.symbol = portfolios.portf_symbol WHERE symbol_list.uid="+ str(uid) +" ORDER BY portfolios.symbol"
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
            symbol_fullname = row[5]
            strategy_order_type = row[6]
            symbol_uid = row[7]

            if order_type == 'buy':
                badge = 'badge-success'
            else:
                badge = 'badge-danger'
            if (order_type == 'buy' and strategy_order_type == 'short') or (order_type == 'sell' and strategy_order_type == 'long'):
                order_type = 'wait'
                badge = 'badge-secondary'
                entry_price = '-'
                quantity = '-'

            signal_box_data = signal_box_data + '' +\
            '                       <tr>'+\
            '                          <th scope="row"><span class="badge '+ badge +'">'+ order_type +'</span></th>'+\
            '                          <td>'+ str(quantity)  +'</td>'+\
            '                          <td><a href="'+ burl +'s/?uid='+ str(symbol_uid) +'">'+ symbol_fullname +'</a></td>'+\
            '                          <td>'+ str(entry_price) +'</td>'+\
            '                          <td>'+ exp_date_str +'</td>'+\
            '                       </tr>'
        cr.close()
        connection.close()

        signal_box = '' +\
        '        <div class="col-lg-7 col-md-7 col-sm-6 col-xs-12">'+\
        '            <div class="box-part rounded sa-portf-alloc">'+\
        '               <table class="table table-hover table-sm sa-table-sm">'+\
        '                   <thead>'+\
        '                       <tr>'+\
        '                          <th scope="col">Order</th>'+\
        '                          <th scope="col">Quantity</th>'+\
        '                          <th scope="col">Trade</th>'+\
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
        sql = "SELECT portfolios.alloc_fullname, portfolios.order_type, portfolios.dollar_amount, portfolios.symbol, portfolios.strategy_order_type "+\
        "FROM `portfolios` JOIN symbol_list ON portfolios.portf_symbol = symbol_list.symbol WHERE symbol_list.uid=" + str(uid) + " "+\
        "ORDER BY portfolios.dollar_amount"
        cr.execute(sql)
        rs = cr.fetchall()
        pie_chart_data = ''
        pie_chart_option = ''
        i = 0
        count_buy = 0
        count_sell = 0
        count_wait = 0
        sell_color_R = 255; sell_color_G = 0; sell_color_B = 0
        buy_color_R = 198; buy_color_G = 255; buy_color_B = 0
        wait_color_R = 220; wait_color_G = 220; wait_color_B = 220

        for row in rs:
            alloc_fullname = row[0]
            order_type = row[1]
            dollar_amount = row[2]
            alloc_symbol = row[3]
            strategy_order_type = row[4]

            if (order_type == 'buy' and strategy_order_type == 'short') or (order_type == 'sell' and strategy_order_type == 'long'):
                order_type = 'wait'

            if i == 0:
                pie_chart_data = '["'+ alloc_fullname +' ('+ alloc_symbol +')'+'", '+ str(dollar_amount) +']'
            else:
                pie_chart_data = pie_chart_data + ', ' + '["'+ alloc_fullname + ' ('+ alloc_symbol +')' +'", '+ str(dollar_amount) +']'
            if order_type == 'buy':
                if count_buy > 0:
                    if buy_color_B > num_rec:
                        buy_color_R = buy_color_R - num_rec
                    if buy_color_B < (255):
                        buy_color_B = buy_color_B + num_rec
                count_buy += 1
                if i == 0:
                    pie_chart_option = str(i) +':{color:"rgb('+ str( int(buy_color_R) ) +','+ str( int(buy_color_G) ) +','+ str( int(buy_color_B) ) +')"}'
                else:
                    pie_chart_option = pie_chart_option + ', '+ str(i) +':{color:"rgb('+ str( int(buy_color_R) ) +','+ str( int(buy_color_G) ) +','+ str( int(buy_color_B) ) +')"}'
            if order_type == 'sell':
                if count_sell > 0:
                    if sell_color_B > num_rec:
                        sell_color_R = sell_color_R - num_rec
                    if sell_color_G < (255):
                        sell_color_G = sell_color_G + num_rec
                    if sell_color_B < (255):
                        sell_color_B = sell_color_B + num_rec
                count_sell += 1
                if i == 0:
                    pie_chart_option =  str(i) +':{color:"rgb('+ str( int(sell_color_R) ) +','+ str( int(sell_color_G) ) +','+ str( int(sell_color_B) ) +')"}'
                else:
                    pie_chart_option = pie_chart_option + ', '+ str(i) +':{color:"rgb('+ str( int(sell_color_R) ) +','+ str( int(sell_color_G) ) +','+ str( int(sell_color_B) ) +')"}'
            if order_type == 'wait':
                count_wait += 1
                if i == 0:
                    pie_chart_option =  str(i) +':{color:"rgb('+ str( int(wait_color_R) ) +','+ str( int(wait_color_G) ) +','+ str( int(wait_color_B) ) +')"}'
                else:
                    pie_chart_option = pie_chart_option + ', '+ str(i) +':{color:"rgb('+ str( int(wait_color_R) ) +','+ str( int(wait_color_G) ) +','+ str( int(wait_color_B) ) +')"}'

            i += 1
        cr.close()
        connection.close()

        pie_chart_title = 'Portfolio Allocation'
        pie_chart_x = "Allocation"
        pie_chart_y = "Dollar Amount"
        pie_chart_font_size = 10
        pie_chart = '' +\
        '        <div class="col-lg-5 col-md-5 col-sm-6 col-xs-12">'+\
        '           <div class="box-part rounded sa-portf-alloc">'+\
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
        '                           pieSliceText: "percentage",'+\
        '                           slices: {' + pie_chart_option  + '},'+\
        '                           legend: {position:"labeled", textStyle: {fontSize: '+ str(pie_chart_font_size) +'} },'+\
        '                           chartArea:{width:"90%",height:"80%"}'+\
        '                       };'+\
        '                       var chart = new google.visualization.PieChart(document.getElementById("portf_alloc_pie_chart"));'+\
        '                       chart.draw(data, options);'+\
        '                   }'+\
        '               </script>'+\
        '               <div id="portf_alloc_pie_chart" class="sa-chart-hw-90"></div>'+\
        '           </div>'+\
        '        </div>'


    except Exception as e: print(e)


    return signal_box + pie_chart
