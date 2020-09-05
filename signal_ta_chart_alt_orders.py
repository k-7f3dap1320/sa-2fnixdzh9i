""" Signal alternative orders and technical analysis section """
import pymysql.cursors
from app_cookie import theme_return_this
from tradingview_chart import get_tradingview_chart
from print_google_ads import print_google_ads
from tradingview_indicators import get_tradingview_indicators

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_alt_orders(uid):
    """ xxx """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT instruments.trade_1_entry, instruments.trade_1_tp, "+\
    "instruments.trade_1_sl, instruments.trade_1_type, "+\
    "instruments.trade_2_entry, instruments.trade_2_tp, "+\
    "instruments.trade_2_sl, instruments.trade_2_type, "+\
    "instruments.trade_3_entry, instruments.trade_3_tp, "+\
    "instruments.trade_3_sl, instruments.trade_3_type, "+\
    "instruments.trade_4_entry, instruments.trade_4_tp, "+\
    "instruments.trade_4_sl, instruments.trade_4_type, "+\
    "instruments.decimal_places FROM instruments "+\
    "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid=" +\
    str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        trade_1_entry = row[0]
        trade_1_tp = row[1]
        trade_1_sl = row[2]
        trade_1_type = row[3]
        trade_2_entry = row[4]
        trade_2_tp = row[5]
        trade_2_sl = row[6]
        trade_2_type = row[7]
        trade_3_entry = row[8]
        trade_3_tp = row[9]
        trade_3_sl = row[10]
        trade_3_type = row[11]
        trade_4_entry = row[12]
        trade_4_tp = row[13]
        trade_4_sl = row[14]
        trade_4_type = row[15]
        decimal_places = row[16]

    cursor.close()
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
    '   <td>'+ str(round(trade_1_entry, decimal_places)) +'</td>'+\
    '   <td>'+ str(round(trade_1_tp, decimal_places)) +'</td>'+\
    '   <td>'+ str(round(trade_1_sl, decimal_places)) +'</td>'+\
    '</tr>'
    # Trade 2
    table_content = table_content +'<tr>'
    if trade_2_type == 'buy':
        table_content = table_content + '<th scope="row">'+ buy_badge +'</th>'
    else:
        table_content = table_content + '<th scope="row">'+ sell_badge +'</th>'
    table_content = table_content +\
    '   <td>'+ str(round(trade_2_entry, decimal_places)) +'</td>'+\
    '   <td>'+ str(round(trade_2_tp, decimal_places)) +'</td>'+\
    '   <td>'+ str(round(trade_2_sl, decimal_places)) +'</td>'+\
    '</tr>'
    # Trade 3
    table_content = table_content +'<tr>'
    if trade_3_type == 'buy':
        table_content = table_content + '<th scope="row">'+ buy_badge +'</th>'
    else:
        table_content = table_content + '<th scope="row">'+ sell_badge +'</th>'
    table_content = table_content +\
    '   <td>'+ str(round(trade_3_entry, decimal_places)) +'</td>'+\
    '   <td>'+ str(round(trade_3_tp, decimal_places)) +'</td>'+\
    '   <td>'+ str(round(trade_3_sl, decimal_places)) +'</td>'+\
    '</tr>'
    # Trade 4
    table_content = table_content +'<tr>'
    if trade_4_type == 'buy':
        table_content = table_content + '<th scope="row">'+ buy_badge +'</th>'
    else:
        table_content = table_content + '<th scope="row">'+ sell_badge +'</th>'
    table_content = table_content +\
    '   <td>'+ str(round(trade_4_entry, decimal_places)) +'</td>'+\
    '   <td>'+ str(round(trade_4_tp, decimal_places)) +'</td>'+\
    '   <td>'+ str(round(trade_4_sl, decimal_places)) +'</td>'+\
    '</tr>'

    return_data = ''+\
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

    return return_data

