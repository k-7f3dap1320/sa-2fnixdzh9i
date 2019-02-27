# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_head import *
from app_metatags import *
from app_title import *
from app_body import *
from bootstrap import *
from google_chart import *
from app_loading import *
from app_stylesheet import *
from awesomplete import *
from tablesorter import *
from app_navbar import *
from details_header import *
from portf_alloc import *
from portf_perf_desc import *
from portf_popup import *
from portf_risk_trail_returns import *
from trades_tab import *
from font_awesome import *
from googleanalytics import *

from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def gen_portf_page(uid,appname,burl,pop):

    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.fullname FROM `symbol_list` JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
            "WHERE symbol_list.uid = " + str(uid)

        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            instfullname = row[0]

        r = get_head(  get_loading_head() + get_googleanalytics() + get_title( appname +' - ' + instfullname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_google_chart_script() + get_stylesheet(burl) )
        r = r + get_body(  get_loading_body(), gen_portf_popup(uid,pop) + navbar(burl) + '<div class="box-top"><div class="row">' + get_details_header(uid,burl) + get_portf_alloc(uid) + get_portf_perf_desc(uid) + get_portf_risk_trail_returns(uid) + get_trades_box(uid,burl) + '</div></div>' )
        r = set_page(r)

        cr.close()
        connection.close()
    except Exception as e: print(e)

    return r
