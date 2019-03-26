# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from search import *
from sa_func import *
from app_login import *
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_top_signals_menu(burl):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT * FROM instruments  WHERE instruments.symbol NOT LIKE '%"+ get_portf_suffix() +"%' AND w1_signal > 0"
        cr.execute(sql)
        rs = cr.fetchall()
        i = 0
        for row in rs: i += 1
        l_top_signal = 'Top Signals'
        link = burl + 'ls/?w=instr&x='
        r = '<li class="nav-item"><a class="nav-link" href="'+ link +'">'+ l_top_signal +'&nbsp;<sup><span class="badge badge-pill badge-info">'+ str(i) +'</span></sup></a></li>'
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_top_trader_menu(burl):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.w1 FROM instruments JOIN feed ON feed.symbol = instruments.symbol WHERE instruments.symbol LIKE '%"+ get_portf_suffix() +"%' AND instruments.w1 > 0 AND feed.globalrank <=200"
        cr.execute(sql)
        rs = cr.fetchall()
        i = 0
        for row in rs: i += 1
        l_top_trader = 'Top Traders'
        link = burl + 'ls/?w=portf&x='
        r = '<li class="nav-item"><a class="nav-link" href="'+ link +'">'+ l_top_trader +'&nbsp;<sup><span class="badge badge-pill badge-info">'+ str(i) +'</span></sup></a></li>'
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_market_menu_selection(burl):
    r = ''
    try:
        l_select_market = 'Select Market'
        l_all_market_selection = 'Show all markets'
        asset_class_selection = ''
        markets_selection = ''
        l_markets_caption = '{market} Market'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT asset_class_id, asset_class_name FROM Asset_class ORDER BY asset_class_name"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            asset_class_id = row[0]
            asset_class_name = row[1]
            if asset_class_id != 'MA:' and asset_class_id != 'PF:':
                asset_class_selection = asset_class_selection + '<a class="dropdown-item" href="'+ burl + '?x='+ str(asset_class_id) +'">'+ str(asset_class_name) +'</a>'

        sql = "SELECT market_id, market_label FROM Markets"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            market_id = row[0]
            market_label = row[1]
            markets_selection = markets_selection + '<a class="dropdown-item" href="'+ burl + '?x='+ str(market_id) +'">'+ str(l_markets_caption.replace('{market}',market_label) ) +'</a>'

        r = '' +\
        '    <li class="nav-item dropdown">'+\
        '      <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+ l_select_market +'</a>'+\
        '      <div class="dropdown-menu" aria-labelledby="navbarDropdown">'+\
        '        <a class="dropdown-item" href="'+ burl + '?x=">'+ l_all_market_selection +'</a>'+\
        '        <div class="dropdown-divider"></div>'+\
        asset_class_selection +\
        '        <div class="dropdown-divider"></div>'+\
        markets_selection +\
        '      </div>'+\
        '    </li>'

        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r

