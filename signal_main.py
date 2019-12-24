""" Signal main functions """
import pymysql.cursors
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_footer import get_page_footer
from app_ogp import set_ogp
from app_metatags import get_metatags
from app_title import get_title
from app_cookie import theme_return_this, get_sa_theme
from bootstrap import get_bootstrap
from google_chart import get_google_chart_script
from app_loading import get_loading_head, get_loading_body
from app_stylesheet import get_stylesheet
from app_navbar import navbar
from details_header import get_details_header
from signal_details import get_signal_details
from signal_ta_chart_alt_orders import get_sign_ta_chart_alt_orders
from signal_recom_trail_returns import get_sign_recommend_trail_returns
from trades_tab import get_trades_box
from font_awesome import get_font_awesome
from googleanalytics import get_googleanalytics
from googleadsense import get_googleadsense
from sa_func import redirect_if_not_logged_in
from signal_returns_colchart import get_signal_return_colchart

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_uid_from_tvs(tvws):
    """ xxx """
    return_data = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT uid FROM symbol_list WHERE tradingview ='"+ str(tvws) +"' "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        return_data = row[0]
    cursor.close()
    connection.close()
    return return_data

def get_sign_header(uid, burl, terminal):
    """ xxx """
    return_data = ''
    return_data = ' '+\
    '        <div class="col-lg-8 col-md-8 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    get_signal_details(uid, burl, 'desc', terminal) +\
    '            </div>'+\
    '        </div>'+\
    '        <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded" >'+\
    get_signal_return_colchart(uid) +\
    '            </div>'+\
    '        </div>'
    return return_data

def gen_sign_page(uid, tvws, appname, burl, terminal):
    """ xxx """
    return_data = ''
    if tvws is not None:
        uid = get_uid_from_tvs(tvws)
    if uid is None:
        uid = 0
    if uid == '':
        uid = 0

    if uid != 0:
        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)

        sql = "SELECT instruments.fullname FROM symbol_list "+\
        "JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
        "WHERE symbol_list.uid = " +\
        str(uid)

        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            instfullname = row[0]

        page_title = 'This is how we decide to trade ' + instfullname

        page_desc = 'Access to thousands of financial instruments, '+\
        'stocks, forex, commodities & cryptos analysis and recommendations.'

        return_data = get_head(get_loading_head() +\
                               get_googleanalytics() +\
                               get_googleadsense() +\
                               get_title(appname +' - ' + instfullname) +\
                               get_metatags(burl) +\
                               redirect_if_not_logged_in(burl, '') +\
                               set_ogp(burl, 2, page_title, page_desc) +\
                               get_bootstrap(get_sa_theme(), burl) +\
                               get_font_awesome() +\
                               get_google_chart_script() +\
                               get_stylesheet(burl))
        return_data = return_data + get_body(get_loading_body(), navbar(burl, 0, terminal) +\
                                             '<div class="box-top"><div class="row">' +\
                                             get_details_header(uid, burl) +\
                                             get_sign_header(uid, burl, terminal) +\
                                             get_sign_ta_chart_alt_orders(uid) +\
                                             get_sign_recommend_trail_returns(uid) +\
                                             get_trades_box(uid, burl, None) +\
                                             '</div></div>' +\
                                             get_page_footer(burl, False))
        return_data = set_page(return_data)

        cursor.close()
        connection.close()
    else: return_data = set_page(get_head('<meta http-equiv="refresh" content="0;URL=' +\
                                          str(burl) + 'error" />') + get_body('', ''))
    return return_data
