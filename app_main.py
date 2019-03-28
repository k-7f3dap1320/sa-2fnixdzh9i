# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_head import *
from app_ogp import *
from app_footer import *
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
from card import *
from trades_tab import *
from signinbox import *
from user_profile_header import *
from font_awesome import *
from googleanalytics import *
from googleadsense import *
from list_instr_n_portf import *
from control_center import *

def gen_main_page(x,appname,burl,is_dashboard):

    dashboard_content = ''
    if is_dashboard == str(1):
        dashboard_content = get_box_list_instr_n_portf(burl,'dashboard','portf',0,0,500,None)
        dashboard_content = dashboard_content + '<div class="row">' + get_trades_box(0,burl,is_dashboard) + get_control_center(burl) + '</div>'

    r = get_head( get_loading_head() + get_googleanalytics() + get_googleadsense() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_google_chart_script() + get_stylesheet(burl) )
    r = r + get_body( get_loading_body(), navbar(burl) + get_signin_box(burl) + get_box_user_profile_header(burl) + dashboard_content + get_card(x,9,burl) + get_card(x,1,burl) + get_page_footer(burl) )
    r = set_page(r)

    return r
