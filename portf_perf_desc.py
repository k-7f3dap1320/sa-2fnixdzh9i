""" Portfolio performance content and description """
import pymysql.cursors
from app_cookie import theme_return_this
from sa_func import get_selected_lang

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_desc_box(uid):
    """ xxx """
    desc_box_title = 'Description & Recommendations'
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.description, instruments.w_forecast_display_info, "+\
    "instruments.account_reference, instruments.unit, instruments.symbol "+\
    "FROM instruments JOIN symbol_list "+\
    "ON instruments.symbol = symbol_list.symbol WHERE symbol_list.uid=" + str(uid)
    cursor.execute(sql)
    res = cursor.fetchall()
    portf_summary = ""
    for row in res:
        portf_summary = row[0]
        portf_forecast = row[1]
        portf_account_ref = row[2]
        portf_unit = row[3]
        portf_symbol = row[4]

    slang = get_selected_lang()
    l_wait = 'wait'
    sql = "SELECT portf_descr, portf_recomm_buy, portf_recomm_sell "+\
    "FROM recommendations WHERE lang ='"+ slang +"' "
    cursor.execute(sql)
    res = cursor.fetchall()
    portf_descr = ''
    portf_recomm_buy = ''
    portf_recomm_sell = ''
    for row in res:
        portf_descr = row[0]
        portf_recomm_buy = row[1]
        portf_recomm_sell = row[2]

    portf_descr = portf_descr.replace('{account_minimum}', str(int(portf_account_ref)))
    portf_descr = portf_descr.replace('{unit}', portf_unit)
    portf_descr = portf_descr.replace('{display_forecast}', str(portf_forecast))

    sql = "SELECT price_close FROM chart_data WHERE uid="+ str(uid) +" ORDER by date DESC LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    portf_last_price = 0
    for row in res:
        portf_last_price = row[0]

    portf_recomm = '<br /><br />'
    sql = 'SELECT order_type, alloc_fullname, entry_level, strategy_order_type FROM portfolios '+\
    "WHERE portf_symbol ='"+ portf_symbol +"'  ORDER BY alloc_fullname"
    cursor.execute(sql)
    res = cursor.fetchall()
    i = 1
    for row in res:
        alloc_order_type = row[0]
        alloc_fullname = row[1]
        alloc_entry_price = row[2]
        alloc_strategy_order_type = row[3]
        added_order = False

        if alloc_order_type.lower() == 'buy' and\
        (alloc_strategy_order_type == 'long/short' or\
         alloc_strategy_order_type == 'long'):
            portf_recomm = portf_recomm  + str(i)+') ' +\
            portf_recomm_buy.replace('{portf_alloc_instr}', alloc_fullname)+ '<br />'
            added_order = True

        if alloc_order_type.lower() == 'sell' and\
        (alloc_strategy_order_type == 'long/short' or\
         alloc_strategy_order_type == 'short'):
            portf_recomm = portf_recomm + str(i)+') ' +\
            portf_recomm_sell.replace('{portf_alloc_instr}', alloc_fullname)+ '<br />'
            added_order = True

        if not added_order:
            portf_recomm = portf_recomm + str(i)+') ' + l_wait + ' ' + alloc_fullname + '<br />'
        i += 1

        portf_recomm = portf_recomm.replace('{portf_alloc_entry_price}', alloc_entry_price)


    portf_descr = portf_descr.replace('{portf_recomm}',
                                      portf_recomm + '<br />')
    portf_descr = portf_descr.replace('{portf_last_price}',
                                      str(round(portf_last_price - portf_account_ref, 2)))

    cursor.close()
    connection.close()

    portf_desc_box = '' +\
    '        <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-portf-perf-portf-chart" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div><h6>'+ desc_box_title +'</h6></div>'+\
    '               <div class="sa-descr-box-sm">'+ portf_summary + ' ' + portf_descr +'</div>'+\
    '            </div>'+\
    '        </div>'

    return portf_desc_box

