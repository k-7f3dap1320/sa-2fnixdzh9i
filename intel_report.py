""" Intelligence report """
import datetime
from datetime import timedelta
import pymysql.cursors
from sa_func import get_user_numeric_id, redirect_if_not_logged_in
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_loading import get_loading_head, get_loading_body
from app_ogp import set_ogp
from app_title import get_title
from app_metatags import get_metatags
from bootstrap import get_bootstrap
from font_awesome import get_font_awesome
from app_navbar import navbar
from googleanalytics import get_googleanalytics
from print_google_ads import print_google_ads
from app_cookie import get_sa_theme, user_is_login
from app_stylesheet import get_stylesheet
from signal_details import get_signal_details
from signal_recom_trail_returns import get_recomm
from tradingview_mini_chart import get_tradingview_mini_chart
from trades_tab import get_trades_tbl
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def report_is_available():
    """ check if report is available and generated """
    ret = False
    date_now = datetime.datetime.now()

    not_weekend = False
    if date_now.weekday() != 5:
        if date_now.weekday() != 6:
            not_weekend = True

    date_now = date_now.strftime("%Y%m%d")
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT COUNT(*) FROM log '+\
    'WHERE date_time >= '+ str(date_now) +\
    ' AND module = "Data update terminated" AND status = 1'
    cursor.execute(sql)
    res = cursor.fetchall()
    data_generated = 0
    for row in res:
        data_generated = row[0]
    cursor.close()
    connection.close()

    if data_generated != 0:
        if not_weekend:
            ret = True

    return ret

def get_report_title(burl):
    """ Get title of the report """
    return_data = ''
    date_now = datetime.datetime.now()
    dnstr = date_now.strftime("%A %d %B, %Y")
    l_title = 'Daily Intelligence Briefing: <br />' + dnstr
    l_generated_for = 'Report generated for '
    if user_is_login():
        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT name FROM users WHERE id= "+ str(get_user_numeric_id())
        cursor.execute(sql)
        res = cursor.fetchall()
        name = ''
        for row in res:
            name = row[0]
        cursor.close()
        connection.close()

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

def get_market_snapshot_n_brief_text(what):
    """ Get market snapshot briefing text """
    return_data = ''
    language = 'en'
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT market_snapshot FROM reports WHERE lang='"+ language +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    market_snapshot = ''
    for row in res:
        market_snapshot = row[0]
    cursor.close()
    connection.close()

    if what == 'market_snapshot':
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
        '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12">'+\
        '<div class="box-part rounded"><h2>'+ l_title  +'</h2></div></div>'+\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12 d-none d-md-block"></div>'+\
        '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block">'+\
        '<div class="box-part rounded">'+\
        get_tradingview_mini_chart(uid_worldstocks, '100%', '160', 'false', '6m', 0) +\
        '</div></div>'+\
        '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block">'+\
        '<div class="box-part rounded">'+\
        get_tradingview_mini_chart(uid_eem, '100%', '160', 'false', '6m', 0) +\
        '</div></div>'+\
        '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block">'+\
        '<div class="box-part rounded">'+\
        get_tradingview_mini_chart(uid_gold, '100%', '160', 'false', '6m', 0) +\
        '</div></div>'+\
        '    <div class="col-lg-2 col-md-2 col-sm-12 col-xs-12 d-none d-md-block"></div>'+\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12 d-none d-md-block"></div>'+\
        '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block">'+\
        '<div class="box-part rounded">'+\
        get_tradingview_mini_chart(uid_btc, '100%', '160', 'false', '6m', 0) +\
        '</div></div>'+\
        '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block">'+\
        '<div class="box-part rounded">'+\
        get_tradingview_mini_chart(uid_jpy, '100%', '160', 'false', '6m', 0) +\
        '</div></div>'+\
        '    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-6 d-none d-md-block">'+\
        '<div class="box-part rounded">'+\
        get_tradingview_mini_chart(uid_tlt, '100%', '160', 'false', '6m', 0) +\
        '</div></div>'+\
        '    <div class="col-lg-2 col-md-2 col-sm-12 col-xs-12 d-none d-md-block"></div>'+\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12">'+\
        '<div class="box-part rounded">'+\
        get_market_snapshot_n_brief_text('market_snapshot') +\
        '<br /><br />'+\
        '<div style="text-align: center; overflow: hidden;">'+\
        print_google_ads('leaderboard', 'none') +\
        '</div>'+\
        '</div></div>'+\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '</div>'
    return return_data

