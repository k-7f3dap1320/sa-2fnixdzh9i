# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


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

    if unit == '%':
        y1 = round( y1*100 ,2 )
        m6 = round( m6*100 ,2 )
        m3 = round( m3*100 ,2 )
        m1 = round( m1*100 ,2 )
        w1 = round( w1*100 ,2 )
    cr.close()
    connection.close()

    if p == 'y1':
        data = str(y1) + ',"' + str(y1) +' '+ str(unit)  + '"'
    if p == 'm6':
        data = str(m6) + ',"' + str(m6) +' '+ str(unit)  + '"'
    if p == 'm3':
        data = str(m3) + ',"' + str(m3) +' '+ str(unit)  + '"'
    if p == 'm1':
        data = str(m1) + ',"' + str(m1) +' '+ str(unit)  + '"'
    if p == 'w1':
        data = str(w1) + ',"' + str(w1) +' '+ str(unit)  + '"'

    return data


def get_trailing_returns(uid):

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        fullname = row[0]

    fontSize = 10
    l_title = fullname + ' trailing returns'
    l_y1 = '1-Year'
    l_m6 = '6-month'
    l_m3 = '3-month'
    l_m1 = '1-month'
    l_w1 = '1-week'

    data = '["'+ l_y1 + '",' + get_chart_data(uid,'y1') +']' + ',' +\
    '["'+ l_m6 + '",' + str(m6) + get_chart_data(uid,'m6') + ']' + ',' +\
    '["'+ l_m3 + '",' + str(m3) + get_chart_data(uid,'m3') + ']' + ',' +\
    '["'+ l_m1 + '",' + str(m1) + get_chart_data(uid,'m1') + ']' + ',' +\
    '["'+ l_w1 + '",' + str(w1) + get_chart_data(uid,'w1') + ']'


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
    "       fontSize: "+ str( fontSize ) + "," +\
    "      	legend: 'none'," +\
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
    "        series: {0:{color:'#497f8c'} }," +\
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
    "    <div id='trail_chart' class='sa-chart-hw-50'></div>"


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
    '               <div><h6>'+ l_title +'</h6></div>'+\
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
