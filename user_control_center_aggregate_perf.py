""" Aggregate strategy portfolio chart and control center """
import pymysql.cursors
from app_cookie import theme_return_this
from sa_func import get_user_numeric_id
from user_dashboard_count import get_num_orders
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_current_user_total_account_size(what):
    """ xxx """
    return_data = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    if what != 'min':
        sql = "SELECT sum(instruments.account_reference) as total_account, "+\
        "instruments.unit, markets.conv_to_usd "+\
        "FROM instruments JOIN markets ON markets.market_id = instruments.market "+\
        "WHERE instruments.owner = "+ str(get_user_numeric_id())
        cursor.execute(sql)
        res = cursor.fetchall()
        total_account = 0
        prev_unit = ''
        unit_diff = False
        min_balance = 0
        for row in res:
            total_account = row[0]
            if prev_unit == '':
                prev_unit = row[1]
            else:
                if prev_unit != row[1]:
                    unit_diff = True
            conv_to_usd = row[2]
            if total_account is not None:
                total_account = total_account * conv_to_usd
        if unit_diff:
            prev_unit = 'USD'
        if what == 'total':
            return_data = total_account
        if what == 'unit':
            return_data = prev_unit

    if what == 'min':
        min_balance = 0

        sql = "SELECT DISTINCT min(s.nav) FROM chart_data "+\
        "JOIN instruments ON instruments.symbol = chart_data.symbol "+\
        "JOIN (SELECT sum(chart_data.price_close) as nav, chart_data.date FROM chart_data "+\
        "JOIN instruments ON instruments.symbol = chart_data.symbol "+\
        "WHERE instruments.owner = "+\
        str(get_user_numeric_id()) +" GROUP BY chart_data.date) AS s ON s.date = chart_data.date "+\
        "WHERE instruments.owner = "+\
        str(get_user_numeric_id()) +" ORDER BY chart_data.date"

        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            min_balance = row[0]
        return_data = min_balance

    cursor.close()
    connection.close()
    return return_data

def gen_aggregate_perf_graph():
    """ xxx """
    return_data = ''
    min_yaxis = 0

    l_aggregate_perf_series_name = 'Aggregate Portfolio Performance'

    l_aggregate_portf_xaxis_total = '1-year aggregate performance based '+\
    'on a {total_account_size} {unit} invested.'

    l_aggregate_portf_xaxis_total = '' +\
    l_aggregate_portf_xaxis_total.replace('{total_account_size}',
                                          str(get_current_user_total_account_size('total')))

    l_aggregate_portf_xaxis_total = '' +\
    l_aggregate_portf_xaxis_total.replace('{unit}',
                                          str(get_current_user_total_account_size('unit')))

    portf_owner = get_user_numeric_id()

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = ' '+\
    'SELECT DISTINCT chart_data.date, s.nav, chart_data.price_close, chart_data.symbol '+\
    'FROM chart_data '+\
    'JOIN instruments ON instruments.symbol = chart_data.symbol '+\
    'JOIN (SELECT sum(chart_data.price_close) as nav, chart_data.date FROM chart_data '+\
    'JOIN instruments ON instruments.symbol = chart_data.symbol '+\
    'WHERE instruments.owner = '+\
    str(portf_owner) +' GROUP BY chart_data.date) AS s ON s.date = chart_data.date '+\
    'WHERE instruments.owner = '+\
    str(portf_owner) +' ORDER BY chart_data.date'

    cursor.execute(sql)
    res = cursor.fetchall()
    i = 0
    chart_rows = ''
    num_portf = 0
    cr_n = connection.cursor(pymysql.cursors.SSCursor)

    sql_n = "SELECT instruments.symbol FROM instruments WHERE instruments.owner = " +\
    str(portf_owner)

    cr_n.execute(sql_n)
    rs_n = cr_n.fetchall()
    for row in rs_n:
        num_portf += 1

    for row in res:
        date = row[0].strftime("%d-%m-%Y")
        nav = row[1]
        if min_yaxis == 0:
            min_yaxis = nav
        if nav < min_yaxis:
            min_yaxis = nav
        cr_c = connection.cursor(pymysql.cursors.SSCursor)

        sql_c = "SELECT chart_data.date, chart_data.price_close, chart_data.symbol "+\
        "FROM chart_data JOIN instruments ON instruments.symbol = chart_data.symbol "+\
        "WHERE instruments.owner = '"+\
        str(portf_owner) +"' AND chart_data.date = " +\
        str(row[0].strftime("%Y%m%d"))

        cr_c.execute(sql_c)
        rs_c = cr_c.fetchall()
        count_portf = 0
        for row in rs_c:
            count_portf += 1

        if count_portf == num_portf:
            if i == 0:
                chart_rows = "['"+ str(date) +"',  "+ str(nav) +"]"
            else:
                chart_rows = chart_rows + ",['"+ str(date) +"',  "+ str(nav) +"]"
            i += 1
        cr_c.close()

    return_data = "<script>"+\
    "google.charts.load('current', {'packages':['corechart']}); "+\
    "google.charts.setOnLoadCallback(drawChart); "+\
    "function drawChart() { "+\
    "  var data = google.visualization.arrayToDataTable([ "+\
    "    ['text', '"+ l_aggregate_perf_series_name +"'], "+\
    chart_rows +\
    "  ]); "+\
    "  var options = { "+\
    "    title: '', "+\
    "    hAxis: {title: '"+\
    l_aggregate_portf_xaxis_total +"',  titleTextStyle: {color: '"+\
    theme_return_this("#343a40", "#ffffff") +\
    "'}, textPosition: 'none', gridlines: {color: 'transparent'} }, "+\
    "    legend: {position: 'none'}, "+\
    "    chartArea:{right: '5', width:'90%',height:'80%'}, "+\
    "    vAxis: { "+\
    "    textStyle: { color:'"+ theme_return_this("#343a40", "#ffffff") +"' },"+\
    "    viewWindow:{ min: "+ str(min_yaxis) +", viewWindowMode: 'explicit'}, "+\
    "    gridlines: {color: 'transparent'} }, "+\
    "    lineWidth: 1, "+\
    "    areaOpacity: 0.2, "+\
    "    colors: ['"+ theme_return_this("#17a2b8", "orange") + "'],"+\
    "    backgroundColor: 'transparent'"+\
    "  }; "+\
    "  var chart = "+\
    "new google.visualization.AreaChart(document.getElementById('aggr_perf_chart_div')); "+\
    "  chart.draw(data, options); "+\
    "} "+\
    "</script>"+\
    "<div id='aggr_perf_chart_div' style='height:200px;'></div>"

    cursor.close()
    cursor.close()
    connection.close()
    return return_data

