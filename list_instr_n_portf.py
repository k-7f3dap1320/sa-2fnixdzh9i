# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *
from sa_db import *
from sa_func import *
from app_cookie import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def set_modal_delete_n_view_popup(portf_name,portf_id,burl,user_portf):
    r = ''
    try:
        l_delete_message_caption = 'Are you sure you want to delete this portfolio? ' + '<br /><strong>'+ portf_name + '</strong>'
        l_cancel_button = 'Cancel'
        l_delete_button = 'Delete'
        delete_url_redirect_list = burl +'p/?delete='+ str(portf_id)
        delete_url_redirect_dash = burl +'p/?delete='+ str(portf_id) + '&dashboard=1'

        if user_portf:
            delete_url = delete_url_redirect_dash
        else:
            delete_url = delete_url_redirect_list

        l_view_message_caption = 'View or edit your portfolio:' + '<br /><strong>'+ portf_name + '</strong>'
        l_view_button = 'Take me to my portfolio'

        r = '' +\
        '  <div class="modal" id="popup_delete_'+ str(portf_id) +'">'+\
        '    <div class="modal-dialog modal-dialog-centered">'+\
        '      <div class="modal-content">'+\
        '        <div class="modal-body">'+\
        l_delete_message_caption +\
        '        </div>'+\
        '        <div class="modal-footer">'+\
        '          <button type="button" class="btn btn-secondary" data-dismiss="modal">'+ l_cancel_button +'</button>'+\
        '           <a class="btn btn-danger" href="'+ delete_url +'">'+ l_delete_button +'</a>'+\
        '        </div>'+\
        '       </div>'+\
        '     </div>'+\
        '   </div>'

        r = r  +\
        '  <div class="modal" id="popup_view_'+ str(portf_id) +'">'+\
        '    <div class="modal-dialog modal-dialog-centered">'+\
        '      <div class="modal-content">'+\
        '        <div class="modal-body">'+\
        l_view_message_caption +\
        '        </div>'+\
        '        <div class="modal-footer">'+\
        '          <button type="button" class="btn btn-secondary" data-dismiss="modal">'+ l_cancel_button +'</button>'+\
        '           <a class="btn btn-info" href="'+ burl +'p/?uid='+ str(portf_id) +'">'+ l_view_button +'</a>'+\
        '        </div>'+\
        '       </div>'+\
        '     </div>'+\
        '   </div>'


    except Exception as e: print(e)
    return r

