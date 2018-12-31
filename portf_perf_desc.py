# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
from sa_func import *
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_desc_box(uid):

    desc_box_title = 'Description & Recommendations'
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.description, instruments.w_forecast_display_info, instruments.account_reference, instruments.unit, instruments.symbol from instruments JOIN symbol_list "+\
    "ON instruments.symbol = symbol_list.symbol WHERE symbol_list.uid=" + str(uid)
    print(sql)
    cr.execute(sql)
    rs = cr.fetchall()
    portf_summary = ""
    for row in rs:
        portf_summary = row[0]
        portf_forecast = row[1]
        portf_account_ref = row[2]
        portf_unit = row[3]
        portf_symbol = row[4]

    slang = get_selected_lang()
    sql = "SELECT portf_descr, portf_recomm_buy, portf_recomm_sell FROM recommendations WHERE lang ='"+ slang +"' "
    cr.execute(sql)
    rs = cr.fetchall()
    portf_descr =''; portf_recomm_buy =''; portf_recomm_sell = ''
    for row in rs:
        portf_descr = row[0]
        portf_recomm_buy = row[1]
        portf_recomm_sell = row[2]

    portf_descr = portf_descr.replace('{account_minimum}',str(int( portf_account_ref) ) )
    portf_descr = portf_descr.replace('{unit}', portf_unit)
    portf_descr = portf_descr.replace('{display_forecast}',str(portf_forecast) )

    sql ="SELECT price_close FROM chart_data WHERE uid="+ str(uid) +" ORDER by date DESC LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        portf_last_price = row[0]

    #{portf_recomm} = "buy {portf_alloc_instr} below {portf_alloc_entry_price}"
    #{portf_recomm} = "sell {portf_alloc_instr} above {portf_alloc_entry_price}"
    portf_recomm = '<br /><br />'
    sql = 'SELECT order_type, alloc_fullname, entry_level FROM portfolios '+\
    "WHERE portf_symbol ='"+ portf_symbol +"'  ORDER BY alloc_fullname"
    cr.execute(sql)
    rs = cr.fetchall()
    i = 1
    for row in rs:
        alloc_order_type = row[0]
        alloc_fullname = row[1]
        alloc_entry_price = row[2]

        if alloc_order_type.lower() == 'buy':
            portf_recomm = portf_recomm  + str(i)+') ' + portf_recomm_buy.replace('{portf_alloc_instr}',alloc_fullname)+ '<br />'
        if alloc_order_type.lower() == 'sell':
            portf_recomm = portf_recomm + str(i)+') ' + portf_recomm_sell.replace('{portf_alloc_instr}',alloc_fullname)+ '<br />'

        portf_recomm = portf_recomm.replace('{portf_alloc_entry_price}', alloc_entry_price)
        i += 1

    portf_descr = portf_descr.replace('{portf_recomm}', portf_recomm + '<br />')
    portf_descr = portf_descr.replace('{portf_last_price}', str(portf_last_price) )

    cr.close()
    connection.close()

    portf_desc_box = '' +\
    '        <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">'+\
    '            <div class="box-part sa-portf-perf-portf-chart">'+\
    '               <div><h6>'+ desc_box_title +'</h6></div>'+\
    '               <div class="sa-descr-box-sm">'+ portf_summary + ' ' + portf_descr +'</div>'+\
    '            </div>'+\
    '        </div>'

    return portf_desc_box

