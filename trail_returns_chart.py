# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from sa_func import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_chart_data(uid,p):
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT instruments.fullname,instruments.y1, instruments.m6, instruments.m3, instruments.m1, instruments.w1, instruments.unit, instruments.is_benchmark "+\
    "FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        fullname = row[0]
        y1 = row[1]
        m6 = row[2]
        m3 = row[3]
        m1 = row[4]
        w1 = row[5]
        unit = row[6]
        is_benchmark = row[7]

    if unit.lower() == 'pips':
        y1 = int(y1); m6 = int(m6); m3 = int(m3); m1 = int(m1); w1 = int(w1)
    else:
        y1 = round( y1*100 ,2 ); m6 = round( m6*100 ,2 ); m3 = round( m3*100 ,2 ); m1 = round( m1*100 ,2 ); w1 = round( w1*100 ,2 )
        unit = '%'


    cr.close()
    connection.close()

    data = "null,''"
    if p == 'y1':
        if not y1 == 0:
            data = str(y1) + ',"' + str(y1) +' '+ str(unit)  + '"'
    if p == 'm6':
        if not m6 == 0:
            data = str(m6) + ',"' + str(m6) +' '+ str(unit)  + '"'
    if p == 'm3':
        if not m3 == 0:
            data = str(m3) + ',"' + str(m3) +' '+ str(unit)  + '"'
    if p == 'm1':
        if not m1 == 0:
            data = str(m1) + ',"' + str(m1) +' '+ str(unit)  + '"'
    if p == 'w1':
        if not w1 == 0:
            data = str(w1) + ',"' + str(w1) +' '+ str(unit)  + '"'

    return data

def get_trailing_returns(uid):

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname, instruments.is_benchmark, instruments.market, instruments.symbol, instruments.asset_class FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        fullname = row[0].replace("'","")
        is_benchmark = row[1]
        market = row[2]
        symbol_is_portf = row[3]
        asset_class = row[4]

    if symbol_is_portf.find( get_portf_suffix() ) > -1:
        sql = "SELECT date FROM chart_data WHERE uid=" + str(uid) + " ORDER BY date DESC LIMIT 1"
    else:
        sql = "SELECT price_instruments_data.date FROM price_instruments_data JOIN symbol_list "+\
        "ON symbol_list.symbol = price_instruments_data.symbol "+\
        "WHERE symbol_list.uid=" + str(uid) +" ORDER BY date DESC LIMIT 1"

    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        as_date = row[0]

    l_as_date = 'Trailing returns as of '+ as_date.strftime("%d-%b-%Y")

    fontSize = 10
    l_y1 = '1-Year'
    l_m6 = '6-month'
    l_m3 = '3-month'
    l_m1 = '1-month'
    l_w1 = '1-week'

    benchmark_header = ''; benchmark_data_y1 = ''; benchmark_data_m6 = ''; benchmark_data_m3 = ''; benchmark_data_m1 = ''; benchmark_data_w1 = ''

    if not is_benchmark:
        sql = "SELECT symbol_list.uid, instruments.fullname FROM symbol_list JOIN instruments "+\
        "ON symbol_list.symbol = instruments.symbol WHERE instruments.market='"+ str( market ) +"' AND instruments.asset_class='"+ str( asset_class ) +"' AND instruments.is_benchmark=1"
        cr.execute(sql)
        rs = cr.fetchall()
        benchmark_uid = 0
        for row in rs:
            benchmark_uid = row[0]
            benchmark_fullname = row[1].replace("'","")
        if not benchmark_uid == 0:
            benchmark_header = ", ' " + benchmark_fullname + " ', {type: 'string', role: 'annotation'}"
            benchmark_data_y1 = ','+ get_chart_data(benchmark_uid,'y1')
            benchmark_data_m6 = ','+ get_chart_data(benchmark_uid,'m6')
            benchmark_data_m3 = ','+ get_chart_data(benchmark_uid,'m3')
            benchmark_data_m1 = ','+ get_chart_data(benchmark_uid,'m1')
            benchmark_data_w1 = ','+ get_chart_data(benchmark_uid,'w1')



    data = ''+\
    '["'+ l_y1 + '",' + get_chart_data(uid,'y1') + benchmark_data_y1 +']' + ',' +\
    '["'+ l_m6 + '",' + get_chart_data(uid,'m6') + benchmark_data_m6 + ']' + ',' +\
    '["'+ l_m3 + '",' + get_chart_data(uid,'m3') + benchmark_data_m3 + ']' + ',' +\
    '["'+ l_m1 + '",' + get_chart_data(uid,'m1') + benchmark_data_m1 + ']' + ',' +\
    '["'+ l_w1 + '",' + get_chart_data(uid,'w1') + benchmark_data_w1 + ']'

    header = "    ['x', ' " + fullname + " ', {type: 'string', role: 'annotation'}"+ benchmark_header +"  ],"


    chart_content = "" +\
    "<script>" +\
    "google.charts.load('current', {packages: ['corechart', 'bar']});" +\
    "google.charts.setOnLoadCallback(drawAnnotations);" +\
    "function drawAnnotations() {" +\
    "  var data = google.visualization.arrayToDataTable([" +\
    header +\
    data +\
    "  ]);" +\
    "      var options = {" +\
    "       fontSize: "+ str( fontSize ) + "," +\
    "      	legend: 'top'," +\
    "        title: ''," +\
    "        chartArea: {width: '100%'}," +\
    "        annotations: {" +\
    "          alwaysOutside: true," +\
    "          textStyle: {" +\
    "            auraColor: 'none'," +\
    "            color: '#555'" +\
    "          }," +\
    "          boxStyle: {" +\
    "            stroke: '#ccc'," +\
    "            strokeWidth: 1," +\
    "            gradient: {" +\
    "              color1: 'yellow'," +\
    "              color2: 'white'," +\
    "              x1: '0%', y1: '0%'," +\
    "              x2: '100%', y2: '100%'" +\
    "            }" +\
    "          }" +\
    "        }," +\
    "        series: {0:{color:'#497f8c'}, 1:{color: '#c9d6ea'} }," +\
    "        chartArea: {width:'80%',height:'80%'}," +\
    "        hAxis: {" +\
    "          title: '" + l_as_date + "' " +\
    "        }," +\
    "        vAxis: {" +\
    "          title: '' " +\
    "        }" +\
    "      };" +\
    "      var chart = new google.visualization.BarChart(document.getElementById('trail_chart'));" +\
    "      chart.draw(data, options);" +\
    "    }" +\
    "    </script>" +\
    "    <div id='trail_chart' class='sa-chart-hw-290'></div>"

    cr.close()
    connection.close()
    print(chart_content)
    return chart_content
