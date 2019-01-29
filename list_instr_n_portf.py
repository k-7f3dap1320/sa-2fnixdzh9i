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

                if w_forecast_change >=0:
                    order_type = '<span class="badge badge-success">buy</span>'
                else:
                    order_type = '<span class="badge badge-danger">sell</span>'

                if mode == 'portf_select': target_url = burl + 'p/?ins=2&step='+ str(step) +'&uid='+ str(uid)
                if mode == 'view': target_url = burl + 's/?uid=' + str(uid)

                r = r +\
                '    <tr class="sa-table-click-row" data-href="'+ target_url +'">'+\
                '      <th scope="row">'+ order_type +'</th>'+\
                '      <td>'+ '<strong>'+str(fullname)+ '</strong> (' + str(symbol) + ')' + '</td>'+\
                '      <td>'+ str(volatility_risk_st) +'</td>'+\
                '      <td>'+ str(y1_signal) +'</td>'+\
                '      <td>'+ str(m6_signal) +'</td>'+\
                '      <td>'+ str(m3_signal) +'</td>'+\
                '      <td>'+ str(m1_signal) +'</td>'+\
                '      <td>'+ str(w1_signal) +'</td>'+\
                '      <td>'+ str(w_forecast_display_info) +'</td>'+\
                '    </tr>'
            cr.close()
            connection.close()

    except Exception as e: print(e)
    return r


def gen_instr_n_portf_table(burl,mode,what,step,portf,maxrow,x):

    r = ''
    try:

        r = '' +\
        '<table class="table table-hover table-sm sa-table-sm">'+\
        '  <thead>'+\
        '    <tr>'+\
        '      <th scope="col">Signal</th>'+\
        '      <th scope="col">Instrument</th>'+\
        '      <th scope="col">Volatility risk (%)</th>'+\
        '      <th scope="col">1-Year</th>'+\
        '      <th scope="col">6-month</th>'+\
        '      <th scope="col">3-month</th>'+\
        '      <th scope="col">1-month</th>'+\
        '      <th scope="col">1-week</th>'+\
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

    box_content = ''

    try:

        box_content = '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-center-content sa-list-select-100pct">'+\
        gen_instr_n_portf_table(burl,mode,what,step,portf,maxrow,x)
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


        cr.close()
        connection.close()

    except Exception as e: print(e)

    return box_content
