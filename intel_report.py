""" Intelligence report """
import pymysql.cursors
from sa_func import get_random_str
import datetime
import time
from datetime import timedelta
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_loading import get_loading_head, get_loading_body
from app_footer import get_page_footer
from app_ogp import set_ogp
from app_title import get_title
from app_metatags import get_metatags
from bootstrap import get_bootstrap
from font_awesome import get_font_awesome
from app_navbar import navbar
from googleanalytics import get_googleanalytics
from app_cookie import theme_return_this, get_sa_theme
from app_stylesheet import get_stylesheet
from signal_details import *
from tradingview_indicators import *
from signal_recom_trail_returns import *
from tradingview_mini_chart import *
from trades_tab import *

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_report_title(burl):
    """ Get title of the report """
    return_data = ''
    dn = datetime.datetime.now(); dnstr = dn.strftime("%A %d %B, %Y");
    l_title = 'Daily Intelligence Briefing: <br />' + dnstr
    l_generated_for = 'Report generated for '
    if user_is_login():
        connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT name FROM users WHERE id= "+ str( get_user_numeric_id() )
        cr.execute(sql)
        rs = cr.fetchall()
        name = ''
        for row in rs: name = row[0]

        return_data = return_data +\
        '<h1>'+ l_title +'</h1>' +\
        l_generated_for + '<strong>'+ name.capitalize() + '</strong>'+\
        '<hr />'
    else:
        return_data = return_data +\
        '<h1>'+ l_title +'</h1>' +\
        'This report is only accessible to members only. '+\
        '<a href="'+ burl +'signin/?redirect='+ burl +'intelligence">Sign In</a>'
    return return_data

def get_market_snapshot_n_brief_text(w):
    """ Get market snapshot briefing text """
    return_data = ''
    language = 'en'
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT market_snapshot FROM reports WHERE lang='"+ language +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    market_snapshot = ''
    for row in rs: market_snapshot = row[0]

    if w == 'market_snapshot':
        return_data = market_snapshot
    return return_data

def get_market_snapshot_section():
    """ Get the market snapshot section """
    return_data = ''
    l_title = 'Market Snapshot'

    uid_worldstocks = 544
    uid_eem = 540
    uid_gold = 39
    uid_btc = 7
    uid_jpy = 575
    uid_tlt = 163

    if user_is_login():
        return_data = ''+\
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
    return return_data

def get_intel_content(burl):
    """ Get intelligence report content """
    box_content = ''
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
    return box_content

def get_expired_signals(burl):
    """ Get expired signals table """
    return_data = ''
    if user_is_login():
        l_title = 'Expired Signals'
        dn = datetime.datetime.now() - ( timedelta(days=7) ); dnstr = dn.strftime("%A %d %B, %Y");
        l_comment = 'Signals with orders entered on <strong>' + dnstr + '</strong> and before are now expired and may be closed or managed at your own discretion.'
        return_data = ''+\
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
    return return_data

def get_signals_lines(burl):
    """ Get signals lines """
    return_data = ''
    if user_is_login():
        l_title = 'Opportunities'
        dn = datetime.datetime.now(); dnstr = dn.strftime("%Y%m%d");
        connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
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
        return_data = ''+\
        '<div class="row">' +\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '<div class="col-lg-10 col-md-10 col-sm-12 col-xs-12"><div class="box-part rounded"><h2>'+ l_title  +'</h2></div></div>'+\
        '</div>'

        for row in rs:
            uid = row[0]
            return_data = return_data +\
            '<div class="row">' +\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '    <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12"><div class="box-part rounded">'+ get_tradingview_mini_chart(uid,'100%','200','false','1m',1) +'</div></div>'+\
            '    <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12"><div class="box-part rounded">'+ get_signal_details(uid,burl,'desc') + '<span style="font-size: small">'+ get_recomm(uid)  +'</span></div></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '</div>'
        cr.close()
        connection.close()
    return return_data

def get_intel_page(appname,burl):
    """ Get and build the entire intelligence report page """
    return_data = ''
    return_data = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + redirect_if_not_logged_in(burl,burl +'intelligence') + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_font_awesome() + get_stylesheet(burl) )
    return_data = return_data + get_body( get_loading_body(),  navbar(burl,0) + get_intel_content(burl) )
    return_data = set_page(return_data)
    return return_data
