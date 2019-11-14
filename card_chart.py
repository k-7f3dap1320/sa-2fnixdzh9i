""" Card charts """
from app_cookie import theme_return_this, get_sa_theme
import pymysql.cursors

import datetime
import time
from datetime import timedelta

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def write_func(uid,data,color,minval):
    """ Draw chart within the card """
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
    "      chartArea:{right: '0', width:'90%',height:'80%' },"+\
    "      hAxis: {"+\
    "        textPosition: 'none',"+\
    "        title: '',"+\
    "        gridlines: {"+\
    "            color: 'transparent'"+\
    "        }"+\
    "      },"+\
    "      vAxis: {"+\
    "        viewWindow:{min:"+ str(minval) +", viewWindowMode: 'explicit'}, "+\
    "        title: '',"+\
    "        textStyle: { color:'"+ theme_return_this("#343a40","#ffffff") +"'},"+\
    "        gridlines: {"+\
    "            color: 'transparent'"+\
    "        }"+\
    "      },"+\
    "      colors: ['"+str(color)+"'],"+\
    "      legend: {position: 'none'},"+\
    "      lineWidth: 1,"+\
    "      backgroundColor: 'transparent'"+\
    "    };"+\
    "    var chart = new google.visualization.AreaChart(document.getElementById('chart_div_"+str(uid)+"'));"+\
    "    chart.draw(data, options);"+\
    "  }"+\
    " </script>"
    return f


def get_card_chart(uid,color):
    """ Get card chart """
    d = datetime.datetime.now() - timedelta(days=360)
    d = d.strftime("%Y%m%d")
    data = ""
    minval = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT MIN(price_close) FROM chart_data WHERE uid="+ str(uid) + " ORDER BY price_close LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        minval = row[0]

    sql = "SELECT date, price_close, forecast FROM chart_data WHERE date>="+str(d)+" AND uid="+ str(uid)+" ORDER BY date"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        date = row[0]
        price_close = row[1]
        forecast = row[2]
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        if forecast == 0:
            if data =="":
                data = data + "[new Date("+str(year)+", "+str( int(month) -1 )+", "+str(day)+"),"+str(price_close)+"]"
            else:
                data = data + ",[new Date("+str(year)+", "+str( int(month) -1 )+", "+str(day)+"),"+str(price_close)+"]"
    cr.close()
    connection.close()

    return write_func(uid,data,color,minval)