def get_aggregate_perf():
    """ xxx """
    box_content = ''
    l_title_aggregate_perf = 'Your Performance'

    box_content = '' +\
    '            <div class="box-part rounded" style="height: 300px;'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'" >'+\
    '               <span class="sectiont"><i class="fas fa-chart-area"></i>&nbsp;'+\
    l_title_aggregate_perf +'</span>'+\
    gen_aggregate_perf_graph() +\
    '            </div>'
    return box_content

def get_control_center():
    """ xxx """
    box_content = ''

    l_control_center_open_trade = 'You have {#} trade(s) to open today.'

    l_control_center_close_trade = 'You have to close {#} trade(s) '+\
    'at the best available price.'

    l_control_center_pending_trade = 'You have {#} trade(s) '+\
    'that you have to get ready to close at market open.'

    num_open_trades = get_num_orders('open')
    num_close_trades = get_num_orders('close')
    num_pending_trades = get_num_orders('pending')

    l_control_center_open_trade = '' +\
    l_control_center_open_trade.replace('{#}', str(num_open_trades))

    l_control_center_close_trade = '' +\
    l_control_center_close_trade.replace('{#}', str(num_close_trades))

    l_control_center_pending_trade = '' +\
    l_control_center_pending_trade.replace('{#}', str(num_pending_trades))

    open_trades = ''
    close_trades = ''
    pending_trades = ''

    if num_open_trades != 0:
        open_trades = ' '+\
        '  <li class="list-group-item d-flex justify-content-between align-items-center" '+\
        'style="background-color: transparent; border-color: '+\
        theme_return_this('','#343a40') +';">'+\
        '<span style="font-size: small;">' + l_control_center_open_trade +'</span>'+\
        '    <span class="badge badge-primary badge-pill">'+ str(num_open_trades) +'</span>'+\
        '  </li>'
    if num_close_trades != 0:
        close_trades = ' '+\
        '  <li class="list-group-item d-flex justify-content-between align-items-center" '+\
        'style="background-color: transparent; border-color: '+\
        theme_return_this('','#343a40') +';">'+\
        '<span style="font-size: small;">' + l_control_center_close_trade +'</span>' +\
        '    <span class="badge badge-warning badge-pill">'+ str(num_close_trades) +'</span>'+\
        '  </li>'
    if num_pending_trades != 0:
        pending_trades = ' '+\
        '  <li class="list-group-item d-flex justify-content-between align-items-center" '+\
        'style="background-color: transparent; border-color: '+\
        theme_return_this('','#343a40') +';">'+\
        '<span style="font-size: small;">' + l_control_center_pending_trade +'</span>' +\
        '    <span class="badge badge-secondary badge-pill">'+\
        str(num_pending_trades) +'</span>'+\
        '  </li>'

    control_center_content = ' '+\
    '<ul class="list-group">'+\
    open_trades +\
    close_trades +\
    pending_trades +\
    '</ul>'

    l_title_control_center = 'Control Center'

    box_content = '' +\
    '            <div class="box-part rounded" style="height: 300px; '+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'" >'+\
    '               <span class="sectiont"><i class="fas fa-tasks"></i>&nbsp;'+\
    l_title_control_center +'</span>'+\
    control_center_content+\
    '            </div>'
    return box_content

def get_control_center_aggregate_perf():
    """ xxx """
    return_data = ''+\
    '<div class="col-lg-6 col-md-12 col-sm-12 col-xs-12">'+\
    get_control_center()+\
    '</div>'+\
    '<div class="col-lg-6 col-md-12 col-sm-12 col-xs-12">'+\
    get_aggregate_perf()+\
    '</div>'
    return return_data
