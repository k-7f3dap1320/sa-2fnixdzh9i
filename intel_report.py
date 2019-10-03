# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from sa_func import *
import datetime
import time
from datetime import timedelta
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *
from app_cookie import *
from app_stylesheet import *
from signal_details import *
from tradingview_indicators import *
from signal_recom_trail_returns import *
from tradingview_mini_chart import *
from trades_tab import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_report_title(burl):
    content = ''
    try:
        dn = datetime.datetime.now(); dnstr = dn.strftime("%A %d %B, %Y");
        l_title = 'Daily Intelligence Briefing: <br />' + dnstr
        l_generated_for = 'Report generated for '


        if user_is_login():
            connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT name FROM users WHERE id= "+ str( get_user_numeric_id() )
            cr.execute(sql)
            rs = cr.fetchall()
            name = ''
            for row in rs: name = row[0]

            content = content +\
            '<h1>'+ l_title +'</h1>' +\
            l_generated_for + '<strong>'+ name.capitalize() + '</strong>'+\
            '<hr />'
        else:
            content = content +\
            '<h1>'+ l_title +'</h1>' +\
            'This report is only accessible to members only. '+\
            '<a href="'+ burl +'signin/?redirect='+ burl +'intelligence">Sign In</a>'

    except Exception as e: print(e)
    return content

def get_market_snapshot_n_brief_text(w):
    r = ''
    try:
        language = 'en'
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT market_snapshot FROM reports WHERE lang='"+ language +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        market_snapshot = ''
        for row in rs: market_snapshot = row[0]

        if w == 'market_snapshot':
            r = market_snapshot

    except Exception as e: print(e)
    return r

def get_market_snapshot_section():
    content = ''
    try:
        l_title = 'Market Snapshot'

        uid_worldstocks = 544
        uid_eem = 540
        uid_gold = 39
        uid_btc = 7
        uid_jpy = 575
        uid_tlt = 163

        if user_is_login():
            content = ''+\
            '<div class="row">' +\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12"><div class="box-part rounded"><h2>'+ l_title  +'</h2></div></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12 d-none d-md-block"></div>'+\
            '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block"><div class="box-part rounded">'+ get_tradingview_mini_chart(uid_worldstocks,'100%','160','false','6m',0) +'</div></div>'+\
            '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block"><div class="box-part rounded">'+ get_tradingview_mini_chart(uid_eem,'100%','160','false','6m',0) +'</div></div>'+\
            '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block"><div class="box-part rounded">'+ get_tradingview_mini_chart(uid_gold,'100%','160','false','6m',0) +'</div></div>'+\
            '    <div class="col-lg-2 col-md-2 col-sm-12 col-xs-12 d-none d-md-block"></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12 d-none d-md-block"></div>'+\
            '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block"><div class="box-part rounded">'+ get_tradingview_mini_chart(uid_btc,'100%','160','false','6m',0) +'</div></div>'+\
            '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block"><div class="box-part rounded">'+ get_tradingview_mini_chart(uid_jpy,'100%','160','false','6m',0) +'</div></div>'+\
            '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block"><div class="box-part rounded">'+ get_tradingview_mini_chart(uid_tlt,'100%','160','false','6m',0) +'</div></div>'+\
            '    <div class="col-lg-2 col-md-2 col-sm-12 col-xs-12 d-none d-md-block"></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12"><div class="box-part rounded">'+ get_market_snapshot_n_brief_text('market_snapshot')  +'</div></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '</div>'

    except Exception as e: print(e)
    return content

def get_intel_content(burl):

    box_content = ''

    try:

        box_content = ''+\
        '<div class="box-top">'+\
        '<div class="row">' +\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12"><div class="box-part rounded">'+ get_report_title(burl) +'</div></div>'+\
        '</div>'+\
        get_market_snapshot_section() +\
        get_signals_lines(burl) +\
        get_expired_signals(burl) +\
        '<div class="row">' +\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12"><div class="box-part rounded"></div></div>'+\
        '</div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content

def get_expired_signals(burl):
    content = ''
    try:
        if user_is_login():
            l_title = 'Expired Signals'
            dn = datetime.datetime.now() - ( timedelta(days=7) ); dnstr = dn.strftime("%A %d %B, %Y");
            l_comment = 'Signals with orders entered on <strong>' + dnstr + '</strong> and before are now expired and may be closed or managed at your own discretion.'
            content = ''+\
            '<div class="row">' +\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12"><div class="box-part rounded"><h2>'+ l_title  +'</h2></div></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '</div>'+\
            '<div class="row">' +\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '    <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12"><div class="box-part rounded">'+ l_comment +'</div></div>'+\
            '    <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div class="box-part rounded">'+ get_trades_tbl(0,'today',burl,'expired') + '</div></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '</div>'
    except Exception as e: print(e)
    return content

def get_signals_lines(burl):
    content = ''
    try:
        if user_is_login():
            l_title = 'Opportunities'
            dn = datetime.datetime.now(); dnstr = dn.strftime("%Y%m%d");
            connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql ="SELECT DISTINCT "+\
                "trades.uid "+\
                "FROM trades "+\
                "JOIN portfolios ON portfolios.symbol = trades.symbol "+\
                "JOIN instruments ON instruments.symbol = portfolios.portf_symbol "+\
                "JOIN instruments as a_alloc ON a_alloc.symbol = portfolios.symbol "+\
                "WHERE "+\
                "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
                "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
                "OR (portfolios.strategy_order_type = 'long/short') ) AND "+\
                "(trades.entry_date >= " + dnstr + " AND instruments.owner = " + str(get_user_numeric_id()) + " AND status = 'active')"
            cr.execute(sql)
            rs = cr.fetchall()
            content = ''+\
            '<div class="row">' +\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '<div class="col-lg-10 col-md-10 col-sm-12 col-xs-12"><div class="box-part rounded"><h2>'+ l_title  +'</h2></div></div>'+\
            '</div>'

            for row in rs:
                uid = row[0]
                content = content +\
                '<div class="row">' +\
                '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
                '    <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12"><div class="box-part rounded">'+ get_tradingview_mini_chart(uid,'100%','200','false','1m',1) +'</div></div>'+\
                '    <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div class="box-part rounded">'+ get_signal_details(uid) + '<span style="font-size: small">'+ get_recomm(uid)  +'</span></div></div>'+\
                '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
                '</div>'
            cr.close()
            connection.close()

    except Exception as e: print(e)
    return content

def get_intel_page(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + redirect_if_not_logged_in(burl,burl +'intelligence') + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(),  navbar(burl,0) + get_intel_content(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