def get_perf_chart(uid):

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT chart_data.symbol, chart_data.date, chart_data.price_close, instruments.fullname, instruments.unit, instruments.account_reference FROM chart_data "+\
    "JOIN instruments ON chart_data.symbol = instruments.symbol "+\
    "WHERE chart_data.uid=" + str(uid) + " ORDER BY chart_data.date"
    print(sql)
    cr.execute(sql)
    rs = cr.fetchall()
    data = ""
    for row in rs:
        symbol = row[0]
        chart_date = row[1]
        price_close = row[2]
        fullname = row[3]
        portf_unit = row[4]
        account_reference = row[5]

        year = chart_date.strftime("%Y")
        month = chart_date.strftime("%m")
        day = chart_date.strftime("%d")
        if data =="":
            data = data + "[new Date("+str(year)+", "+str(int(month)-1 )+", "+str(day)+"),"+str(price_close)+"]"
        else:
            data = data + ",[new Date("+str(year)+", "+str( int(month)-1 )+", "+str(day)+"),"+str(price_close)+"]"


    chart_title = "Portfolio 1-Year Performance"
    hAxis = "Date"; vAxis = "Price (" + portf_unit + ")"
    profit_1Y = price_close
    portf_perf_font_size = 10

    portf_perf_box = '' +\
    '                   <script>'+\
    '                       google.charts.load("current", {"packages":["corechart"]});'+\
    '                       google.charts.setOnLoadCallback(drawChart);'+\
    '                       function drawChart() {'+\
    '                          var data = new google.visualization.DataTable();'+\
    '                          data.addColumn("date", "'+ hAxis +'");'+\
    '                          data.addColumn("number", "'+ vAxis +'");'+\
    '                          data.addRows(['+data+']);'+\
    '                          var options = {'+\
    '                            title: "'+ chart_title +'", '+\
    '                            fontSize:'+ str(portf_perf_font_size) + ', '+\
    '                            legend: "none",'+\
    '                            vAxis: {viewWindow:{min: 1000, viewWindowMode: "explicit"}, minValue: '+ str(account_reference / 2 ) +', gridlines: { color: "transparent" } },'+\
    '                            hAxis: { gridlines: { count: 4 } }, '+\
    '                            series:{0: {areaOpacity: 0.1, color: "black", lineWidth: 1} },'+\
    '                            chartArea:{width:"90%",height:"80%"}'+\
    '                          };'+\
    '                          var chart = new google.visualization.AreaChart(document.getElementById("portf_perf_chart"));'+\
    '                          chart.draw(data, options);'+\
    '                       }'+\
    '                   </script>'+\
    '               <div id="portf_perf_chart" class="sa-chart-hw-90"></div>'
    cr.close()
    connection.close()
    return portf_perf_box

def get_chart_box(uid):
    chart_1y_perf = get_perf_chart(uid)

    tab_1_label = 'Performance'; tab_1_link = '#perf'; tab_1_id = tab_1_link.replace('#','')
    tab_2_label = 'Portfolio vs Benchmark'; tab_2_link = '#bench'; tab_2_id = tab_2_link.replace('#','')

    r = '' +\
    '        <div class="col-lg-8 col-md-8 col-sm-12 col-xs-12">'+\
    '            <div class="box-part sa-portf-perf-portf-chart">'+\
    '                  <ul id="sa-tab-sm" class="nav nav-pills" role="tablist">'+\
    '                    <li class="nav-item">'+\
    '                      <a class="nav-link active" data-toggle="pill" href="'+ tab_1_link +'">'+ tab_1_label +'</a>'+\
    '                    </li>'+\
    '                    <li class="nav-item">'+\
    '                      <a class="nav-link" href="'+ tab_2_link +'">'+ tab_2_label +'</a>'+\
    '                    </li>'+\
    '                  </ul>'+\
    '                  <div class="tab-content">'+\
    '                      <div id="'+ tab_1_id +'" class="container tab-pane active">'+ chart_1y_perf +'</div>'+\
    '                      <div id="'+ tab_2_id +'" class="container tab-pane fade">'+'</div>'+\
    '                  </div>'+\
    '            </div>'+\
    '        </div>'
    #To disable tab: remove the data-toggle="pill"


    return r

def get_portf_perf_desc(uid):

    try:
        r = get_desc_box(uid) + ' ' + get_chart_box(uid)
    except Exception as e: print(e)

    return r
