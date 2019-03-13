# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from tradingview_chart import *


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
    for row in rs:
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
    '<table class="table table-sm table-hover sa-table-sm">'+\
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

def get_ta_chart(uid):
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT price_close FROM chart_data WHERE uid="+ str(uid) + " ORDER BY price_close LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        minval = row[0]

    sql = "SELECT symbol, date, price_close, forecast, lt_upper_trend_line, lt_lower_trend_line, "+\
    "st_upper_trend_line, st_lower_trend_line, ma200 FROM chart_data WHERE uid=" + str(uid) +" "+\
    "ORDER BY date "
    cr.execute(sql)
    rs = cr.fetchall()
    data = ''
    i = 0
    for row in rs:
        symbol = row[0]; chart_date = row[1]; price_close = str( row[2] ) ; forecast = str( row[3] )
        lt_upper_trend_line = str( row[4] ) ; lt_lower_trend_line = str( row[5] )
        st_upper_trend_line = str( row[6] ); st_lower_trend_line = str( row[7] ) ; ma200 = str( row[8] )

        year = chart_date.strftime("%Y")
        month = chart_date.strftime("%m")
        day = chart_date.strftime("%d")

        if forecast == '0' or forecast == '0.0':
            forecast = 'null'
        if price_close == '0' or price_close == '0.0' or forecast != 'null':
            price_close = 'null'
        if lt_upper_trend_line == '0' or lt_upper_trend_line == '0.0':
            lt_upper_trend_line = 'null'
        if lt_lower_trend_line == '0' or lt_lower_trend_line == '0.0':
            lt_lower_trend_line = 'null'
        if st_upper_trend_line == '0' or st_upper_trend_line == '0.0':
            st_upper_trend_line = 'null'
        if st_lower_trend_line == '0' or st_lower_trend_line == '0.0':
            st_lower_trend_line = 'null'
        if ma200 == '0' or ma200 == '0.0':
            ma200 == 'null'

        if i > 0:
            data = data + ','
        data = data + '[new Date('+str(year)+','+str(int(month)-1 )+', '+str(day)+')'+','+ str(price_close) +','+ str(forecast) + ','+\
        str(lt_upper_trend_line) + ','+ str(lt_lower_trend_line) + ',' +\
        str(st_upper_trend_line) + ','+ str(st_lower_trend_line) + ',' + str(ma200)  + ']'

        i += 1

    chart_title = 'Technical analysis and Forecast'
    chart_font_size = 10
    l_symbol = 'Symbol'; l_date = 'Date'; l_price_close = "price"; l_forecast = 'Forecast'
    l_lt_up_trend = 'Long-term upper trend line'; l_lt_low_trend = 'Long-term lower trend line'
    l_st_up_trend = 'Short-term upper trend line'; l_st_low_trend = 'Short-term lower trend line'
    l_ma200 = 'MA200'

    r = "" +\
    "<script>"+\
    "      google.charts.load('current', {'packages':['corechart']});"+\
    "      google.charts.setOnLoadCallback(drawChart);"+\
    "      function drawChart() {"+\
    "        var data = new google.visualization.DataTable();"+\
    "        data.addColumn('date', '"+ l_date +"');"+\
    "        data.addColumn('number', '"+ l_price_close +"');"+\
    "        data.addColumn('number', '"+ l_forecast +"');"+\
    "        data.addColumn('number', '"+ l_lt_up_trend +"');"+\
    "        data.addColumn('number', '"+ l_lt_low_trend +"');"+\
    "        data.addColumn('number', '"+ l_st_up_trend +"');"+\
    "        data.addColumn('number', '"+ l_st_low_trend +"');"+\
    "        data.addColumn('number', '"+ l_ma200 +"');"+\
    "        data.addRows(["+data+"]);"+\
    '        var options = {'+\
    '          title: "'+ chart_title +'", '+\
    '          fontSize: '+ str(chart_font_size)+','+\
    '          legend: "top",'+\
    '          vAxis: { viewWindow:{min: '+ str( minval ) +', viewWindowMode: "explicit"}, gridlines: { color: "transparent" } },'+\
    '          hAxis: { gridlines: { count: 4 } }, '+\
    '          series:{'+\
    '                   0: {areaOpacity: 0.1, color: "black", lineWidth: 1},'+\
    '                   1: {areaOpacity: 0.2, color: "#ff9800", lineWidth: 3},'+\
    '                   2: {areaOpacity: 0, color: "#47808d", lineWidth: 2},'+\
    '                   3: {areaOpacity: 0, color: "#47808d", lineWidth: 2},'+\
    '                   4: {areaOpacity: 0.05, color: "#ff3399", lineWidth: 2, lineDashStyle:[10,2] },'+\
    '                   5: {areaOpacity: 0.05, color: "#ff3399", lineWidth: 2, lineDashStyle:[10,2] },'+\
    '                   6: {areaOpacity: 0.05, color: "red", lineWidth: 1}'+\
    '                  },'+\
    '          chartArea:{width:"90%",height:"80%"}'+\
    '        };'+\
    '        var chart = new google.visualization.AreaChart(document.getElementById("ta_chart"));'+\
    '        chart.draw(data, options);'+\
    "      }"+\
    "</script>"+\
    '<div id="ta_chart" class="sa-chart-hw-100"></div>'

    return r


