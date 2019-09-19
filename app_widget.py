# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *
from app_stylesheet import *
from app_cookie import *
#-------------------------------------------------------------------------------
from tradingview_chart import *
from tradingview_ecocal import *
from tradingview_fxcross import *
from tradingview_fxheatmap import *
from trades_tab import *
from news_feed import *
#-------------------------------------------------------------------------------

def get_widget_content(burl,nonavbar,funcname):

    box_content = ''
    box_class = 'box'
    box_vh = '100vh'
    box_vw = '100vw'

    try:
        if nonavbar is None:
            box_class ='box-top'
            box_vh = '95vh'

        box_content = ' '+\
        '<div class="'+ box_class +'">' +\
        '        <div style="height: '+ box_vh +'; width: '+ box_vw +'; margin=-15px;">'+\
        eval(funcname)+\
        '        </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def get_widget_page(appname,burl,nonavbar,funcname,refresh_in_second):
    r = ''
    navbarcontent = ''
    metarefresh = ''
    try:
        if nonavbar is None: navbarcontent = navbar(burl,0)

        if refresh_in_second is not None:
            metarefresh = '<meta http-equiv="refresh" content="'+ str(refresh_in_second) +'">'

        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + metarefresh + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbarcontent + get_widget_content(burl,nonavbar,funcname)  )
        r = set_page(r)
    except Exception as e: print(e)

    return r
