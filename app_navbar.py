# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *
from sa_func import *
from app_login import *
from sa_db import *
from user_dashboard_count import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_how_menu(burl):
    r = ''
    l_helpTooltip = 'Quick Help over there...'
    try:
        if user_is_login() == 1:
            l_howitworks = '<i class="far fa-question-circle" style="font-size: x-large;"></i>'
        else:
            l_howitworks = 'How it works?'

        l_how_menu = '<li class="nav-item d-none d-sm-block"><a class="nav-link sa-navbar-text" href="'+ burl +'h/" data-toggle="tooltip" data-placement="bottom" data-original-title="'+ l_helpTooltip +'">'+ l_howitworks +'</a></li>'
        r = l_how_menu
    except Exception as e: print(e)
    return r

def get_dashboard_menu(burl):
    r = ''
    try:
        l_dashboard = 'Dashboard'
        i = 0
        num_dashboard_badge = get_num_orders('open') + get_num_orders('close') + get_num_orders('pending')
        l_dashboard_menu = '<li class="nav-item d-none d-sm-block"><a class="nav-link sa-navbar-text" href="'+ burl +'?dashboard=1" data-toggle="tooltip" data-placement="bottom" data-original-title="'+ l_dashboard +'" ><strong>'+ '<i class="fas fa-tachometer-alt" style="font-size: x-large;"></i>' +'</strong><sup><span class="badge badge-pill badge-danger">'+ str(num_dashboard_badge) +'</span></sup></a></li>'
        r = l_dashboard_menu
    except Exception as e: print(e)
    return r

def get_portfolio_button(burl):
    r = ''
    try:
        l_create_portfolio = 'Create a new trading strategy'
        portfolio_button = '<div class="d-none d-sm-block"><a href="'+burl+'p/?ins=1&step=1&button=1" class="btn btn-lg btn-primary d-block d-md-inline-block" style="font-size:large;" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="'+ l_create_portfolio +'"><i class="fas fa-edit"></i></a></div>'
        r = portfolio_button
    except Exception as e: print(e)
    return r

def navbar(burl,disable_search):

    search_placeholder = '<search> function, ticker...'
    sid = get_random_str(9)
    l_join_now_btn = 'Join now'
    l_myportfolio = 'My Portfolio'
    l_themeSwitch = 'Theme: Light/Dark'
    l_settings = 'Settings'
    l_logout = 'Logout'

    search_box = ''
    if disable_search != 1:
        search_box =  ' '+\
        '<img alt="" src="'+ burl+'static/cursor.gif'+'" height="15" class="d-none d-sm-block">'+\
        '    <input id="sa-search-input" onclick="location.href = \''+ burl + 'search/' +'\';"' +\
        '       type="text" name="'+ str(sid) +'" placeholder="'+ search_placeholder +'" aria-label="Search" class="d-none d-sm-block" >'

    if user_is_login() == 1:
        rightsidemenu = '' +\
        get_dashboard_menu(burl) +\
        get_how_menu(burl) +\
        '    <li class="nav-item dropdown">'+\
        '      <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+ '<i class="fas fa-user-circle" style="font-size: x-large;"></i>' +'</a>'+\
        '      <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">'+\
        '        <a class="dropdown-item sa-navbar-text d-none d-sm-block" href="'+ burl + 'ls/?w=portf"><i class="fas fa-chart-pie"></i>&nbsp;'+ l_myportfolio +'</a>'+\
        '        <div class="dropdown-divider"></div>'+\
        '        <a class="dropdown-item sa-navbar-text" href="'+ burl + 'theme/"><i class="fas fa-toggle-on"></i>&nbsp;'+ l_themeSwitch +'</a>'+\
        '        <a class="dropdown-item sa-navbar-text" href="'+ burl + 'settings/"><i class="fas fa-cog"></i>&nbsp;'+ l_settings +'</a>'+\
        '        <a class="dropdown-item sa-navbar-text" href="'+ burl + 'logout/"><i class="fas fa-sign-out-alt"></i>&nbsp;'+ l_logout +'</a>'+\
        '      </div>'+\
        '    </li>'+\
        '<li class="nav-item">'+\
        get_portfolio_button(burl)+\
        '</li>'
    else:
        rightsidemenu = '<strong>'+ get_how_menu(burl) + '</strong>' +'<li class="nav-item"><a href="'+burl+'pricing/" class="btn btn-sm btn-danger btn-block form-signin-btn"><i class="fas fa-sign-in-alt"></i>&nbsp;'+ l_join_now_btn +'</a></li>'

    r = ''+\
    '<nav class="navbar fixed-top navbar-expand-sm navbar-dark bg-dark">'+\
    '<a class="navbar-brand" href="'+ burl +'"><img src="'+ burl+'static/logo.png' +'?'+ get_random_str(9) +'" height="30" alt="logo"></a>'+\
    '<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">'+\
    '  <span class="navbar-toggler-icon"></span>'+\
    '</button>'+\
    '<div class="collapse navbar-collapse" id="navbarSupportedContent">'+\
    search_box +\
    '  <ul class="navbar-nav ml-auto">'+\
    ' '+\
    rightsidemenu +\
    ' '+\
    '  </ul>'+\
    '</div>'+\
    '</nav>'

    return r