def draw_portf_table(burl,mode,what,step,portf,maxrow,x,user_portf):
    try:
        r = '<script>$(document).ready(function($) {'+\
        '$(".sa-table-click-row").click(function() {'+\
        'window.document.location = $(this).data("href");'+\
        '});'+\
        '});</script>'
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        if user_portf:
            sql = "SELECT symbol_list.uid, instruments.w_forecast_change, instruments.fullname, instruments.volatility_risk_st, "+\
            "instruments.y1, instruments.m6, instruments.m3, instruments.m1, instruments.w1, "+\
            "instruments.w_forecast_display_info, instruments.unit, instruments.symbol, feed.globalrank, feed.content FROM instruments "+\
            "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "JOIN feed ON instruments.symbol = feed.symbol "+\
            "WHERE instruments.owner = "+ str( get_user_numeric_id() ) +" AND symbol_list.symbol LIKE '%"+ str( get_portf_suffix() )+ "%'" + " ORDER BY feed.globalrank LIMIT "+ str(maxrow)
        else:
            sql = "SELECT symbol_list.uid, instruments.w_forecast_change, instruments.fullname, instruments.volatility_risk_st, "+\
            "instruments.y1, instruments.m6, instruments.m3, instruments.m1, instruments.w1, "+\
            "instruments.w_forecast_display_info, instruments.unit, instruments.symbol, feed.globalrank, feed.content FROM instruments "+\
            "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "JOIN feed ON instruments.symbol = feed.symbol "+\
            "WHERE symbol_list.symbol LIKE '%"+ str( get_portf_suffix() ) +"%' AND feed.globalrank <> 0 AND ( instruments.market LIKE '%"+ str(x) +"%' OR instruments.asset_class LIKE '%"+ str(x) +"%') "+\
            "AND symbol_list.disabled=0 ORDER BY feed.globalrank LIMIT "+ str(maxrow)

        print(sql)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            uid = row[0]; w_forecast_change = row[1]
            fullname = row[2]; volatility_risk_st = row[3]
            y1 = row[4]; m6 = row[5]
            m3 = row[6]; m1 = row[7]
            w1 = row[8]; w_forecast_display_info = row[9]
            unit = row[10]; symbol = row[11]
            globalrank  = row[12]
            portf_owner = row[13]
            volatility_risk_st = str(round(volatility_risk_st*100,2))+'%'
            if globalrank == 0:
                globalrank = 'Not ranked'
            if y1 >= 0: class_y1 = "text text-success"
            else: class_y1 = "text text-danger"
            if m6 >= 0: class_m6 = "text text-success"
            else: class_m6 = "text text-danger"
            if m3 >= 0: class_m3 = "text text-success"
            else: class_m3 = "text text-danger"
            if m1 >= 0: class_m1 = "text text-success"
            else: class_m1 = "text text-danger"
            if w1 >= 0: class_w1 = "text text-success"
            else: class_w1 = "text text-danger"
            if w_forecast_change >= 0: class_forecast = "bg bg-success text-white"
            else: class_forecast = "bg bg-danger text-white"

            if user_portf:
                class_row_style = ""
            else:
                class_row_style = ""

            if unit == 'pips':
                y1 = str(round( y1 ,0)) + ' pips'
                m6 = str(round( m6 ,0)) + ' pips'
                m3 = str(round( m3 ,0)) + ' pips'
                m1 = str(round( m1 ,0)) + ' pips'
                w1 = str(round( w1 ,0)) + ' pips'
            else:
                y1 = str(round( y1 * 100 ,2)) + '%'
                m6 = str(round( m6 * 100 ,2)) + '%'
                m3 = str(round( m3 * 100 ,2)) + '%'
                m1 = str(round( m1 * 100 ,2)) + '%'
                w1 = str(round( w1 * 100 ,2)) + '%'

            column_globalrank = '<td scope="row" class="'+ class_row_style +'" style="text-align: left"><i class="fas fa-trophy"></i>&nbsp'+ str(globalrank) +'</td>'
            target_url = burl + 'p/?uid=' + str(uid)

            r = r + set_modal_delete_n_view_popup(fullname,uid,burl,user_portf)
            l_btn_delete = 'delete'

            if user_portf == False:
                column_fullname = '<td  style="text-align: left" class="'+ class_row_style +'">'+ str(portf_owner.replace('{burl}',burl) ) + ' | ' + str(fullname)+ '</td>'
                data_href = 'data-href="'+ target_url +'"'
            else:
                column_fullname = '<td  style="text-align: left" class="'+ class_row_style +'">'+ '<button type="button" class="btn btn-danger btn-sm active" data-toggle="modal" data-target="#popup_delete_'+ str(uid) +'"><i class="far fa-trash-alt"></i>&nbsp;'+ l_btn_delete +'</button>' + ' | <button type="button" class="btn btn-info btn-sm active" data-toggle="modal" data-target="#popup_view_'+ str(uid) +'">' + str(fullname)+ '</button></td>'
                data_href = 'data-href="#"'

            column_y1 = '      <td class="'+ class_y1 +" "+ class_row_style +'">'+ str(y1) +'</td>'
            column_m6 = '      <td class="'+ class_m6 +" "+ class_row_style +'">'+ str(m6) +'</td>'
            column_m3 = '      <td class="'+ class_m3 +" "+ class_row_style +'">'+ str(m3) +'</td>'
            column_m1 = '      <td class="'+ class_m1 +" "+ class_row_style +'">'+ str(m1) +'</td>'
            column_w1 = '      <td class="'+ class_w1 +" "+ class_row_style +'">'+ str(w1) +'</td>'
            r = r +\
            '    <tr class="sa-table-click-row" '+data_href+'>'+\
            column_globalrank +\
            column_fullname +\
            '      <td class="'+ class_row_style +'">'+ str(volatility_risk_st) +'</td>'+\
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

def draw_instr_table(burl,mode,what,step,portf,maxrow,x):
    try:
        r = '<script>$(document).ready(function($) {'+\
        '$(".sa-table-click-row").click(function() {'+\
        'window.document.location = $(this).data("href");'+\
        '});'+\
        '});</script>'
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol_list.uid, instruments.w_forecast_change, instruments.fullname, instruments.volatility_risk_st, "+\
        "instruments.y1_signal, instruments.m6_signal, instruments.m3_signal, instruments.m1_signal, instruments.w1_signal, "+\
        "instruments.w_forecast_display_info, instruments.unit, instruments.symbol FROM instruments JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
        "WHERE symbol_list.symbol NOT LIKE '%"+ str( get_portf_suffix() ) +"%' AND ( instruments.market LIKE '%"+ str(x) +"%' OR instruments.asset_class LIKE '%"+ str(x) +"%') "+\
        "AND symbol_list.disabled=0 ORDER BY instruments.y1_signal DESC LIMIT "+ str(maxrow)
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
                column_order_type = '<td style="text-align: left" scope="row">'+ order_type +'</td>'
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
            '      <td style="text-align: left">'+ '<strong>'+str(fullname)+ '</strong> (' + str(symbol) + ')' + '</td>'+\
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

