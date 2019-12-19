""" List of instruments and strategy portfolio """
import pymysql.cursors
from app_cookie import user_is_login, theme_return_this
from sa_func import get_user_numeric_id, get_portf_suffix
from app_popup_modal import get_portf_delete_data_toggle, set_modal_delete_n_view_popup
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def draw_portf_table(burl, maxrow, sel, user_portf):
    """ xxx """
    return_data = '<script>$(document).ready(function($) {'+\
    '$(".sa-table-click-row").click(function() {'+\
    'window.document.location = $(this).data("href");'+\
    '});'+\
    '});</script>'
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    if user_portf:
        sql = "SELECT symbol_list.uid, instruments.w_forecast_change, "+\
        "instruments.fullname, instruments.volatility_risk_st, "+\
        "instruments.y1, instruments.m6, instruments.m3, instruments.m1, "+\
        "instruments.w1, "+\
        "instruments.w_forecast_display_info, instruments.unit, "+\
        "instruments.symbol, feed.globalrank, feed.content FROM instruments "+\
        "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
        "JOIN feed ON instruments.symbol = feed.symbol "+\
        "WHERE instruments.owner = "+\
        str(get_user_numeric_id()) +" AND symbol_list.symbol LIKE '%"+\
        str(get_portf_suffix())+ "%'" + " ORDER BY feed.globalrank LIMIT "+\
        str(maxrow)
    else:
        sql = "SELECT symbol_list.uid, instruments.w_forecast_change, "+\
        "instruments.fullname, instruments.volatility_risk_st, "+\
        "instruments.y1, instruments.m6, instruments.m3, "+\
        "instruments.m1, instruments.w1, "+\
        "instruments.w_forecast_display_info, instruments.unit, "+\
        "instruments.symbol, feed.globalrank, feed.content FROM instruments "+\
        "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
        "JOIN feed ON instruments.symbol = feed.symbol "+\
        "WHERE symbol_list.symbol LIKE '%"+\
        str(get_portf_suffix()) +\
        "%' AND feed.globalrank <> 0 AND ( instruments.market LIKE '%"+\
        str(sel) +"%' OR instruments.asset_class LIKE '%"+\
        str(sel) +"%') "+\
        "AND symbol_list.disabled=0 ORDER BY feed.globalrank LIMIT "+\
        str(maxrow)

    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        uid = row[0]
        fullname = row[2]
        volatility_risk_st = row[3]
        y_1 = row[4]
        m_6 = row[5]
        m_3 = row[6]
        m_1 = row[7]
        w_1 = row[8]
        unit = row[10]
        globalrank = row[12]
        portf_owner = row[13]
        if user_portf:
            volatility_risk_st = ''
        else:
            volatility_risk_st = str(round(volatility_risk_st * 100, 2))+'%'

        if globalrank == 0:
            globalrank = 'Not ranked'
        if y_1 >= 0:
            class_y1 = "text text-success"
        else:
            class_y1 = "text text-danger"
        if m_6 >= 0:
            class_m6 = "text text-success"
        else:
            class_m6 = "text text-danger"
        if m_3 >= 0:
            class_m3 = "text text-success"
        else:
            class_m3 = "text text-danger"
        if m_1 >= 0:
            class_m1 = "text text-success"
        else:
            class_m1 = "text text-danger"
        if w_1 >= 0:
            class_w1 = "text text-success"
        else:
            class_w1 = "text text-danger"

        if user_portf:
            class_row_style = ""
        else:
            class_row_style = ""

        if unit == 'pips':
            y_1 = str(round(y_1, 0)) + ' pips'
            m_6 = str(round(m_6, 0)) + ' pips'
            m_3 = str(round(m_3, 0)) + ' pips'
            m_1 = str(round(m_1, 0)) + ' pips'
            w_1 = str(round(w_1, 0)) + ' pips'
        else:
            y_1 = str(round(y_1 * 100, 2)) + '%'
            m_6 = str(round(m_6 * 100, 2)) + '%'
            m_3 = str(round(m_3 * 100, 2)) + '%'
            m_1 = str(round(m_1 * 100, 2)) + '%'
            w_1 = str(round(w_1 * 100, 2)) + '%'

        column_globalrank = '<td scope="row" class="'+ class_row_style +\
        '" style="text-align: left"><i class="fas fa-trophy"></i>&nbsp'+\
        str(globalrank) +'</td>'

        target_url = burl + 'p/?uid=' + str(uid)

        return_data = (return_data +
                       set_modal_delete_n_view_popup(fullname, uid, burl, user_portf))

        if not user_portf:
            column_fullname = '<td  style="text-align: left" class="'+\
            class_row_style +'">'+\
            str(portf_owner.replace('{burl}', burl)) + ' | ' +\
            str(fullname)+ '</td>'
            data_href = 'data-href="'+ target_url +'"'
        else:
            column_fullname = '<td  style="text-align: left" class="'+\
            class_row_style +'">'+\
            '<button type="button" class="btn btn-danger btn-sm active" '+\
            get_portf_delete_data_toggle(uid) +'><i class="far fa-trash-alt"></i></button>' +\
            ' | <button type="button" class="btn btn-info btn-sm active" '+\
            'data-toggle="modal" data-target="#popup_view_'+\
            str(uid) +'">' +\
            '<i class="far fa-folder-open"></i></button>'+\
            '&nbsp;' + get_allocation_for_table(uid, connection) +'</td>'
            data_href = 'data-href="#"'

        column_y1 = '      <td class="'+ class_y1 +" "+ class_row_style +'">'+ str(y_1) +'</td>'
        column_m6 = '      <td class="'+ class_m6 +" "+ class_row_style +'">'+ str(m_6) +'</td>'
        column_m3 = '      <td class="'+ class_m3 +" "+ class_row_style +'">'+ str(m_3) +'</td>'
        column_m1 = '      <td class="'+ class_m1 +" "+ class_row_style +'">'+ str(m_1) +'</td>'
        column_w1 = '      <td class="'+ class_w1 +" "+ class_row_style +'">'+ str(w_1) +'</td>'
        return_data = return_data +\
        '    <tr class="sa-table-click-row" '+data_href+'>'+\
        column_globalrank +\
        column_fullname +\
        '      <td class="'+ class_row_style +'">'+ str(volatility_risk_st) +'</td>'+\
        column_y1 +\
        column_m6 +\
        column_m3 +\
        column_m1 +\
        column_w1 +\
        '    </tr>'
    cursor.close()
    connection.close()

    return return_data

