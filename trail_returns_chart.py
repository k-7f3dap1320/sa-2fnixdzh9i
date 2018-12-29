# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_trailing_returns(uid):

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname, instruments.is_benchmark, instruments.market FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        fullname = row[0]
        is_benchmark = row[1]
        market = row[2]


    fontSize = 10
    l_y1 = '1-Year'
    l_m6 = '6-month'
    l_m3 = '3-month'
    l_m1 = '1-month'
    l_w1 = '1-week'

    benchmark_header = ''; benchmark_data_y1 = ''; benchmark_data_m6 = ''; benchmark_data_m3 = ''; benchmark_data_m1 = ''; benchmark_data_w1 = ''

    if not is_benchmark:
        sql = "SELECT symbol_list.uid, instruments.fullname FROM symbol_list JOIN instruments "+\
        "ON symbol_list.symbol = instruments.symbol WHERE instruments.market='"+ str( market ) +"' AND instruments.is_benchmark=1"
        cr.execute(sql)
        rs = cr.fetchall()
        benchmark_uid = 0
        for row in rs:
            benchmark_uid = row[0]
            benchmark_fullname = row[1]
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
    "        chartArea: {width: '50%'}," +\
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

    return chart_content