def get_intel_content(burl, terminal):
    """ Get intelligence report content """
    box_content = ''

    l_report_not_available = 'The report is being compiled. '+\
    'You will receive an email once the report will be available.'

    if report_is_available():
        report_content = ''+\
        get_market_snapshot_section() +\
        get_signals_lines(burl, terminal) +\
        get_expired_signals(burl)
    else:
        report_content = ''+\
        '<div class="alert alert-info" role="alert">'+\
        l_report_not_available +\
        '</div>'

    box_content = ''+\
    '<div class="box-top">'+\
    '<div class="row">' +\
    '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
    '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12">'+\
    '<div class="box-part rounded">'+ get_report_title(burl) +'</div></div>'+\
    '</div>'+\
    report_content +\
    '<div class="row">' +\
    '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
    '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12">'+\
    '<div class="box-part rounded"></div></div>'+\
    '</div>'+\
    '</div>'
    return box_content

def get_expired_signals(burl):
    """ Get expired signals table """
    return_data = ''
    if user_is_login():
        l_title = 'Expired Signals'
        date_minus_seven = datetime.datetime.now() - (timedelta(days=7))
        dnstr = date_minus_seven.strftime("%A %d %B, %Y")
        l_comment = 'Signals with orders entered on <strong>' +\
        dnstr + '</strong> '+\
        'and before are now expired and may be closed or managed at your own discretion.'
        return_data = ''+\
        '<div class="row">' +\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '    <div class="col-lg-10 col-md-10 col-sm-12 col-xs-12">'+\
        '<div class="box-part rounded">'+\
        '<div style="text-align: center; overflow: hidden;">'+\
        print_google_ads('leaderboard', 'none') +\
        '</div>'+\
        '<br />'+\
        '<h2>'+ l_title  +'</h2>'+\
        '</div></div>'+\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '</div>'+\
        '<div class="row">' +\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '    <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">'+\
        '<div class="box-part rounded">'+ l_comment +\
        '</div></div>'+\
        '    <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '<div class="box-part rounded">'+\
        get_trades_tbl(0, 'today', burl, 'expired') +\
        '</div></div>'+\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '</div>'
    return return_data

def get_signals_lines(burl, terminal):
    """ Get signals lines """
    return_data = ''
    signal_available = False
    if user_is_login():
        l_title = 'Opportunities'
        l_customize_label = 'Customize your Report'
        l_customize_link = '<span style="font-size: small;">[<a href="'+\
        burl +'p/?ins=1&step=1">'+\
        l_customize_label +'</a>]</span>'
        date_now = datetime.datetime.now()
        dnstr = date_now.strftime("%Y%m%d")

        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT DISTINCT "+\
            "trades.uid "+\
            "FROM trades "+\
            "JOIN portfolios ON portfolios.symbol = trades.symbol "+\
            "JOIN instruments ON instruments.symbol = portfolios.portf_symbol "+\
            "JOIN instruments as a_alloc ON a_alloc.symbol = portfolios.symbol "+\
            "WHERE "+\
            "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
            "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
            "OR (portfolios.strategy_order_type = 'long/short') ) AND "+\
            "(trades.entry_date >= " + dnstr + " AND instruments.owner = " +\
            str(get_user_numeric_id()) + " AND status = 'active')"
        cursor.execute(sql)
        res = cursor.fetchall()
        return_data = ''+\
        '<div class="row">' +\
        '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
        '<div class="col-lg-10 col-md-10 col-sm-12 col-xs-12">'+\
        '<div class="box-part rounded">'+\
        '<h2>'+ l_title + '</h2>'+\
        l_customize_link +\
        '</div></div>'+\
        '</div>'
        for row in res:
            signal_available = True
            uid = row[0]
            return_data = return_data +\
            '<div class="row">' +\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '    <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">'+\
            '<div class="box-part rounded">'+\
            get_tradingview_mini_chart(uid, '100%', '200', 'false', '1m', 1) +\
            '</div></div>'+\
            '    <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
            '<div class="box-part rounded">'+ get_signal_details(uid, burl, 'desc', terminal) +\
            '<span style="font-size: small">'+ get_recomm(uid)  +'</span>'+\
            '</div></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-12 col-xs-12"></div>'+\
            '</div>'
        cursor.close()
        connection.close()

    if not signal_available:
        return_data = return_data +\
        'There is no trading signal according to your strategy for today.'

    return return_data

def get_intel_page(appname, burl, terminal):
    """ Get and build the entire intelligence report page """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           redirect_if_not_logged_in(burl, burl +'intelligence') +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_intel_content(burl, terminal),'')

    return_data = set_page(return_data)
    return return_data
