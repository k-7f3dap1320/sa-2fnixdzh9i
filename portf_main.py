""" Portfolio main module """
import pymysql.cursors
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_ogp import set_ogp
from app_footer import get_page_footer
from app_metatags import get_metatags
from app_title import get_title
from bootstrap import get_bootstrap
from google_chart import get_google_chart_script
from app_loading import get_loading_body, get_loading_head
from app_stylesheet import get_stylesheet
from app_navbar import navbar
from details_header import get_details_header
from portf_alloc import get_portf_alloc
from portf_perf_desc import get_portf_perf_desc
from portf_risk_trail_returns import get_portf_risk_trail_returns
from trades_tab import get_trades_box
from font_awesome import get_font_awesome
from googleanalytics import get_googleanalytics
from error_page import get_error_page
from sa_func import redirect_if_not_logged_in
from app_cookie import get_sa_theme
from app_popup_modal import gen_portf_popup

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def gen_portf_page(uid, appname, burl, pop, terminal):
    """ xxx """
    return_data = ''
    if uid is None:
        uid = 0
    if uid == '':
        uid = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname FROM `symbol_list` "+\
    "JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
        "WHERE symbol_list.uid = " + str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()
    instfullname = ''
    for row in res:
        instfullname = row[0]
    cursor.close()
    connection.close()

    if instfullname != '':
        return_data = get_head(get_loading_head() +\
                               get_googleanalytics() +\
                               get_title(appname +' - ' + instfullname) +\
                               get_metatags(burl) +\
                               redirect_if_not_logged_in(burl, '') +\
                               set_ogp(burl, 1, '', '') +\
                               get_bootstrap(get_sa_theme(), burl) +\
                               get_font_awesome() +\
                               get_google_chart_script() +\
                               get_stylesheet(burl))
        return_data = return_data +\
        get_body(get_loading_body(), gen_portf_popup(pop) +\
                 navbar(burl, 0, terminal) +\
                 '<div class="box-top"><div class="row">' +\
                 get_details_header(uid, burl) +\
                 get_portf_alloc(uid, burl) +\
                 get_portf_perf_desc(uid) +\
                 get_portf_risk_trail_returns(uid) +\
                 get_trades_box(uid, burl, None) +\
                 '</div></div>' +\
                 get_page_footer(burl))
        return_data = set_page(return_data)
    else:
        get_error_page(appname, burl, terminal)
    return return_data
