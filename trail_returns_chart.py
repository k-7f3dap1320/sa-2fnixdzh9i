""" Trail returns barchart """
import pymysql.cursors
from app_cookie import theme_return_this
from sa_func import get_portf_suffix
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_minmax(uid, what):
    """ xxx """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT instruments.y1, instruments.m6, instruments.m3, "+\
    "instruments.m1, instruments.w1, instruments.unit "+\
    "FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid=" + str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()

    for row in res:
        y_1 = row[0]
        m_6 = row[1]
        m_3 = row[2]
        m_1 = row[3]
        w_1 = row[4]
        unit = row[5]

    margin = 0
    if unit.lower() != 'pips':
        y_1 = y_1 * 100
        m_6 = m_6 * 100
        m_3 = m_3 * 100
        m_1 = m_1 * 100
        w_1 = w_1 * 100
        margin = 0.05
    else:
        margin = 20

    list_val = [y_1, m_6, m_3, m_1, w_1]
    if what == 'min':
        data = min(list_val) - margin
    if what == 'max':
        data = max(list_val) + margin

    cursor.close()
    connection.close()
    return data

def get_chart_data(uid, period):
    """ xxx """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT instruments.fullname,instruments.y1, instruments.m6, "+\
    "instruments.m3, instruments.m1, instruments.w1, instruments.unit, instruments.is_benchmark "+\
    "FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid=" + str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()

    for row in res:
        y_1 = row[1]
        m_6 = row[2]
        m_3 = row[3]
        m_1 = row[4]
        w_1 = row[5]
        unit = row[6]

    if unit.lower() == 'pips':
        y_1 = int(y_1)
        m_6 = int(m_6)
        m_3 = int(m_3)
        m_1 = int(m_1)
        w_1 = int(w_1)
    else:
        y_1 = round(y_1 * 100, 2)
        m_6 = round(m_6 * 100, 2)
        m_3 = round(m_3 * 100, 2)
        m_1 = round(m_1 * 100, 2)
        w_1 = round(w_1 * 100, 2)
        unit = '%'

    cursor.close()
    connection.close()

    data = "null,''"
    if period == 'y1':
        if y_1 != 0:
            data = str(y_1) + ',"' + str(y_1) +' '+ str(unit)  + '"'
    if period == 'm6':
        if m_6 != 0:
            data = str(m_6) + ',"' + str(m_6) +' '+ str(unit)  + '"'
    if period == 'm3':
        if m_3 != 0:
            data = str(m_3) + ',"' + str(m_3) +' '+ str(unit)  + '"'
    if period == 'm1':
        if m_1 != 0:
            data = str(m_1) + ',"' + str(m_1) +' '+ str(unit)  + '"'
    if period == 'w1':
        if w_1 != 0:
            data = str(w_1) + ',"' + str(w_1) +' '+ str(unit)  + '"'

    return data