def navbar(burl):

    search_placeholder = 'Enter function, ticker or search. Hit <enter> to go.'
    sid = get_random_str(9)
    l_join_now_btn = 'Join now'
    l_dashboard = 'Dashboard'
    l_myportfolio = 'My Portfolio(s)'
    l_settings = 'Settings'
    l_logout = 'Logout'
    l_create_portfolio = 'Create a new portfolio'
    l_portf_call_action_header = 'We are working on it...'
    l_portf_call_action_body = 'Oh! Sorry for now as we are still under development, SmartAlpha is limited to one portfolio per member. '+\
    'If you want to create a new portfolio you must [delete] your current one first. You can just go to your list of portfolio to proceed.'
    l_portf_call_action_button_list = 'View my list of portfolio'

    modal_portf_call_action = '' +\
    '  <div class="modal" id="portf_call_action">'+\
    '    <div class="modal-dialog">'+\
    '      <div class="modal-content">'+\
    '        <div class="modal-header">'+\
    '          <h4 class="modal-title">'+ l_portf_call_action_header +'</h4>'+\
    '          <button type="button" class="close" data-dismiss="modal">&times;</button>'+\
    '        </div>'+\
    '        <div class="modal-body">'+\
    l_portf_call_action_body +\
    '        </div>'+\
    '        <!-- Modal footer -->'+\
    '        <div class="modal-footer">'+\
    '          <a href="'+ burl + 'ls/?w=portf' +'" type="button" class="btn btn-info">'+ l_portf_call_action_button_list +'</a>'+\
    '        </div>'+\
    '      </div>'+\
    '    </div>'+\
    '  </div>'


    if allowed_multiple_portf() == True:
        portfolio_button = '<a href="'+burl+'p/?ins=1&step=1" class="btn btn-lg btn-primary" style="font-size:x-large;" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="'+ l_create_portfolio +'"><i class="fas fa-edit"></i></a>'
    else:
        portfolio_button = '<button type="button" class="btn btn-lg btn-primary" style="font-size:x-large;" data-placement="bottom" title="" data-original-title="'+ l_create_portfolio +'" data-toggle="modal" data-target="#portf_call_action"><i class="fas fa-edit"></i></button>'

    if user_is_login() == 1:
        rightsidemenu = '' +\
        '    <li class="nav-item dropdown">'+\
        '      <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+ get_avatar(burl,18)+'&nbsp;'+ get_nickname() +'</a>'+\
        '      <div class="dropdown-menu" aria-labelledby="navbarDropdown">'+\
        '        <a class="dropdown-item" href="'+ burl + '"><i class="fas fa-user"></i>&nbsp;'+ l_dashboard +'</a>'+\
        '        <a class="dropdown-item" href="'+ burl + 'ls/?w=portf"><i class="fas fa-chart-pie"></i>&nbsp;'+ l_myportfolio +'</a>'+\
        '        <div class="dropdown-divider"></div>'+\
        '        <a class="dropdown-item disabled" href="'+ burl + 'settings"><i class="fas fa-cog"></i>&nbsp;'+ l_settings +'</a>'+\
        '        <a class="dropdown-item" href="'+ burl + 'logout"><i class="fas fa-sign-out-alt"></i>&nbsp;'+ l_logout +'</a>'+\
        '      </div>'+\
        '    </li>' +\
        portfolio_button
    else:
        rightsidemenu = '<a href="'+burl+'n/?uid=0" class="btn btn-sm btn-danger btn-block form-signin-btn"><i class="fas fa-sign-in-alt"></i>&nbsp;'+ l_join_now_btn +'</a>'

    r = ''+\
    '<nav class="navbar fixed-top navbar-expand-sm navbar-dark bg-dark">'+\
    '<a class="navbar-brand" href="'+ burl +'"><img src="'+ burl+'static/logo.png' +'?'+ get_random_str(9) +'" height="30"></a>'+\
    '<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">'+\
    '  <span class="navbar-toggler-icon"></span>'+\
    '</button>'+\
    '<div class="collapse navbar-collapse" id="navbarSupportedContent">'+\
    '  <form class="form-inline my-2 my-lg-0" action="'+ burl +'" method="get" >'+\
    '    <input id="sa-search-input" class="form-control mr-lg-4 btn-outline-info awesomplete"' +\
    '       type="search" name="'+ str(sid) +'" placeholder="'+ search_placeholder +'" aria-label="Search" id="navBarSearchForm" data-list="'+ get_search_suggestions() +'" >'+\
    '     <input type="hidden" name="sid" value="'+ str(sid) +'">'+\
    '  </form>'+\
    '  <ul class="navbar-nav mr-auto">'+\
    get_market_menu_selection(burl) +\
    '&nbsp;'+\
    get_top_trader_menu(burl) +\
    '&nbsp;'+\
    get_top_signals_menu(burl) +\
    '&nbsp;'+\
    '  </ul>'+\
    '  <ul class="navbar-nav ml-auto">'+\
    '      <li class="nav-item">'+\
    rightsidemenu +\
    '      </li>'+\
    '  </ul>'+\
    '</div>'+\
    '</nav>'+\
    modal_portf_call_action

    return r
