""" Strategy portfolio allocation """
import pymysql.cursors
from app_cookie import theme_return_this
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def get_portf_alloc(uid, burl):
    """ xxx """
    signal_box = ''
    pie_chart = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT portfolios.order_type, portfolios.quantity, "+\
    "portfolios.symbol, portfolios.entry_level, "+\
    "portfolios.expiration, portfolios.alloc_fullname, "+\
    "portfolios.strategy_order_type FROM portfolios "+\
    "JOIN symbol_list ON symbol_list.symbol = portfolios.portf_symbol "+\
    "WHERE symbol_list.uid="+\
    str(uid) +" ORDER BY portfolios.symbol"

    cursor.execute(sql)
    res = cursor.fetchall()
    signal_box_data = ''
    for row in res:
        order_type = row[0]
        quantity = row[1]
        symbol = row[2]
        entry_price = row[3]
        trade_expiration = row[4]
        exp_date_str = trade_expiration.strftime("%d-%b-%Y")
        symbol_fullname = row[5]
        strategy_order_type = row[6]

        cr_s = connection.cursor(pymysql.cursors.SSCursor)
        sql_s = "SELECT uid FROM symbol_list WHERE symbol = '"+ symbol +"'"
        cr_s.execute(sql_s)
        rs_s = cr_s.fetchall()
        for row in rs_s:
            symbol_uid = row[0]

        if order_type == 'buy':
            badge = 'badge-success'
        else:
            badge = 'badge-danger'
        if ((order_type == 'buy' and strategy_order_type == 'short') or\
            (order_type == 'sell' and strategy_order_type == 'long')):
            order_type = 'wait'
            badge = 'badge-secondary'
            entry_price = '-'
            quantity = '-'

        signal_box_data = signal_box_data + '' +\
        '                       <tr>'+\
        '                          <th scope="row"><span class="badge '+\
        badge +'">'+\
        order_type +'</span></th>'+\
        '                          <td>'+\
        str(quantity)  +'</td>'+\
        '                          <td><a href="'+\
        burl +'s/?uid='+\
        str(symbol_uid) +'">'+\
        symbol_fullname +'</a></td>'+\
        '                          <td>'+ str(entry_price) +'</td>'+\
        '                          <td>'+ exp_date_str +'</td>'+\
        '                       </tr>'
        cr_s.close()
    cursor.close()
    connection.close()

    signal_box = '' +\
    '        <div class="col-lg-7 col-md-7 col-sm-6 col-xs-12">'+\
    '            <div class="box-part rounded sa-portf-alloc" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
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

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT count(1) FROM portfolios "+\
    "JOIN symbol_list ON portfolios.portf_symbol = symbol_list.symbol "+\
    "WHERE symbol_list.uid=" +\
    str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        num_rec = row[0]
    num_rec = round(255 / num_rec, 0)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT portfolios.alloc_fullname, portfolios.order_type, "+\
    "portfolios.dollar_amount, portfolios.symbol, "+\
    "portfolios.strategy_order_type "+\
    "FROM `portfolios` JOIN symbol_list ON "+\
    "portfolios.portf_symbol = symbol_list.symbol "+\
    "WHERE symbol_list.uid=" + str(uid) + " "+\
    "ORDER BY portfolios.dollar_amount"
    cursor.execute(sql)
    res = cursor.fetchall()
    pie_chart_data = ''
    pie_chart_option = ''
    i = 0
    count_buy = 0
    count_sell = 0
    count_wait = 0
    sell_color_r = 255
    sell_color_g = 0
    sell_color_b = 0
    buy_color_r = 198
    buy_color_g = 255
    buy_color_b = 0
    wait_color_r = 220
    wait_color_g = 220
    wait_color_b = 220

    for row in res:
        alloc_fullname = row[0]
        order_type = row[1]
        dollar_amount = row[2]
        alloc_symbol = row[3]
        strategy_order_type = row[4]

        if ((order_type == 'buy' and strategy_order_type == 'short') or\
            (order_type == 'sell' and strategy_order_type == 'long')):
            order_type = 'wait'

        if i == 0:
            pie_chart_data = '["'+\
            alloc_fullname +' ('+\
            alloc_symbol +')'+'", '+\
            str(dollar_amount) +']'
        else:
            pie_chart_data = pie_chart_data + ', ' + '["'+\
            alloc_fullname + ' ('+\
            alloc_symbol +')' +'", '+\
            str(dollar_amount) +']'
        if order_type == 'buy':
            if count_buy > 0:
                if buy_color_b > num_rec:
                    buy_color_r = buy_color_r - num_rec
                if buy_color_b < (255):
                    buy_color_b = buy_color_b + num_rec
            count_buy += 1
            if i == 0:
                pie_chart_option = str(i) +\
                ':{color:"rgb('+\
                str(int(buy_color_r)) +','+\
                str(int(buy_color_g)) +','+\
                str(int(buy_color_b)) +')"}'
            else:
                pie_chart_option = pie_chart_option + ', '+\
                str(i) +':{color:"rgb('+\
                str(int(buy_color_r)) +','+\
                str(int(buy_color_g)) +','+\
                str(int(buy_color_b)) +')"}'
        if order_type == 'sell':
            if count_sell > 0:
                if sell_color_b > num_rec:
                    sell_color_r = sell_color_r - num_rec
                if sell_color_g < (255):
                    sell_color_g = sell_color_g + num_rec
                if sell_color_b < (255):
                    sell_color_b = sell_color_b + num_rec
            count_sell += 1
            if i == 0:
                pie_chart_option = str(i) +':{color:"rgb('+\
                str(int(sell_color_r)) +','+\
                str(int(sell_color_g)) +','+\
                str(int(sell_color_b)) +')"}'
            else:
                pie_chart_option = pie_chart_option + ', '+\
                str(i) +':{color:"rgb('+\
                str(int(sell_color_r)) +','+\
                str(int(sell_color_g)) +','+\
                str(int(sell_color_b)) +')"}'
        if order_type == 'wait':
            count_wait += 1
            if i == 0:
                pie_chart_option = str(i) +':{color:"rgb('+\
                str(int(wait_color_r)) +','+\
                str(int(wait_color_g)) +','+\
                str(int(wait_color_b)) +')"}'
            else:
                pie_chart_option = pie_chart_option + ', '+\
                str(i) +':{color:"rgb('+\
                str(int(wait_color_r)) +','+\
                str(int(wait_color_g)) +','+\
                str(int(wait_color_b)) +')"}'

        i += 1
    cursor.close()
    connection.close()

    pie_chart_title = 'Portfolio Allocation'
    pie_chart_x = "Allocation"
    pie_chart_y = "Dollar Amount"
    pie_chart_font_size = 10
    pie_chart = '' +\
    '        <div class="col-lg-5 col-md-5 col-sm-6 col-xs-12">'+\
    '           <div class="box-part rounded sa-portf-alloc" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
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
    '                           titleTextStyle:{color:'+\
    theme_return_this('"black"', '"white"') +'},'+\
    '                           pieHole: 0.2,'+\
    '                           legend: {position:"none", textStyle:{color:'+\
    theme_return_this('"black"', '"white"') +'} },'+\
    '                           backgroundColor: "transparent",'+\
    '                           pieSliceText: "percentage",'+\
    '                           slices: {' + pie_chart_option  + '},'+\
    '                           legend: {position:"labeled", textStyle: {fontSize: '+\
    str(pie_chart_font_size) +', color:'+ theme_return_this('"black"', '"white"') +'} },'+\
    '                           chartArea:{width:"90%",height:"80%"}'+\
    '                       };'+\
    '                       var chart = '+\
    'new google.visualization.PieChart(document.getElementById("portf_alloc_pie_chart"));'+\
    '                       chart.draw(data, options);'+\
    '                   }'+\
    '               </script>'+\
    '               <div id="portf_alloc_pie_chart" class="sa-chart-hw-90"></div>'+\
    '           </div>'+\
    '        </div>'
    return signal_box + pie_chart
