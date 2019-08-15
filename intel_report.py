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

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_report_title():
    content = ''
    try:
        dn = datetime.datetime.now(); dnstr = dn.strftime("%A %d %B, %Y");
        l_title = 'Daily Intelligence Briefing: ' + dnstr
        l_generated_for = 'Report generated for: '

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT name FROM users WHERE id= "+ str( get_user_numeric_id() )
        cr.execute(sql)
        rs = cr.fetchall()
        name = ''
        for row in rs: name = row[0]

        content = content +\
        '<h2>'+ l_title +'</h2>' +\
        l_generated_for + name +\
        '<hr />'
    except Exception as e: print(e)
    return content

def get_intel_content(burl):

    box_content = ''

    try:

        box_content = ''+\
        '<div>' +\
        '<div class="row">' +\
        '    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="box-part rounded">'+ get_report_title() +'</div></div>'+\
        get_signals_lines(burl) +\
        '    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="box-part rounded"></div></div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content

def get_signals_lines(burl):
    content = ''
    try:
        l_title = 'Today\'s Trade(s) Opportunities'
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

        content = '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="box-part rounded"><h4>'+ l_title  +'</h4></div></div>'

        for row in rs:
            uid = row[0]
            content = content +\
            '    <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12"><div class="box-part rounded sa-center-content">'+ get_tradingview_mini_chart(uid,'100%','250','false') +'</div></div>'+\
            '    <div class="col-lg-8 col-md-8 col-sm-12 col-xs-12"><div class="box-part rounded sa-center-content">'+ get_signal_details(uid) + '<span style="font-size: small">'+ get_recomm(uid)  +'</span></div></div>'+\
            '    <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12"><div class="box-part rounded sa-center-content"><hr /></div></div>'
        cr.close()
        connection.close()

    except Exception as e: print(e)
    return content

def get_intel_page(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(),  get_intel_content(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
