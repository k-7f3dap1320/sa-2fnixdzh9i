# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
from sa_func import *
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_portf_perf(uid):

    portf_perf_box = ''
    portf_desc_box = ''


    try:
        desc_box_title = 'Description & Recommendations'
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.description, instruments.w_forecast_display_info, instruments.account_reference, instruments.unit, instruments.symbol from instruments JOIN symbol_list "+\
        "ON instruments.symbol = symbol_list.symbol WHERE symbol_list.uid=" + str(uid)
        print(sql)
        cr.execute(sql)
        rs = cr.fetchall()
        portf_summary = ""
        for row in rs:
            portf_summary = row[0]
            portf_forecast = row[1]
            portf_account_ref = row[2]
            portf_unit = row[3]
            portf_symbol = row[4]

        slang = get_selected_lang()
        sql = "SELECT portf_descr, portf_recomm_buy, portf_recomm_sell FROM recommendations WHERE lang ='"+ slang +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        portf_descr =''; portf_recomm_buy =''; portf_recomm_sell = ''
        for row in rs:
            portf_descr = row[0]
            portf_recomm_buy = row[1]
            portf_recomm_sell = row[2]

        portf_descr = portf_descr.replace('{account_minimum}',str(portf_account_ref) )
        portf_descr = portf_descr.replace('{unit}', portf_unit)

        #{portf_recomm} = "buy {portf_alloc_instr} below {portf_alloc_entry_price}"
        #{portf_recomm} = "sell {portf_alloc_instr} above {portf_alloc_entry_price}"
        portf_recomm = '<br /><br />'
        sql = 'SELECT order_type, alloc_fullname, entry_level FROM portfolios '+\
        "WHERE portf_symbol ='"+ portf_symbol +"'  ORDER BY alloc_fullname"
        cr.execute(sql)
        rs = cr.fetchall()
        i = 1
        for row in rs:
            alloc_order_type = row[0]
            alloc_fullname = row[1]
            alloc_entry_price = row[2]

            if alloc_order_type.lower() == 'buy':
                portf_recomm = portf_recomm + '('+str(i)+') ' + portf_recomm_buy.replace('{portf_alloc_instr}',alloc_fullname)+ '<br />'
            if alloc_order_type.lower() == 'sell':
                portf_recomm = portf_recomm + '('+str(i)+') ' + portf_recomm_sell.replace('{portf_alloc_instr}',alloc_fullname)+ '<br />'

            portf_recomm = portf_recomm.replace('{portf_alloc_entry_price}', alloc_entry_price)
            i += 1

        portf_descr = portf_descr.replace('{portf_recomm}', portf_recomm)

        cr.close()
        connection.close()

        desc_box_content = portf_summary + ' ' + portf_descr



        portf_desc_box = '' +\
        '        <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-portf-perf-portf-chart">'+\
        '               <div><h6>'+ desc_box_title +'</h6></div>'+\
        '               <div class="sa-descr-box-sm">'+ desc_box_content +'</div>'+\
        '            </div>'+\
        '        </div>'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT chart_data.symbol, chart_data.date, chart_data.price_close, instruments.fullname, instruments.unit FROM chart_data "+\
        "JOIN instruments ON chart_data.symbol = instruments.symbol "+\
        "WHERE chart_data.uid=" + str(uid) + " ORDER BY chart_data.date"
        print(sql)
        cr.execute(sql)
        rs = cr.fetchall()
        data = ""
        for row in rs:
            symbol = row[0]
            chart_date = row[1]
            price_close = row[2]
            fullname = row[3]
            portf_unit = row[4]

            year = chart_date.strftime("%Y")
            month = chart_date.strftime("%m")
            day = chart_date.strftime("%d")
            if data =="":
                data = data + "[new Date("+str(year)+", "+str(int(month)-1 )+", "+str(day)+"),"+str(price_close)+"]"
            else:
                data = data + ",[new Date("+str(year)+", "+str( int(month)-1 )+", "+str(day)+"),"+str(price_close)+"]"


        chart_box_title = "Portfolio 1-Year Performance"
        hAxis = "Date"; vAxis = "Price (" + portf_unit + ")"
        profit_1Y = price_close
        portf_perf_font_size = 10

        portf_perf_box = '' +\
        '        <div class="col-lg-8 col-md-8 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-portf-perf-portf-chart">'+\
        '                   <div><h6>'+ chart_box_title +'</h6></div>'+\
        '                   <script>'+\
        '                       google.charts.load("current", {"packages":["corechart"]});'+\
        '                       google.charts.setOnLoadCallback(drawChart);'+\
        '                       function drawChart() {'+\
        '                          var data = new google.visualization.DataTable();'+\
        '                          data.addColumn("date", "'+ hAxis +'");'+\
        '                          data.addColumn("number", "'+ vAxis +'");'+\
        '                          data.addRows(['+data+']);'+\
        '                          var options = {'+\
        '                            legend: "none",'+\
        '                            vAxis: {minValue: 0, textStyle: {fontSize:'+ str(portf_perf_font_size) +'}, gridlines: { color: "transparent" } },'+\
        '                            hAxis: {textStyle: {fontSize:'+ str(portf_perf_font_size) +'}, gridlines: { count: 4 } }, '+\
        '                            series:{0: {areaOpacity: 0.1, color: "black", lineWidth: 1} },'+\
        '                            chartArea:{width:"80%",height:"80%"}'+\
        '                          };'+\
        '                          var chart = new google.visualization.AreaChart(document.getElementById("portf_perf_chart"));'+\
        '                          chart.draw(data, options);'+\
        '                       }'+\
        '                   </script>'+\
        '               <div id="portf_perf_chart" class="sa-chart-hw-100"></div>'+\
        '            </div>'+\
        '        </div>'


        cr.close()
        connection.close()


    except Exception as e: print(e)

    return portf_desc_box + portf_perf_box
