# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
from sa_func import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_table_content_list_instr_n_portf(burl,mode,what,step,portf,maxrow,x):

    r = '<script>$(document).ready(function($) {'+\
        '$(".sa-table-click-row").click(function() {'+\
        'window.document.location = $(this).data("href");'+\
        '});'+\
        '});</script>'
    try:

        if x is None: x = get_user_default_profile()
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        if what == 'instr':
            sql = "SELECT symbol_list.uid, instruments.w_forecast_change, instruments.fullname, instruments.volatility_risk_st, "+\
            "instruments.y1_signal, instruments.m6_signal, instruments.m3_signal, instruments.m1_signal, instruments.w1_signal, "+\
            "instruments.w_forecast_display_info, instruments.unit, instruments.symbol FROM instruments JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "WHERE symbol_list.symbol NOT LIKE '%"+ str( get_portf_suffix() ) +"%' AND ( instruments.market LIKE '%"+ str(x) +"%' OR instruments.asset_class LIKE '%"+ str(x) +"%') "+\
            "AND symbol_list.disabled=0 ORDER BY RAND() LIMIT "+ str(maxrow)
            print(sql)
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                uid = row[0]; w_forecast_change = row[1]
                fullname = row[2]; volatility_risk_st = row[3]
                y1_signal = row[4]; m6_signal = row[5]
                m3_signal = row[6]; m1_signal = row[7]
                w1_signal = row[8]; w_forecast_display_info = row[9]
                unit = row[10]; symbol = row[11]

                volatility_risk_st = str(round(volatility_risk_st*100,2))+'%'

                if y1_signal >= 0: class_y1 = "text text-success"
                else: class_y1 = "text text-danger"

                if m6_signal >= 0: class_m6 = "text text-success"
                else: class_m6 = "text text-danger"

                if m3_signal >= 0: class_m3 = "text text-success"
                else: class_m3 = "text text-danger"

                if m1_signal >= 0: class_m1 = "text text-success"
                else: class_m1 = "text text-danger"

                if w1_signal >= 0: class_w1 = "text text-success"
                else: class_w1 = "text text-danger"

                if w_forecast_change >= 0: class_forecast = "bg bg-success text-white"
                else: class_forecast = "bg bg-danger text-white"


                if unit == 'pips':
                    y1_signal = str(round( y1_signal ,0)) + ' pips'
                    m6_signal = str(round( m6_signal ,0)) + ' pips'
                    m3_signal = str(round( m3_signal ,0)) + ' pips'
                    m1_signal = str(round( m1_signal ,0)) + ' pips'
                    w1_signal = str(round( w1_signal ,0)) + ' pips'
                else:
                    y1_signal = str(round( y1_signal * 100 ,2)) + '%'
                    m6_signal = str(round( m6_signal * 100 ,2)) + '%'
                    m3_signal = str(round( m3_signal * 100 ,2)) + '%'
                    m1_signal = str(round( m1_signal * 100 ,2)) + '%'
                    w1_signal = str(round( w1_signal * 100 ,2)) + '%'

                if not mode == "portf_select":
                    if w_forecast_change >=0:
                        order_type = '<span class="badge badge-success">buy</span>'
                    else:
                        order_type = '<span class="badge badge-danger">sell</span>'
                    column_order_type = '<td scope="row">'+ order_type +'</td>'
                    column_y1 = '      <td class="'+ class_y1 +'">'+ str(y1_signal) +'</td>'
                    column_m6 = '      <td class="'+ class_m6 +'">'+ str(m6_signal) +'</td>'
                    column_m3 = '      <td class="'+ class_m3 +'">'+ str(m3_signal) +'</td>'
                    column_m1 = '      <td class="'+ class_m1 +'">'+ str(m1_signal) +'</td>'
                    column_w1 = '      <td class="'+ class_w1 +'">'+ str(w1_signal) +'</td>'
                else:
                    order_type = ''
                    column_order_type = ''
                    column_y1 = ''
                    column_m6 = ''
                    column_m3 = ''
                    column_m1 = ''
                    column_w1 = ''

                if mode == 'portf_select': target_url = burl + 'p/?ins=2&step='+ str(step) +'&uid='+ str(uid) + '&x=' + str(x)
                if mode == 'view': target_url = burl + 's/?uid=' + str(uid)

                r = r +\
                '    <tr class="sa-table-click-row" data-href="'+ target_url +'">'+\
                column_order_type +\
                '      <td>'+ '<strong>'+str(fullname)+ '</strong> (' + str(symbol) + ')' + '</td>'+\
                '      <td>'+ str(volatility_risk_st) +'</td>'+\
                column_y1 +\
                column_m6 +\
                column_m3 +\
                column_m1 +\
                column_w1 +\
                '      <td class="'+ class_forecast +'">'+ str(w_forecast_display_info) +'</td>'+\
                '    </tr>'
            cr.close()
            connection.close()

    except Exception as e: print(e)
    return r


