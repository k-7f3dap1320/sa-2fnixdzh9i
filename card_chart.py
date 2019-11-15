""" Card charts """
import datetime
from datetime import timedelta
import pymysql.cursors
from app_cookie import theme_return_this
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def write_func(uid, data, color, minval):
    """ Draw chart within the card """
    funct = ""+\
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
    "        textStyle: { color:'"+ theme_return_this("#343a40", "#ffffff") +"'},"+\
    "        gridlines: {"+\
    "            color: 'transparent'"+\
    "        }"+\
    "      },"+\
    "      colors: ['"+str(color)+"'],"+\
    "      legend: {position: 'none'},"+\
    "      lineWidth: 1,"+\
    "      backgroundColor: 'transparent'"+\
    "    };"+\
    "    var chart = new google.visualization.AreaChart(document.getElementById('chart_div_"+\
    str(uid)+"'));"+\
    "    chart.draw(data, options);"+\
    "  }"+\
    " </script>"
    return funct


def get_card_chart(uid, color):
    """ Get card chart """
    date_minus_year = datetime.datetime.now() - timedelta(days=360)
    date_minus_year = date_minus_year.strftime("%Y%m%d")
    data = ""
    minval = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT MIN(price_close) FROM chart_data WHERE uid="+\
    str(uid) + " ORDER BY price_close LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        minval = row[0]

    sql = "SELECT date, price_close, forecast FROM chart_data WHERE date>="+\
    str(date_minus_year)+" AND uid="+ str(uid)+" ORDER BY date"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        date = row[0]
        price_close = row[1]
        forecast = row[2]
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        if forecast == 0:
            if data == "":
                data = data +\
                "[new Date("+str(year)+", "+\
                str(int(month) -1)+", "+\
                str(day)+"),"+str(price_close)+"]"
            else:
                data = data + ",[new Date("+\
                str(year)+", "+\
                str(int(month) -1)+", "+\
                str(day)+"),"+str(price_close)+"]"
    cursor.close()
    connection.close()

    return write_func(uid, data, color, minval)