def get_ta_chart(uid):
    """ xxx """
    return_data = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT price_close FROM chart_data WHERE uid="+\
    str(uid) + " ORDER BY price_close LIMIT 1"

    cursor.execute(sql)
    res = cursor.fetchall()
    minval = -9
    for row in res:
        minval = row[0]
    
    if minval != -9:
        sql = "SELECT symbol, date, price_close, forecast, lt_upper_trend_line, lt_lower_trend_line, "+\
        "st_upper_trend_line, st_lower_trend_line, ma200 FROM chart_data WHERE uid=" + str(uid) +" "+\
        "ORDER BY date "
        cursor.execute(sql)
        res = cursor.fetchall()
        data = ''
        i = 0
        for row in res:
            chart_date = row[1]
            price_close = str(row[2])
            forecast = str(row[3])
            lt_upper_trend_line = str(row[4])
            lt_lower_trend_line = str(row[5])
            st_upper_trend_line = str(row[6])
            st_lower_trend_line = str(row[7])
            ma200 = str(row[8])
    
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
                ma200 = 'null'
    
            if i > 0:
                data = data + ','
    
            data = data + '[new Date('+\
            str(year)+','+\
            str(int(month)-1)+', '+\
            str(day)+')'+','+\
            str(price_close) +','+\
            str(forecast) + ','+\
            str(lt_upper_trend_line) + ','+\
            str(lt_lower_trend_line) + ',' +\
            str(st_upper_trend_line) + ','+\
            str(st_lower_trend_line) + ',' +\
            str(ma200)  + ']'
    
            i += 1
        cursor.close()
        connection.close()
    
        chart_title = 'Technical analysis and Forecast'
        chart_font_size = 10
        l_date = 'Date'
        l_price_close = "price"
        l_forecast = 'Forecast'
        l_lt_up_trend = 'Long-term upper trend line'
        l_lt_low_trend = 'Long-term lower trend line'
        l_st_up_trend = 'Short-term upper trend line'
        l_st_low_trend = 'Short-term lower trend line'
        l_ma200 = 'MA200'
        
        return_data = "" +\
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
        '          title: "'+\
        chart_title +'", '+\
        '          titleTextStyle: {color: '+\
        theme_return_this('"black"', '"white"') +' },'+\
        '          fontSize: '+\
        str(chart_font_size)+','+\
        '          legend: {position:"top" '+\
        theme_return_this('', ', textStyle: {color: "white"}') +'},'+\
        '          vAxis: { viewWindow:{min: '+\
        str(minval) +', viewWindowMode: "explicit"}, gridlines: { color: "transparent" } '+\
        theme_return_this('', ', textStyle: {color: "white"}') +' },'+\
        '          hAxis: { gridlines: { count: 4, color: "transparent" } '+\
        theme_return_this('', ', textStyle: {color: "white"}') +'}, '+\
        '          series:{'+\
        '                   0: {areaOpacity: 0.3, color: '+\
        theme_return_this('"#17a2b8"', '"#ffffff"') +', lineWidth: 2},'+\
        '                   1: {areaOpacity: 0.3, color: "#ff9800", lineWidth: 3},'+\
        '                   2: {areaOpacity: 0, color: '+\
        theme_return_this('"gray"', '"white"') +', lineWidth: 1},'+\
        '                   3: {areaOpacity: 0, color: '+\
        theme_return_this('"gray"', '"white"') +', lineWidth: 1},'+\
        '                   4: {areaOpacity: 0.05, color: '+\
        theme_return_this('"#ff3399"', '"yellow"') +', lineWidth: 2, lineDashStyle:[10,2] },'+\
        '                   5: {areaOpacity: 0.1, color: '+\
        theme_return_this('"#ff3399"', '"yellow"') +', lineWidth: 2, lineDashStyle:[10,2] },'+\
        '                   6: {areaOpacity: 0.05, color: '+\
        theme_return_this('"red"', '"#00f2ff"') +', lineWidth: 1}'+\
        '                  },'+\
        '          chartArea:{width:"90%",height:"80%"},'+\
        '          backgroundColor: "transparent"'+\
        '        };'+\
        '        var chart = new google.visualization.AreaChart(document.getElementById("ta_chart"));'+\
        '        chart.draw(data, options);'+\
        "      }"+\
        "</script>"+\
        '<div id="ta_chart" class="sa-chart-hw-100"></div>'

    return return_data


