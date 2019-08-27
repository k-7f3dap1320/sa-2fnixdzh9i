# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *
from sa_db import *
from sa_func import *
access_obj = sa_db_access()
import pymysql.cursors
import datetime
import time
from user_dashboard_count import *


def get_current_user_total_account_size(w):
    r = 0
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)

        if w != 'min':
            sql = "SELECT sum(instruments.account_reference) as total_account, instruments.unit, markets.conv_to_usd "+\
            "FROM instruments JOIN markets ON markets.market_id = instruments.market "+\
            "WHERE instruments.owner = "+ str( get_user_numeric_id() )
            print(sql)
            cr.execute(sql)
            rs = cr.fetchall()
            total_account = 0
            prev_unit = ''
            unit_diff = False
            min_balance = 0
            for row in rs:
                total_account = row[0]
                if prev_unit == '':
                    prev_unit = row[1]
                else:
                    if prev_unit != row[1]:
                        unit_diff = True
                conv_to_usd = row[2]
                total_account = total_account * conv_to_usd
            if unit_diff:
                prev_unit = 'USD'
            if w == 'total':
                r = total_account
            if w == 'unit':
                r = prev_unit

        if w == 'min':
            min_balance = 0
            sql = "SELECT DISTINCT min(s.nav) FROM chart_data "+\
            "JOIN instruments ON instruments.symbol = chart_data.symbol "+\
            "JOIN (SELECT sum(chart_data.price_close) as nav, chart_data.date FROM chart_data "+\
            "JOIN instruments ON instruments.symbol = chart_data.symbol "+\
            "WHERE instruments.owner = "+ str( get_user_numeric_id() ) +" GROUP BY chart_data.date) AS s ON s.date = chart_data.date "+\
            "WHERE instruments.owner = "+ str( get_user_numeric_id() ) +" ORDER BY chart_data.date"
            print(sql)
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: min_balance = row[0]
            r = min_balance

        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def gen_aggregate_perf_graph():
    r = ''
    try:

        l_aggregate_perf_series_name = 'Aggregate Portfolio Performance'
        l_aggregate_portf_Xaxis_total = '1-year aggregate performance based on a {total_account_size} {unit} invested.'
        l_aggregate_portf_Xaxis_total = l_aggregate_portf_Xaxis_total.replace('{total_account_size}', str(get_current_user_total_account_size('total')) )
        l_aggregate_portf_Xaxis_total = l_aggregate_portf_Xaxis_total.replace('{unit}', str( get_current_user_total_account_size('unit') ) )

        portf_owner = get_user_numeric_id()

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = ' '+\
        'SELECT DISTINCT chart_data.date, s.nav, chart_data.price_close, chart_data.symbol '+\
        'FROM chart_data '+\
        'JOIN instruments ON instruments.symbol = chart_data.symbol '+\
        'JOIN (SELECT sum(chart_data.price_close) as nav, chart_data.date FROM chart_data '+\
        'JOIN instruments ON instruments.symbol = chart_data.symbol '+\
        'WHERE instruments.owner = '+ str(portf_owner) +' GROUP BY chart_data.date) AS s ON s.date = chart_data.date '+\
        'WHERE instruments.owner = '+ str(portf_owner) +' ORDER BY chart_data.date'
        cr.execute(sql)
        rs = cr.fetchall()
        i = 0
        chart_rows = ''
        num_portf = 0
        cr_n = connection.cursor(pymysql.cursors.SSCursor)
        sql_n = "SELECT instruments.symbol FROM instruments WHERE instruments.owner = " + str(portf_owner)
        cr_n.execute(sql_n)
        rs_n = cr_n.fetchall()
        for row in rs_n: num_portf += 1

        for row in rs:
            date = row[0].strftime("%d-%m-%Y")
            nav = row[1]
            price_close = row[2]
            portf_symbol = row[3]
            cr_c = connection.cursor(pymysql.cursors.SSCursor)
            sql_c = "SELECT chart_data.date, chart_data.price_close, chart_data.symbol FROM chart_data JOIN instruments ON instruments.symbol = chart_data.symbol "+\
                    "WHERE instruments.owner = '"+ str(portf_owner) +"' AND chart_data.date = " + str( row[0].strftime("%Y%m%d") )
            cr_c.execute(sql_c)
            rs_c = cr_c.fetchall()
            count_portf = 0
            for row in rs_c: count_portf += 1

            if count_portf == num_portf:
                if i == 0:
                    chart_rows = "['"+ str(date) +"',  "+ str(nav) +"]"
                else:
                    chart_rows = chart_rows + ",['"+ str(date) +"',  "+ str(nav) +"]"
                i += 1

        r = "<script>"+\
        "google.charts.load('current', {'packages':['corechart']}); "+\
        "google.charts.setOnLoadCallback(drawChart); "+\
        "function drawChart() { "+\
        "  var data = google.visualization.arrayToDataTable([ "+\
        "    ['text', '"+ l_aggregate_perf_series_name +"'], "+\
        chart_rows +\
        "  ]); "+\
        "  var options = { "+\
        "    title: '', "+\
        "    hAxis: {title: '"+ l_aggregate_portf_Xaxis_total +"',  titleTextStyle: {color: '#343a40'}, textPosition: 'none', gridlines: {color: 'transparent'} }, "+\
        "    legend: {position: 'none'}, "+\
        "    chartArea:{right: '5', width:'90%',height:'80%'}, "+\
        "    vAxis: { "+\
        "    viewWindow:{viewWindowMode: 'explicit'}, gridlines: {color: 'transparent'} }, "+\
        "    lineWidth: 2, "+\
        "    areaOpacity: 0.3, "+\
        "    colors: ['"+ theme_return_this("#17a2b8","#ffffff") + "'],"+\
        "    backgroundColor: 'transparent'"+\
        "  }; "+\
        "  var chart = new google.visualization.AreaChart(document.getElementById('aggr_perf_chart_div')); "+\
        "  chart.draw(data, options); "+\
        "} "+\
        "</script>"+\
        "<div id='aggr_perf_chart_div' style='height:350px;'></div>"

        cr.close()
        cr_c.close()
        cr_n.close()
        connection.close()

    except Exception as e: print(e)
    return r