def get_perf_chart(uid):
    """ xxx """
    l_indexing_in_progress_note = 'Indexing in progress. Data will be available in 10 minutes...'
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
    minval = -9999
    for row in res:
        minval = row[0]

    sql = "SELECT chart_data.symbol, chart_data.date, "+\
    "chart_data.price_close, instruments.fullname, instruments.unit, "+\
    "instruments.account_reference FROM chart_data "+\
    "JOIN instruments ON chart_data.symbol = instruments.symbol "+\
    "WHERE chart_data.uid=" + str(uid) + " ORDER BY chart_data.date"
    cursor.execute(sql)
    res = cursor.fetchall()
    data = ""
    price_close = 0
    portf_unit = ''
    for row in res:
        chart_date = row[1]
        price_close = row[2]
        portf_unit = row[4]

        year = chart_date.strftime("%Y")
        month = chart_date.strftime("%m")
        day = chart_date.strftime("%d")
        if data == "":
            data = data +\
            "[new Date("+\
            str(year)+", "+\
            str(int(month)-1)+", "+\
            str(day)+"),"+str(price_close)+"]"
        else:
            data = data +\
            ",[new Date("+\
            str(year)+", "+\
            str(int(month)-1)+", "+\
            str(day)+"),"+ str(price_close)+"]"


    chart_title = "Portfolio 1-Year Performance"
    haxis = "Date"
    vaxis = "Price (" + portf_unit + ")"
    portf_perf_font_size = 10

    if minval != -9999:
        portf_perf_box = '' +\
        '                   <script>'+\
        '                       google.charts.load("current", {"packages":["corechart"]});'+\
        '                       google.charts.setOnLoadCallback(drawChart);'+\
        '                       function drawChart() {'+\
        '                          var data = new google.visualization.DataTable();'+\
        '                          data.addColumn("date", "'+ haxis +'");'+\
        '                          data.addColumn("number", "'+ vaxis +'");'+\
        '                          data.addRows(['+data+']);'+\
        '                          var options = {'+\
        '                            title: "'+ chart_title +'", '+\
        '                            titleTextStyle: {color: '+\
        theme_return_this('"black"', '"white"') +'},'+\
        '                            fontSize:'+\
        str(portf_perf_font_size) + ', '+\
        '                            legend: {position: "none", textStyle: {color: '+\
        theme_return_this('"black"', '"white"') +'} },'+\
        '                            backgroundColor: "transparent",'+\
        '                            vAxis: {viewWindow:{min: '+\
        str(minval) +', viewWindowMode: "explicit"}, gridlines: { color: "transparent" }'+\
        theme_return_this('', ', textStyle: {color: "white"}') +' },'+\
        '                            hAxis: { gridlines: { count: 4, color: "transparent" } '+\
        theme_return_this('', ', textStyle: {color: "white"}') +' }, '+\
        '                            series:{0: {areaOpacity: 0.3, color: '+\
        theme_return_this('"#17a2b8"', '"#ffffff"') +', lineWidth: 2} },'+\
        '                            chartArea:{width:"90%",height:"80%"}'+\
        '                          };'+\
        '                          var chart = '+\
        'new google.visualization.AreaChart(document.getElementById("portf_perf_chart"));'+\
        '                          chart.draw(data, options);'+\
        '                       }'+\
        '                   </script>'+\
        '               <div id="portf_perf_chart" class="sa-chart-hw-90"></div>'
    else:
        portf_perf_box = ''+\
        '<div class="alert alert-info" role="alert">'+\
        l_indexing_in_progress_note +\
        '</div>'

    cursor.close()
    connection.close()
    return portf_perf_box

def get_chart_box(uid):
    """ xxx """
    chart_1y_perf = get_perf_chart(uid)
    tab_1_label = 'Performance'
    tab_1_link = '#perf'
    tab_1_id = tab_1_link.replace('#', '')
    return_data = '' +\
    '        <div class="col-lg-8 col-md-8 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-portf-perf-portf-chart">'+\
    '                  <ul id="sa-tab-sm" class="nav nav-tabs" role="tablist">'+\
    '                    <li class="nav-item">'+\
    '                      <a class="nav-link active" '+\
    'data-toggle="pill" href="'+\
    tab_1_link +'">'+\
    tab_1_label +'</a>'+\
    '                    </li>'+\
    '                  </ul>'+\
    '                  <div class="tab-content">'+\
    '                      <div id="'+\
    tab_1_id +'" class="tab-pane active" style="height: 325px; '+\
    theme_return_this('', 'background-color: #20124d;') +'" ><br />'+\
        chart_1y_perf +'</div>'+\
    '                  </div>'+\
    '            </div>'+\
    '        </div>'
    #To disable tab: remove the data-toggle="pill"
    return return_data

def get_portf_perf_desc(uid):
    """ xxx """
    return_data = get_desc_box(uid) + ' ' + get_chart_box(uid)
    return return_data