def get_allocation_for_table(uid, connection):
    """ xxx """
    ret = ''
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT portfolios.symbol, portfolios.strategy_order_type FROM symbol_list ' +\
    'JOIN portfolios ON portfolios.portf_symbol = symbol_list.symbol '+\
    'WHERE symbol_list.uid = '+ str(uid)
    cursor.execute(sql)
    res = cursor.fetchall()
    symbol = ''
    badge = ''
    total_trade_pnl = 0
    for row in res:
        symbol = row[0]
        strategy_order_type = row[1]
        if strategy_order_type == 'long':
            order_type = 'buy'
        elif strategy_order_type == 'short':
            order_type = 'sell'
        else:
            order_type = '%%'

        cr_o = connection.cursor(pymysql.cursors.SSCursor)
        sql_o = 'SELECT SUM(pnl_pct) FROM trades '+\
        'WHERE status="Active" AND symbol = "'+\
        str(symbol) +'" AND order_type LIKE "'+\
        str(order_type) +'"'
        cr_o.execute(sql_o)
        res_o = cr_o.fetchall()
        for row in res_o:
            total_trade_pnl = row[0]
        cr_o.close()

        if total_trade_pnl > 0:
            badge = '<span class="badge badge-pill badge-success">'+\
            symbol +'</span>'
        elif total_trade_pnl < 0:
            badge = '<span class="badge badge-pill badge-danger">'+\
            symbol +'</span>'
        else:
            badge = '<span class="badge badge-pill badge-warning">'+\
            symbol +'</span>'
        ret = ret + '&nbsp;' + badge

    cursor.close()
    return ret

