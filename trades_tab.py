# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from sa_func import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_trades_tbl(uid,w):

    r = ''
    #try:
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)

    selected_symbol = ''
    selected_is_portf = False
    is_user_prf = False
    sql = "SELECT symbol FROM symbol_list WHERE uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: selected_symbol = row[0]
    if not selected_symbol.find( get_portf_suffix() ) == -1: selected_is_portf = True
    if uid == 0: is_user_prf = True

    user_symbol_selection = ''
    i = 0
    if is_user_prf:
        sql = "SELECT DISTINCT portfolios.symbol FROM instruments JOIN portfolios ON instruments.symbol = portfolios.portf_symbol WHERE instruments.owner = '"+ get_user() +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            if i == 0: user_symbol_selection = user_symbol_selection + " AND (trades.symbol = '"+ str(row[0]) +"' "
            else: user_symbol_selection = user_symbol_selection + " OR trades.symbol = '"+ str(row[0]) +"' "
            i += 1
        user_symbol_selection = user_symbol_selection +') '

    portf_symbol_selection = ''
    i = 0
    if selected_is_portf:
        sql = "SELECT portfolios.symbol FROM symbol_list JOIN portfolios ON symbol_list.symbol = portfolios.portf_symbol WHERE symbol_list.uid = "+ str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            if i == 0: portf_symbol_selection = portf_symbol_selection + " AND (trades.symbol = '"+ str(row[0]) +"' "
            else: portf_symbol_selection = portf_symbol_selection + " OR trades.symbol = '"+ str(row[0]) +"' "
            i += 1
        portf_symbol_selection = portf_symbol_selection + ') '

    single_selection = ''
    if not selected_is_portf and not is_user_prf: single_selection = 'AND trades.uid = ' + str(uid)

    sql = "SELECT trades.order_type, "+\
        "trades.fullname, "+\
        "trades.entry_date,  "+\
        "trades.entry_price, "+\
        "trades.close_price, "+\
        "trades.expiration_date, "+\
        "trades.pnl_pct,  "+\
        "trades.url,  "+\
        "instruments.unit "
    sql = sql + "FROM trades JOIN instruments ON trades.symbol = instruments.symbol WHERE "

    if w == 'active': sql = sql + "trades.status = 'active' "
    else: sql = sql + "trades.status = 'expired' "

    sql = sql + single_selection
    sql = sql + user_symbol_selection
    sql = sql + portf_symbol_selection
    sql = sql + 'order by trades.entry_date DESC'
    print(sql)
    cr.execute(sql)
    rs = cr.fetchall()

    l_order = 'Order'
    l_instrument = 'Instrument'
    l_entry_date = 'Entry date'
    l_open_price = 'Open price'
    l_close_price = 'Close price'
    l_expiration_date = 'Expiration date'
    l_pnl = 'PnL'

    r = ''+\
    '<table class="table table-hover table-sm sa-table-sm">'+\
    '  <thead>'+\
    '    <tr>'+\
    '      <th scope="col">'+ l_order +'</th>'+\
    '      <th scope="col">'+ l_instrument +'</th>'+\
    '      <th scope="col">'+ l_entry_date +'</th>'+\
    '      <th scope="col">'+ l_open_price +'</th>'
    if w == 'expired': r = r + '<th scope="col">'+ l_close_price +'</th>'
    r = r +\
    '      <th scope="col">'+ l_expiration_date +'</th>'+\
    '      <th scope="col">'+ l_pnl +'</th>'+\
    '    </tr>'+\
    '  </thead>'+\
    '  <tbody>'

    for row in rs:
        order_type = row[0]
        fullname = row[1]
        entry_date = row[2].strftime("%d-%b-%Y")
        entry_price = row[3]
        close_price = row[4]
        expiration_date = row[5].strftime("%d-%b-%Y")
        pnl_pct = row[6]
        url = row[7]
        unit = row[8]

        if order_type == 'buy': badge_class = 'badge badge-success'
        else: badge_class = 'badge badge-danger'
        if pnl_pct >= 0: text_class = 'text text-success'
        else: text_class = 'text text-danger'
        if unit == 'pips':
            pnl_pct = round( pnl_pct *10000, 2)
            if pnl_pct > 1: str( pnl_pct ) + " pips"
            else: str( pnl_pct ) + " pip"
        else: pnl_pct = str( round( pnl_pct * 100, 2 ) ) + "%"

        r = r +\
        '    <tr>'+\
        '      <td><span class="'+ badge_class +'">'+ str(order_type) +'</span></td>'+\
        '      <td>'+ str(fullname) +'</td>'+\
        '      <td>'+ str(entry_date) +'</td>'+\
        '      <td>'+ str(entry_price) +'</td>'
        if w == 'expired': r = r + '<td>'+ str(close_price) +'</td>'
        r = r +\
        '      <td>'+ str(expiration_date) +'</td>'+\
        '      <td><span class="'+ text_class +'">'+ str(pnl_pct) +'</span></td>'+\
        '    </tr>'

    r = r +\
    '  </tbody>'+\
    '</table>'
    cr.close()
    connection.close()
    #except Exception as e: print(e)
    return r




def get_trades_box(uid,burl):

    box_content = ''

    try:

        if not uid == 0 or not get_user() == None:
            l_tab_active_title = 'Active trade(s)'; tab_active_id = 'active_trades'
            l_tab_expired_title = 'Closed trade(s)'; tab_expired_id = 'expired_trades'
            box_content = '' +\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="box-part">'+\
            '               <ul id="sa-tab-sm" class="nav nav-tabs" role="tablist">'+\
            '                   <li class="nav-item">'+\
            '                       <a class="nav-link active" data-toggle="pill" href="#'+ tab_active_id +'">'+ l_tab_active_title +'</a>'+\
            '                   </li>'+\
            '                   <li class="nav-item">'+\
            '                       <a class="nav-link" data-toggle="pill" href="#'+ tab_expired_id +'">'+ l_tab_expired_title +'</a>'+\
            '                   </li>'+\
            '               </ul>'+\
            '               <div class="tab-content">'+\
            '                   <div id="'+ tab_active_id +'" class="container tab-pane active"><div>&nbsp;</div>'+ get_trades_tbl(uid,'active') +'</div>'+\
            '                   <div id="'+ tab_expired_id +'" class="container tab-pane fade"><div>&nbsp;</div>'+ get_trades_tbl(uid,'expired') +'</div>'+\
            '               </div>'+\
            '            </div>'+\
            '        </div>'

    except Exception as e: print(e)

    return box_content
