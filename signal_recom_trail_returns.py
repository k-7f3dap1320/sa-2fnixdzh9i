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
    sql = "SELECT instruments.fullname, instruments.y1, instruments.m6, instruments.m3, instruments.m1, instruments.w1, instruments.unit "+\
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

    fontSize = 10
    l_title = fullname + ' trailing returns in ('+ str( unit ) +')'
    l_y1 = '1-Year'
    l_m6 = '6-month'
    l_m3 = '3-month'
    l_m1 = '1-month'
    l_w1 = '1-week'

    data = '["'+ l_y1 + '",' + str(y1) + ',"' + str(y1) +' '+ str(unit)  + '"]' + ',' +\
    '["'+ l_m6 + '",' + str(m6) + ',"' + str(y1) +' '+ str(unit) + '"]' + ',' +\
    '["'+ l_m3 + '",' + str(m3) + ',"' + str(m3) +' '+ str(unit) + '"]' + ',' +\
    '["'+ l_m1 + '",' + str(m1) + ',"' + str(m1) +' '+ str(unit) + '"]' + ',' +\
    '["'+ l_w1 + '",' + str(w1) + ',"' + str(w1) +' '+ str(unit) + '"]'


    chart_content = "" +\
    "<script>" +\
    "google.charts.load('current', {packages: ['corechart', 'bar']});" +\
    "google.charts.setOnLoadCallback(drawAnnotations);" +\
    "function drawAnnotations() {" +\
    "  var data = google.visualization.arrayToDataTable([" +\
    "    ['instrument', 'returns', {type: 'string', role: 'annotation'}]," +\
    data +\
    "  ]);" +\
    "      var options = {" +\
    "      	legend: 'bottom'," +\
    "        title: ''," +\
    "        chartArea: {width: '50%'}," +\
    "        annotations: {" +\
    "          alwaysOutside: true," +\
    "          textStyle: {" +\
    "            fontSize: "+ str(fontSize) +"," +\
    "            auraColor: 'none'," +\
    "            color: '#555'" +\
    "          }," +\
    "          boxStyle: {" +\
    "            stroke: '#ccc'," +\
    "            strokeWidth: 1," +\
    "            gradient: {" +\
    "              color1: 'yellow'," +\
    "              x1: '0%', y1: '0%'," +\
    "              x2: '100%', y2: '100%'" +\
    "            }" +\
    "          }" +\
    "        }," +\
    "        series: {0:{color:'pink'} }," +\
    "        hAxis: {" +\
    "          title: '' " +\
    "        }," +\
    "        vAxis: {" +\
    "          title: '' " +\
    "        }" +\
    "      };" +\
    "      var chart = new google.visualization.BarChart(document.getElementById('trail_chart'));" +\
    "      chart.draw(data, options);" +\
    "    }" +\
    "    </script>" +\
    "    <div id='trail_chart' class='sa-chart-hw-100'></div>"


    trail_chart = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    chart_content +\
    '            </div>'+\
    '        </div>'


    cr.close()
    connection.close()

    return trail_chart



def get_recomm(uid):

    recomm_box = ''

    '''
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT "
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        symbol = row[0]
    '''

    l_title = 'Technical analysis & recommendation'

    recomm_box = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part">'+\
    '               <div><h6>'+ l_title +'</h6></div>'
    '            </div>'+\
    '        </div>'

    '''
    cr.close()
    connection.close()
    '''

    return recomm_box



def get_sign_recommend_trail_returns(uid):

    r =''

    try:

        r = get_recomm(uid) + get_trailing_returns(uid)

    except Exception as e: print(e)

    return r