def draw_instr_table(burl, mode, step, maxrow, sel):
    """ xxx """
    return_data = '<script>$(document).ready(function($) {'+\
    '$(".sa-table-click-row").click(function() {'+\
    'window.document.location = $(this).data("href");'+\
    '});'+\
    '});</script>'
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol_list.uid, instruments.w_forecast_change, "+\
    "instruments.fullname, instruments.volatility_risk_st, "+\
    "instruments.y1_signal, instruments.m6_signal, "+\
    "instruments.m3_signal, instruments.m1_signal, instruments.w1_signal, "+\
    "instruments.w_forecast_display_info, instruments.unit, "+\
    "instruments.symbol FROM instruments "+\
    "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE symbol_list.symbol NOT LIKE '%"+\
    str(get_portf_suffix()) +"%' AND ( instruments.market LIKE '%"+\
    str(sel) +"%' OR instruments.asset_class LIKE '%"+ str(sel) +"%') "+\
    "AND symbol_list.disabled=0 ORDER BY instruments.y1_signal DESC LIMIT "+\
    str(maxrow)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        uid = row[0]
        w_forecast_change = row[1]
        fullname = row[2]
        volatility_risk_st = row[3]
        y1_signal = row[4]
        m6_signal = row[5]
        m3_signal = row[6]
        m1_signal = row[7]
        w1_signal = row[8]
        w_forecast_display_info = row[9]
        unit = row[10]
        symbol = row[11]

        volatility_risk_st = str(round(volatility_risk_st * 100, 2)) + '%'

        if y1_signal >= 0:
            class_y1 = "text text-success"
        else:
            class_y1 = "text text-danger"

        if m6_signal >= 0:
            class_m6 = "text text-success"
        else:
            class_m6 = "text text-danger"

        if m3_signal >= 0:
            class_m3 = "text text-success"
        else:
            class_m3 = "text text-danger"

        if m1_signal >= 0:
            class_m1 = "text text-success"
        else:
            class_m1 = "text text-danger"

        if w1_signal >= 0:
            class_w1 = "text text-success"
        else:
            class_w1 = "text text-danger"

        if w_forecast_change > -999:
            if w_forecast_change >= 0:
                class_forecast = "bg bg-success text-white"
            else:
                class_forecast = "bg bg-danger text-white"
        else:
            class_forecast = ""


        if unit == 'pips':
            y1_signal = str(round(y1_signal, 0)) + ' pips'
            m6_signal = str(round(m6_signal, 0)) + ' pips'
            m3_signal = str(round(m3_signal, 0)) + ' pips'
            m1_signal = str(round(m1_signal, 0)) + ' pips'
            w1_signal = str(round(w1_signal, 0)) + ' pips'
        else:
            y1_signal = str(round(y1_signal * 100, 2)) + '%'
            m6_signal = str(round(m6_signal * 100, 2)) + '%'
            m3_signal = str(round(m3_signal * 100, 2)) + '%'
            m1_signal = str(round(m1_signal * 100, 2)) + '%'
            w1_signal = str(round(w1_signal * 100, 2)) + '%'

        if not mode == "portf_select":
            if w_forecast_change > -999:
                if w_forecast_change >= 0:
                    order_type = '<span class="badge badge-success">buy</span>'
                else:
                    order_type = '<span class="badge badge-danger">sell</span>'
            else:
                order_type = '<span class="text-secondary">wait</span>'

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

        if mode == 'portf_select':
            target_url = burl + 'p/?ins=2&step='+\
            str(step) +'&uid='+ str(uid) + '&x=' + str(sel)
        if mode == 'view':
            target_url = burl + 's/?uid=' + str(uid)

        return_data = return_data +\
        '    <tr class="sa-table-click-row" data-href="'+ target_url +'">'+\
        column_order_type +\
        '      <td style="text-align: left">'+ '<strong>'+\
        str(fullname)+ '</strong> (' + str(symbol) + ')' + '</td>'+\
        '      <td>'+ str(volatility_risk_st) +'</td>'+\
        column_y1 +\
        column_m6 +\
        column_m3 +\
        column_m1 +\
        column_w1 +\
        '      <td class="'+ class_forecast +'">'+\
        str(w_forecast_display_info) +'</td>'+\
        '    </tr>'
    cursor.close()
    connection.close()
    return return_data

