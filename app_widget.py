
from app_head import *
from app_body import *
from app_page import *
from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *
from app_metatags import *
from bootstrap import *
from font_awesome import *
from app_navbar import *
from googleanalytics import *
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

def get_widget_content(burl,nonavbar,funcname,noflexheight):
    box_content = ''
    box_class = 'box'
    box_vh = 'height:100vh;width:100vw;margin-left:-15px;'
    if nonavbar is None:
        box_class ='box-top'
        box_vh = 'height:89vh;'
    if noflexheight is not None: box_vh = ''

    box_content = ' '+\
    '<div class="'+ box_class +'"></div>' +\
    '        <div style="'+ box_vh +'">'+\
    eval(funcname)+\
    '        </div>'
    return box_content


def get_widget_page(appname,burl,nonavbar,funcname,refresh_in_second,noflexheight):
    return_data = ''
    navbarcontent = ''
    metarefresh = ''
    if nonavbar is None: navbarcontent = navbar(burl,0)
    if refresh_in_second is not None:
        metarefresh = '<meta http-equiv="refresh" content="'+ str(refresh_in_second) +'">'
    return_data = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + metarefresh + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_font_awesome() + get_stylesheet(burl) )
    return_data = return_data + get_body( get_loading_body(), navbarcontent + get_widget_content(burl,nonavbar,funcname,noflexheight)  )
    return_data = set_page(return_data)
    return return_data