def gen_instr_n_portf_table(burl,mode,what,step,portf,maxrow,x):

    r = ''
    try:

        if mode == "portf_select":
            signal_column = ""
            c_1_year_column = ""
            c_6_month_column = ""
            c_3_month_column = ""
            c_1_month_column = ""
            c_1_week_column = ""
            l_performance_note = ""
            small_font_class = ""
        else:
            signal_column = '<th scope="col">Signal</th>'
            c_1_year_column = '<th scope="col">1-Year</th>'
            c_6_month_column = '<th scope="col">6-month</th>'
            c_3_month_column = '<th scope="col">3-month</th>'
            c_1_month_column = '<th scope="col">1-month</th>'
            c_1_week_column = '<th scope="col">1-week</th>'
            l_performance_note = '<span style="text-align: center; font-size: x-small;">*Signals performance</span>'
            small_font_class = "sa-table-sm"

        r = '<script>$(function() { $("#table_instr_n_portf").tablesorter();}); $(function() {$("#table_instr_n_portf").tablesorter({ sortList: [[0,0], [1,0]] });});</script>' +\
        l_performance_note +\
        '<table id="table_instr_n_portf" class="table table-hover table-sm '+ small_font_class +' tablesorter`">'+\
        '  <thead>'+\
        '    <tr>'+\
        signal_column +\
        '      <th scope="col">Instrument</th>'+\
        '      <th scope="col">Volatility risk (%)</th>'+\
        c_1_year_column +\
        c_6_month_column +\
        c_3_month_column +\
        c_1_month_column +\
        c_1_week_column +\
        '      <th scope="col">1-week Forecast</th>'+\
        '    </tr>'+\
        ' </thead>'+\
        '  <tbody>'+\
        get_table_content_list_instr_n_portf(burl,mode,what,step,portf,maxrow,x) +\
        '  </tbody>'+\
        '</table>'

    except Exception as e:
        print(e)
    return r

def get_box_list_instr_n_portf(burl,mode,what,step,portf,maxrow,x):
    # mode = 'view', mode = 'portf_select'
    # what = 'instr', what = 'portf'
    # portf = portf uid
    # maxrow = numeric number of row ie. 1000
    #  step = step of portfolio selection

    box_content = ''

    try:
        if mode == 'portf_select':
            col_id = 0
        else:
            col_id = 1

        box_content = '' +\
        '<script>'+\
        'function filterTable() {'+\
        '  var input, filter, table, tr, td, i, txtValue;'+\
        '  input = document.getElementById("filterInput");'+\
        '  filter = input.value.toUpperCase();'+\
        '  table = document.getElementById("table_instr_n_portf");'+\
        '  tr = table.getElementsByTagName("tr");'+\
        '  for (i = 0; i < tr.length; i++) {'+\
        '    td = tr[i].getElementsByTagName("td")['+ str(col_id) +'];'+\
        '    if (td) {'+\
        '      txtValue = td.textContent || td.innerText;'+\
        '      if (txtValue.toUpperCase().indexOf(filter) > -1) {'+\
        '        tr[i].style.display = "";'+\
        '      } else {'+\
        '        tr[i].style.display = "none";'+\
        '      }'+\
        '    }'+\
        '  }'+\
        '}'+\
        '</script>'


        l_placeholder = "Type to find for an instrument..."
        if mode == 'portf_select':
            l_caption_to_more_assets = 'Unable find your instrument or symbol? '
            l_link_to_more_assets = ''
            connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT asset_class_id, asset_class_name FROM asset_class WHERE asset_class_id <> 'PF:' and asset_class_id <>'MA:' ORDER BY asset_class_name"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                asset_class_id = row[0]
                asset_class_name = row[1]
                l_link_to_more_assets = l_link_to_more_assets +'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="'+ burl+'p/?ins=1&step='+ str(step) + '&x='+ asset_class_id +'">'+ asset_class_name +'</a>'
        else:
            l_caption_to_more_assets = ''
            l_link_to_more_assets = ''


        box_content = box_content + '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content sa-list-select-100pct sa-instr-n-portf-list">'+\
        '               <div class="input-group input-group-lg">'+\
        '                   <div class="input-group-prepend">'+\
        '                       <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fas fa-search" style="font-size: xx-large;"></i></span>'+\
        '                   </div>'+\
        '                       <input type="text" id="filterInput" name="filterInput" onkeyup="filterTable()" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_placeholder +'" autofocus>'+\
        '               </div>'+\
        '            <div>&nbsp;</div>'+\
        gen_instr_n_portf_table(burl,mode,what,step,portf,maxrow,x) +\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+ l_caption_to_more_assets + l_link_to_more_assets +'<br /><br /></div>' +\
        '   </div>'+\
        '</div>'


        cr.close()
        connection.close()

    except Exception as e: print(e)

    return box_content