def get_table_content_list_instr_n_portf(burl,mode,what,step,portf,maxrow,x):
    r = ''
    try:

        if what == 'instr':
            r = draw_instr_table(burl,mode,what,step,portf,maxrow,x)
        if what == 'portf':
            if user_is_login() == 1: r = draw_portf_table(burl,mode,what,step,portf,maxrow,x,True)
            r = r + draw_portf_table(burl,mode,what,step,portf,maxrow,x,False)

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
            l_instr_portf = '<th scope="col" style="text-align: left">Instrument</th>'
            l_forc_expect_return = '<th scope="col">1-week Forecast</th>'
        else:
            if what == "instr":
                signal_column = '<th scope="col" style="text-align: left">Signal</th>'
                l_performance_note = '<span style="text-align: center; font-size: x-small;">*Signals performance</span>'
                l_instr_portf = '<th scope="col" style="text-align: left">Instrument</th>'
                l_forc_expect_return = '<th scope="col">1-week Forecast</th>'
            else:
                signal_column = '<th scope="col" style="text-align: left">Rank</th>'
                l_performance_note = ''
                l_instr_portf = '<th scope="col" style="text-align: left">portfolio</th>'
                l_forc_expect_return = '<th scope="col">1-week Forecast</th>'

            c_1_year_column = '<th scope="col">1-Year</th>'
            c_6_month_column = '<th scope="col">6-month</th>'
            c_3_month_column = '<th scope="col">3-month</th>'
            c_1_month_column = '<th scope="col">1-month</th>'
            c_1_week_column = '<th scope="col">1-week</th>'
            small_font_class = "sa-table-sm"

        if what == 'portf_select_disabled' or what == 'instr_disabled':
            tablesorter_script = '<script>$(function() { $("#table_instr_n_portf").tablesorter();}); $(function() {$("#table_instr_n_portf").tablesorter({ sortList: [[0,0], [1,0]] });});</script>'
        else:
            tablesorter_script = ''

        r = tablesorter_script +\
        l_performance_note +\
        '<table id="table_instr_n_portf" class="table table-hover table-sm '+ small_font_class +' ">'+\
        '  <thead>'+\
        '    <tr>'+\
        signal_column +\
        l_instr_portf +\
        '      <th scope="col">Vol. risk (%)</th>'+\
        c_1_year_column +\
        c_6_month_column +\
        c_3_month_column +\
        c_1_month_column +\
        c_1_week_column +\
        l_forc_expect_return +\
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
    # mode = 'view', mode = 'portf_select', mode = 'dashboard'
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


        l_placeholder = "Type to find from the list..."
        l_your_portfolios = 'Your Portfolio(s)'
        box_div_class = 'col-lg-12 col-md-12 col-sm-12 col-xs-12'
        portfolio_box_style_dark_mode = theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;')
        list_title = ''
        list_class = 'sa-center-content sa-list-select-100pct sa-instr-n-portf-list'
        search_box = '<div class="input-group input-group-lg"><div class="input-group-prepend"><span class="input-group-text" id="inputGroup-sizing-lg"><i class="fas fa-search" style="font-size: xx-large;"></i></span></div><input type="text" id="filterInput" name="filterInput" onkeyup="filterTable()" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_placeholder +'" autofocus></div><div>&nbsp;</div>'
        if mode == 'dashboard':
            list_title = '<span class="sectiont"><i class="fas fa-chart-pie"></i>&nbsp;'+ l_your_portfolios +'</span>'
            search_box = ''
            list_class = ''
            box_div_class = 'col-lg-12 col-md-12 col-sm-12 col-xs-12 d-none d-md-block'

        box_content = box_content +\
        '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="'+ box_div_class +'">'+\
        '            <div class="box-part rounded '+ list_class +'" style="'+ portfolio_box_style_dark_mode +'">'+\
        search_box +\
        list_title +\
        gen_instr_n_portf_table(burl,mode,what,step,portf,maxrow,x) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


        cr.close()
        connection.close()

    except Exception as e: print(e)

    return box_content