def get_table_content_list_instr_n_portf(burl, mode, what, step, maxrow, sel):
    """ xxx """
    return_data = ''
    if sel is None:
        sel = ''

    if what == 'instr':
        return_data = draw_instr_table(burl, mode, step, maxrow, sel)
    if what == 'portf':
        if user_is_login() == 1:
            return_data = draw_portf_table(burl, maxrow, sel, True)
        if mode != 'dashboard':
            return_data = return_data + draw_portf_table(burl, maxrow, sel, False)
    return return_data

def gen_instr_n_portf_table(burl, mode, what, step, maxrow, sel):
    """ xxx """
    return_data = ''
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

            l_performance_note = '<span style="text-align: center; '+\
            'font-size: x-small;">*Signals performance</span>'

            l_instr_portf = '<th scope="col" style="text-align: left">Instrument</th>'
            l_forc_expect_return = '<th scope="col">1-week Forecast</th>'
        else:
            signal_column = '<th scope="col" style="text-align: left">Rank</th>'
            l_performance_note = ''
            l_instr_portf = '<th scope="col" style="text-align: left">strategy</th>'
            l_forc_expect_return = ''

        c_1_year_column = '<th scope="col">1-Year</th>'
        c_6_month_column = '<th scope="col">6-month</th>'
        c_3_month_column = '<th scope="col">3-month</th>'
        c_1_month_column = '<th scope="col">1-month</th>'
        c_1_week_column = '<th scope="col">1-week</th>'
        small_font_class = "sa-table-sm"

    l_vol_risk_pct = '<th scope="col">Vol. risk (%)</th>'
    if mode == 'dashboard':
        l_vol_risk_pct = '<th scope="col"></th>'

    return_data = ' ' +\
    l_performance_note +\
    '<table id="table_instr_n_portf" class="table table-hover table-sm '+\
    small_font_class +' ">'+\
    '  <thead>'+\
    '    <tr>'+\
    signal_column +\
    l_instr_portf +\
    l_vol_risk_pct +\
    c_1_year_column +\
    c_6_month_column +\
    c_3_month_column +\
    c_1_month_column +\
    c_1_week_column +\
    l_forc_expect_return +\
    '    </tr>'+\
    ' </thead>'+\
    '  <tbody>'+\
    get_table_content_list_instr_n_portf(burl, mode, what, step, maxrow, sel) +\
    '  </tbody>'+\
    '</table>'
    return return_data

def get_box_list_instr_n_portf(burl, mode, what, step, maxrow, sel):
    """ xxx """
    # mode = 'view', mode = 'portf_select', mode = 'dashboard'
    # what = 'instr', what = 'portf'
    # maxrow = numeric number of row ie. 1000
    #  step = step of portfolio selection
    box_content = ''
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
    l_your_portfolios = 'Your Portfolio'
    box_div_class = 'col-lg-12 col-md-12 col-sm-12 col-xs-12'
    portfolio_box_style_dark_mode = theme_return_this('',
                                                      'border-style:solid; '+\
                                                      'border-width:thin; border-color:#343a40;')
    list_title = ''
    list_class = 'sa-center-content sa-list-select-100pct sa-instr-n-portf-list'

    search_box = '<div class="sa-cursor">'+\
    '<input type="text" id="filterInput" name="filterInput" onkeyup="filterTable()" '+\
    'class="form-control" aria-label="Large" '+\
    'aria-describedby="inputGroup-sizing-sm" style="background: transparent; '+\
    theme_return_this('', 'color: white;') +'" placeholder="'+\
    l_placeholder +'" autofocus>'+\
    '<i></i>'+\
    '</div><div>&nbsp;</div>'

    if mode == 'dashboard':
        list_title = '<span class="sectiont"><i class="fas fa-chart-pie"></i>&nbsp;'+\
        l_your_portfolios +'</span>'
        search_box = ''
        list_class = ''
        box_div_class = 'col-lg-12 col-md-12 col-sm-12 col-xs-12 d-none d-lg-block'
    box_content = box_content +\
    '<div class="box">' +\
    '   <div class="row">'+\
    '        <div class="'+ box_div_class +'">'+\
    '            <div class="box-part rounded '+\
    list_class +'" style="'+ portfolio_box_style_dark_mode +'">'+\
    search_box +\
    list_title +\
    gen_instr_n_portf_table(burl, mode, what, step, maxrow, sel) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content
