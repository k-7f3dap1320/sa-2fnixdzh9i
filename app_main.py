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
from app_navbar import *
from card import *
from trades_tab import *
from signinbox import *
from font_awesome import *

def gen_main_page(x,appname,burl):

    r = get_head( get_loading_head() + get_title( appname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_font_awesome() + get_google_chart_script() + get_stylesheet(burl) )
    r = r + get_body( get_loading_body(), navbar(burl) + get_signin_box(burl) + '<div class="row">' + get_trades_box(0,burl) + '</div>' + get_card(x,9) + get_card(x,1) )
    r = set_page(r)

    return r
