# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_footer import *
from app_head import *
from app_ogp import *
from app_metatags import *
from app_title import *
from app_body import *
from app_cookie import *
from bootstrap import *
from google_chart import *
from app_loading import *
from app_stylesheet import *
from awesomplete import *
from tablesorter import *
from app_navbar import *
from details_header import *
from signal_details import *
from signal_ta_chart_alt_orders import *
from signal_recom_trail_returns import *
from trades_tab import *
from font_awesome import *
from googleanalytics import *
from googleadsense import *
from sa_db import *
from sa_func import *
from signal_returns_colchart import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_uid_from_tvs(tvws):
    r = 0
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT uid FROM symbol_list WHERE tradingview ='"+ str(tvws) +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_sign_header(uid):
    content = ''
    try:
        content = ' '+\
        '        <div class="col-lg-7 col-md-7 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        get_signal_details(uid) +\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-5 col-md-5 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded" >'+\
        get_signal_return_colchart(uid) +\
        '            </div>'+\
        '        </div>'
    except Exception as e: print(e)
    return content

def gen_sign_page(uid,tvws,appname,burl):

    try:
        if tvws is not None: uid = get_uid_from_tvs(tvws)
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.fullname FROM `symbol_list` JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
            "WHERE symbol_list.uid = " + str(uid)

        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            instfullname = row[0]

        page_title = 'This is how we decide to trade ' + instfullname
        page_desc = 'Access to thousands of financial instruments, stocks, forex, commodities & cryptos analysis and recommendations.'
        r = get_head(  get_loading_head() + get_googleanalytics() + get_googleadsense() + get_title( appname +' - ' + instfullname ) + get_metatags(burl) + redirect_if_not_logged_in(burl,'') + set_ogp(burl,2,page_title,page_desc) + get_bootstrap( get_sa_theme(),burl ) + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_google_chart_script() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + '<div class="box-top"><div class="row">' + get_details_header(uid,burl) + get_sign_header(uid) + get_sign_ta_chart_alt_orders(uid) + get_sign_recommend_trail_returns(uid) + get_trades_box(uid,burl,None) + '</div></div>' + get_page_footer(burl))
        r = set_page(r)

        cr.close()
        connection.close()
    except Exception as e: print(e)

    return r