def get_trailing_returns(uid):
    """ Get trailing return chart """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT instruments.fullname, instruments.is_benchmark, "+\
    "instruments.market, instruments.symbol, instruments.asset_class "+\
    "FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid=" + str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()

    for row in res:
        fullname = row[0].replace("'", "")
        is_benchmark = row[1]
        market = row[2]
        symbol_is_portf = row[3]
        asset_class = row[4]

    if symbol_is_portf.find(get_portf_suffix()) > -1:
        sql = "SELECT date FROM chart_data WHERE uid=" + str(uid) + " ORDER BY date DESC LIMIT 1"
    else:
        sql = "SELECT price_instruments_data.date FROM price_instruments_data JOIN symbol_list "+\
        "ON symbol_list.symbol = price_instruments_data.symbol "+\
        "WHERE symbol_list.uid=" + str(uid) +" ORDER BY date DESC LIMIT 1"

    cursor.execute(sql)
    res = cursor.fetchall()

    for row in res:
        as_date = row[0]

    l_as_date = 'Trailing returns as of '+ as_date.strftime("%d-%b-%Y")

    font_size = 10
    l_y1 = '1-Year'
    l_m6 = '6-month'
    l_m3 = '3-month'
    l_m1 = '1-month'
    l_w1 = '1-week'
    minb = 0
    mini = 0
    maxb = 0
    maxi = 0

    benchmark_header = ''
    benchmark_data_y1 = ''
    benchmark_data_m6 = ''
    benchmark_data_m3 = ''
    benchmark_data_m1 = ''
    benchmark_data_w1 = ''

    if not is_benchmark:

        sql = "SELECT symbol_list.uid, instruments.fullname "+\
        "FROM symbol_list JOIN instruments "+\
        "ON symbol_list.symbol = instruments.symbol "+\
        "WHERE instruments.market='"+\
        str(market) +"' AND instruments.asset_class='"+\
        str(asset_class) +"' AND instruments.is_benchmark=1"

        cursor.execute(sql)
        res = cursor.fetchall()
        benchmark_uid = 0
        for row in res:
            benchmark_uid = row[0]
            benchmark_fullname = row[1].replace("'", "")

        if benchmark_uid != 0:

            benchmark_header = ", ' " +\
            benchmark_fullname +\
            " ', {type: 'string', role: 'annotation'}"

            benchmark_data_y1 = ','+ get_chart_data(benchmark_uid, 'y1')
            benchmark_data_m6 = ','+ get_chart_data(benchmark_uid, 'm6')
            benchmark_data_m3 = ','+ get_chart_data(benchmark_uid, 'm3')
            benchmark_data_m1 = ','+ get_chart_data(benchmark_uid, 'm1')
            benchmark_data_w1 = ','+ get_chart_data(benchmark_uid, 'w1')
            minb = get_minmax(benchmark_uid, 'min')
            maxb = get_minmax(benchmark_uid, 'max')

    data = ''+\
    '["'+ l_y1 + '",' + get_chart_data(uid, 'y1') + benchmark_data_y1 +']' + ',' +\
    '["'+ l_m6 + '",' + get_chart_data(uid, 'm6') + benchmark_data_m6 + ']' + ',' +\
    '["'+ l_m3 + '",' + get_chart_data(uid, 'm3') + benchmark_data_m3 + ']' + ',' +\
    '["'+ l_m1 + '",' + get_chart_data(uid, 'm1') + benchmark_data_m1 + ']' + ',' +\
    '["'+ l_w1 + '",' + get_chart_data(uid, 'w1') + benchmark_data_w1 + ']'

    mini = get_minmax(uid, 'min')
    maxi = get_minmax(uid, 'max')

    if minb < mini:
        mini = minb
    if maxb > maxi:
        maxi = maxb

    header = "    ['x', ' " +\
    fullname + " ', {type: 'string', role: 'annotation'}"+\
    benchmark_header +"  ],"

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
    "       fontSize: "+ str(font_size) + "," +\
    "      	legend: {position:'top', textStyle: {color:"+\
    theme_return_this("'black'", "'white'")  +"} }," +\
    "        title: ''," +\
    "        backgroundColor: 'transparent',"+\
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
    "        series: {0:{color: "+\
    theme_return_this("'blue'", "'orange'") +"}, 1:{color: '#c9d6ea'} }," +\
    "        chartArea: {width:'80%',height:'80%'}," +\
    "        hAxis: {" +\
    "          title: '" + l_as_date + "', " +\
    "          titleTextStyle:{ color:"+\
    theme_return_this("'black'", "'white'") +"},"+\
    "          viewWindow:{min:"+\
    str(mini) +",max:"+\
    str(maxi) +"}," +\
    "          gridlines: { color: 'transparent' },"+\
    "          textStyle: { color: "+\
    theme_return_this("'black'", "'white'") +" } "+\
    "        }," +\
    "        vAxis: {" +\
    "          title: '', " +\
    "          textStyle: { color: "+\
    theme_return_this("'black'", "'white'") +" } "+\
    "        }" +\
    "      };" +\
    "      var chart = "+\
    "new google.visualization.BarChart(document.getElementById('trail_chart'));" +\
    "      chart.draw(data, options);" +\
    "    }" +\
    "    </script>" +\
    "    <div id='trail_chart' class='sa-chart-hw-290'></div>"

    cursor.close()
    connection.close()
    return chart_content