def get_rsi_chart(uid):
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT date, rsi, rsi_oversold, rsi_overbought, forecast FROM chart_data WHERE uid=" + str(uid) + " ORDER BY date"
    cr.execute(sql)
    rs = cr.fetchall()
    data = ''
    i = 0
    for row in rs:
        rsi_date = row[0]
        rsi_value = str( row[1] )
        rsi_oversold = str( row[2] )
        rsi_overbought = str( row[3] )
        forecast = str( row[4] )

        year = rsi_date.strftime("%Y")
        month = rsi_date.strftime("%m")
        day = rsi_date.strftime("%d")

        if rsi_value == '0' or rsi_value == '0.0':
            rsi_value = 'null'
        if rsi_oversold == '0' or rsi_oversold == '0.0':
            rsi_oversold = 'null'
        if rsi_overbought == '0' or rsi_overbought == '0.0':
            rsi_overbought = 'null'
        if forecast == '0' or forecast == '0.0':
            forecast = 'null'
        if not forecast == 'null':
            rsi_value = 'null'

        if i > 0:
            data = data + ','
        data = data + '[new Date('+str(year)+','+str(int(month)-1 )+', '+str(day)+')'+','+ str(rsi_value) +','+ str(rsi_overbought)  + ',' + str(rsi_oversold)  + ']'

        i += 1

    chart_title = 'rsi14'
    chart_font_size = 10
    l_date = 'date'; l_rsi_value = 'rsi14'; l_rsi_overbought = 'Overbought'; l_rsi_oversold = 'Oversold'

    r = "" +\
    "<script>"+\
    "      google.charts.load('current', {'packages':['corechart']});"+\
    "      google.charts.setOnLoadCallback(drawChart);"+\
    "      function drawChart() {"+\
    "        var data = new google.visualization.DataTable();"+\
    "        data.addColumn('date', '"+ l_date +"');"+\
    "        data.addColumn('number', '"+ l_rsi_value +"');"+\
    "        data.addColumn('number', '"+ l_rsi_overbought +"');"+\
    "        data.addColumn('number', '"+ l_rsi_oversold +"');"+\
    "        data.addRows(["+data+"]);"+\
    '        var options = {'+\
    '          title: "'+ chart_title +'", '+\
    '          fontSize: '+ str(chart_font_size)+','+\
    '          legend: "top",'+\
    '          vAxis: { gridlines: { color: "transparent" } },'+\
    '          hAxis: { gridlines: { count: 4 } }, '+\
    '          series:{'+\
    '                   0: {areaOpacity: 0.1, color: "black", lineWidth: 1},'+\
    '                   1: {areaOpacity: 0, color: "red", lineWidth: 1},'+\
    '                   2: {areaOpacity: 0.05, color: "green", lineWidth: 1}'+\
    '                  },'+\
    '          chartArea:{width:"90%",height:"80%"}'+\
    '        };'+\
    '        var chart = new google.visualization.AreaChart(document.getElementById("rsi_chart"));'+\
    '        chart.draw(data, options);'+\
    "      }"+\
    "</script>"+\
    '<div id="rsi_chart" class="sa-chart-hw-100-rsi"></div>'

    return r