def get_rsi_chart(uid):
    """ xxx """
    l_indexing_in_progress_note = 'Indexing in progress. Data will be available in 10 minutes...'
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT date, rsi, rsi_oversold, rsi_overbought, forecast "+\
    "FROM chart_data WHERE uid=" +\
    str(uid) + " ORDER BY date"

    cursor.execute(sql)
    res = cursor.fetchall()
    data = ''
    i = 0
    for row in res:
        rsi_date = row[0]
        rsi_value = str(row[1])
        rsi_oversold = str(row[2])
        rsi_overbought = str(row[3])
        forecast = str(row[4])

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

        data = data + '[new Date('+\
        str(year)+','+\
        str(int(month)-1)+', '+\
        str(day)+')'+','+\
        str(rsi_value) +','+\
        str(rsi_overbought)  + ',' +\
        str(rsi_oversold)  + ']'

        i += 1
    cursor.close()
    connection.close()

    chart_title = 'rsi14'
    chart_font_size = 10
    l_date = 'date'
    l_rsi_value = 'rsi14'
    l_rsi_overbought = 'Overbought'
    l_rsi_oversold = 'Oversold'

    if data != '':
        return_data = "" +\
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
        '          vAxis: { gridlines: { color: "transparent" } '+\
        theme_return_this('', ', textStyle: {color: "white"}') + '},'+\
        '          hAxis: { gridlines: { count: 4 }' +\
        theme_return_this('', ', textStyle: {color: "white"}') + ' }, '+\
        '          series:{'+\
        '                   0: {areaOpacity: 0.3, color: '+\
        theme_return_this('"#17a2b8"', '"#00fbff"') +', lineWidth: 1},'+\
        '                   1: {areaOpacity: 0, color: "red", lineWidth: 1},'+\
        '                   2: {areaOpacity: 0.05, color: "green", lineWidth: 1}'+\
        '                  },'+\
        '          chartArea:{width:"90%",height:"80%"},'+\
        '          backgroundColor: "transparent"'+\
        '        };'+\
        '        var chart = '+\
        'new google.visualization.AreaChart(document.getElementById("rsi_chart"));'+\
        '        chart.draw(data, options);'+\
        "      }"+\
        "</script>"+\
        '<div id="rsi_chart" class="sa-chart-hw-100-rsi"></div>'
    else:
        return_data = '' +\
        '<div class="alert alert-info" role="alert">'+\
        l_indexing_in_progress_note +\
        '</div>'

    return return_data

def get_sign_ta_chart_alt_orders(uid):
    """ xxx """
    signal_box = ''
    tech_chart = ''
    signal_box_title = 'Alternative Orders'

    signal_box = '' +\
    '        <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">'+\
    '            <div class="box-part rounded sa-signal-alt-ord-prf" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div><h6>'+\
    signal_box_title +'</h6></div>'+\
    get_alt_orders(uid) +\
    '            </div>'+\
    '            <div class=" rounded sa-signal-alt-ord-prf  sa-signal-ads" '+\
    'style="height: 300px;">'+\
    print_google_ads('rectangle', 'left') +\
    '            </div>'+\
    '        </div>'

    tab_1_label = 'Technical Levels'
    tab_1_link = '#ta'
    tab_1_id = 'ta'
    tab_2_label = 'Technical analysis'
    tab_2_link = '#ia'
    tab_2_id = 'ia'
    tab_3_label = 'Live chart'
    tab_3_link = '#chart'
    tab_3_id = 'chart'

    tech_chart = '' +\
    '<div class="col-lg-9 col-md-6 col-sm-6 col-xs-12">'+\
    '   <div class="box-part rounded sa-signal-ta-chart">'+\
    ''+\
    '<ul id="sa-tab-sm" class="nav nav-tabs" role="tablist">'+\
    '   <li class="nav-item">'+\
    '      <a class="nav-link active" data-toggle="pill" href="'+\
    tab_1_link +'">'+ tab_1_label +'</a>'+\
    '   </li>'+\
    '   <li class="nav-item">'+\
    '      <a class="nav-link" data-toggle="pill" href="'+\
    tab_2_link +'">'+ tab_2_label +'</a>'+\
    '   </li>'+\
    '   <li class="nav-item">'+\
    '      <a class="nav-link" data-toggle="pill" href="'+\
    tab_3_link +'">'+ tab_3_label +'</a>'+\
    '   </li>'+\
    '</ul>'+\
    ''+\
    '<div class="tab-content">'+\
    '   <div id="'+\
    tab_1_id +'" class="tab-pane active" style="'+\
    theme_return_this('', 'background-color: #20124d;') +'"><br />'+\
    get_ta_chart(uid) +\
    get_rsi_chart(uid) +\
    '   </div>'+\
    '   <div id="'+\
    tab_2_id +'" style="height: 520px" class="tab-pane fade"><br />'+\
    '      <div style="height: 99%; width:99%">'+\
    get_tradingview_indicators(uid, '100%', '100%') +\
    '      </div>'+\
    '   </div>'+\
    '   <div id="'+\
    tab_3_id +'" style="height: 520px" class="tab-pane fade"><br />'+\
    '     <div style="height: 510px; width: 99%">'+\
    get_tradingview_chart(uid, '510', '"100%"','1') +\
    '     </div>'+\
    '   </div>'+\
    '</div>'+\
    '</div>'+\
    '</div>'
    #To disable tab: remove the data-toggle="pill"
    return signal_box + tech_chart