def get_aggregate_perf():

    box_content = ''

    try:

        l_title_aggregate_perf = 'Your Performance'

        box_content = '' +\
        '            <div class="box-part rounded" style="height: 465px; '+ theme_return_this('',', background-color: #20124d;') +'">'+\
        '               <span class="sectiont"><i class="fas fa-chart-area"></i>&nbsp;'+ l_title_aggregate_perf +'</span>'+\
        gen_aggregate_perf_graph() +\
        '            </div>'

    except Exception as e: print(e)

    return box_content

def get_control_center(burl):

    box_content = ''

    try:

        l_control_center_open_trade = 'You have {#} trade(s) to open today.'
        l_control_center_close_trade = 'You have to close {#} trade(s) at the best available price.'
        l_control_center_pending_trade = 'You have {#} trade(s) that you have to get ready to close at market open.'

        num_open_trades = get_num_orders('open')
        num_close_trades =  get_num_orders('close')
        num_pending_trades = get_num_orders('pending')

        l_control_center_open_trade = l_control_center_open_trade.replace('{#}', str(num_open_trades) )
        l_control_center_close_trade = l_control_center_close_trade.replace('{#}', str(num_close_trades) )
        l_control_center_pending_trade = l_control_center_pending_trade.replace('{#}', str(num_pending_trades) )

        open_trades = ''
        close_trades = ''
        pending_trades = ''

        if num_open_trades != 0:
            open_trades = ' '+\
            '  <li class="list-group-item d-flex justify-content-between align-items-center">'+\
            '<span style="font-size: small;">' + l_control_center_open_trade +'</span>'+\
            '    <span class="badge badge-primary badge-pill">'+ str(num_open_trades) +'</span>'+\
            '  </li>'
        if num_close_trades != 0:
            close_trades = ' '+\
            '  <li class="list-group-item d-flex justify-content-between align-items-center">'+\
            '<span style="font-size: small;">' + l_control_center_close_trade +'</span>' +\
            '    <span class="badge badge-warning badge-pill">'+ str( num_close_trades ) +'</span>'+\
            '  </li>'
        if num_pending_trades != 0:
            pending_trades = ' '+\
            '  <li class="list-group-item d-flex justify-content-between align-items-center">'+\
            '<span style="font-size: small;">' + l_control_center_pending_trade +'</span>' +\
            '    <span class="badge badge-secondary badge-pill">'+ str( num_pending_trades ) +'</span>'+\
            '  </li>'

        control_center_content = ' '+\
        '<ul class="list-group">'+\
        open_trades +\
        close_trades +\
        pending_trades +\
        '</ul>'

        l_title_control_center = 'Control Center'

        box_content = '' +\
        '            <div class="box-part rounded" style="height: 250px;">'+\
        '               <span class="sectiont"><i class="fas fa-tasks"></i>&nbsp;'+ l_title_control_center +'</span>'+\
        control_center_content+\
        '            </div>'

    except Exception as e: print(e)

    return box_content


def get_control_center_aggregate_perf(burl):
    r = ''
    try:
        r = '<div class="col-lg-6 col-md-12 col-sm-12 col-xs-12">'+\
        get_control_center(burl)+\
        get_aggregate_perf()+\
        '</div>'

    except Exception as e: print(e)
    return r