def get_profile_content(uid):

    r = ''

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol_list.uid, instruments.fullname, instruments.description "+\
        "FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
        "WHERE symbol_list.uid=" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            uid = row[0]
            fullname = row[1].replace("'","")
            description = row[2]

        box_title = fullname + ' profile'

        if len(description) < 1:
            box_description = 'No description available for this instrument.'
        else:
            box_description = description

        r = ''+\
        '   <div><h6>'+ box_title + '</h6></div>'+\
        '   <div>'+ box_description +'</div>'

        cr.close()
        connection.close()

    except Exception as e: print(e)

    return r

def get_sign_ta_chart_alt_orders(uid):

    try:
        signal_box = ''; tech_chart = ''


        signal_box_title = 'Alternative Orders'
        signal_box = '' +\
        '        <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">'+\
        '            <div class="box-part rounded sa-signal-alt-ord-prf">'+\
        '               <div><h6>'+ signal_box_title +'</h6></div>'+\
        get_alt_orders(uid) +\
        '            </div>'+\
        '            <div class="box-part rounded sa-signal-alt-ord-prf">'+\
        get_profile_content(uid) +\
        '            </div>'+\
        '        </div>'

        tab_1_label = 'Technical analysis'; tab_1_link = '#ta'; tab_1_id = 'ta'
        tab_2_label = 'Performance'; tab_2_link = '#perf'; tab_2_id = 'perf'
        tab_3_label = 'Live chart'; tab_3_link = '#chart'; tab_3_id = 'chart'


        tech_chart = '' +\
        '        <div class="col-lg-9 col-md-6 col-sm-6 col-xs-12">'+\
        '            <div class="box-part rounded sa-signal-ta-chart">'+\
        '                  <ul id="sa-tab-sm" class="nav nav-pills" role="tablist">'+\
        '                    <li class="nav-item">'+\
        '                      <a class="nav-link active" data-toggle="pill" href="'+ tab_1_link +'">'+ tab_1_label +'</a>'+\
        '                    </li>'+\
        '                    <li class="nav-item">'+\
        '                      <a class="nav-link" data-toggle="pill" href="'+ tab_2_link +'">'+ tab_2_label +'</a>'+\
        '                    </li>'+\
        '                    <li class="nav-item">'+\
        '                      <a class="nav-link" data-toggle="pill" href="'+ tab_3_link +'">'+ tab_3_label +'</a>'+\
        '                    </li>'+\
        '                  </ul>'+\
        '                  <div class="tab-content">'+\
        '                      <div id="'+ tab_1_id +'" class="container tab-pane active"><br />'+ get_ta_chart(uid) + get_rsi_chart(uid) + '</div>'+\
        '                      <div id="'+ tab_2_id +'" class="container tab-pane fade"><br />'+ 'This module is not yet available.' +'</div>'+\
        '                      <div id="'+ tab_3_id +'" class="container tab-pane fade"><br /><div style="height: 88%">'+ get_tradingview_chart(uid) +'</div></div>'+\
        '                  </div>'+\
        '            </div>'+\
        '        </div>'
        #To disable tab: remove the data-toggle="pill"
    except Exception as e: print(e)

    return signal_box + tech_chart
