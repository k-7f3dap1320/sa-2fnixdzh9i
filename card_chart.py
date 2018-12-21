# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

import datetime
import time
from datetime import timedelta

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def write_func(uid,data,color):
    f =""+\
    "<script>"+\
    "google.charts.load('current', {packages: ['corechart', 'line']});"+\
    "google.charts.setOnLoadCallback(drawChart_"+str(uid)+");"+\
    "function drawChart_"+str(uid)+"() {"+\
    "    var data = new google.visualization.DataTable();"+\
    "    data.addColumn('date', 'date');"+\
    "    data.addColumn('number', 'price');"+\
    "    data.addRows(["+data+"]);"+\
    "    var options = {"+\
    "      hAxis: {"+\
    "        textPosition: 'none',"+\
    "        title: '',"+\
    "        gridlines: {"+\
    "            color: 'transparent'"+\
    "        }"+\
    "      },"+\
    "      vAxis: {"+\
    "        title: '',"+\
    "        gridlines: {"+\
    "            color: 'transparent'"+\
    "        }"+\
    "      },"+\
    "      colors: ['"+str(color)+"'],"+\
    "      legend: {position: 'none'},"+\
    "      lineWidth: 2"+\
    "    };"+\
    "    var chart = new google.visualization.LineChart(document.getElementById('chart_div_"+str(uid)+"'));"+\
    "    chart.draw(data, options);"+\
    "  }"+\
    " </script>"
    return f


def get_card_chart(uid,color):

    d = datetime.datetime.now() - timedelta(days=360)
    d = d.strftime("%Y%m%d")
    data = ""

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT date, price_close FROM chart_data WHERE date>="+str(d)+" AND uid="+ str(uid)+" ORDER BY date"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            date = row[0]
            price_close = row[1]
            year = date.strftime("%Y")
            month = date.strftime("%m")
            day = date.strftime("%d")
            if data =="":
                data = data + "[new Date("+str(year)+", "+str( int(month) -1 )+", "+str(day)+"),"+str(price_close)+"]"
            else:
                data = data + ",[new Date("+str(year)+", "+str( int(month) -1 )+", "+str(day)+"),"+str(price_close)+"]"
        cr.close()
        connection.close()
    except Exception as e: print(e)

    return write_func(uid,data,color)
