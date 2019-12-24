""" App widget functionalities """
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
from app_stylesheet import get_stylesheet
from app_cookie import get_sa_theme
from sa_func import redirect_if_not_logged_in
#-------------------------------------------------------------------------------
# Insert here module of the widget to load
#-------------------------------------------------------------------------------
from tradingview_chart import get_tradingview_chart
from tradingview_ecocal import get_tradingview_ecocal
from tradingview_fxcross import get_tradingview_fxcross
from tradingview_fxheatmap import get_tradingview_fxheatmap
from tradingview_screener import get_tradingview_screener
from tradingview_watchlist import get_tradingview_watchlist
from trades_tab import get_trades_box
from news_feed import get_newsfeed
#-------------------------------------------------------------------------------

def get_widget_content(burl, nonavbar, funcname, noflexheight):
    """ xxx """
    box_content = ''
    box_class = 'box'

    box_vh = 'height:100vh;width:100vw;margin-left:-15px;'+\
    'overflow-x:hidden;overflow-y:hidden;'

    if nonavbar is None:
        box_class = 'box-top'
        box_vh = 'height:89vh;'
    if noflexheight is not None:
        box_vh = ''

    box_content = ' '+\
    '<div class="'+ box_class +'"></div>' +\
    '        <div style="'+ box_vh +'">'+\
    eval(funcname)+\
    '        </div>'
    return box_content


def get_widget_page(appname,
                    burl,
                    nonavbar,
                    funcname,
                    refresh_in_second,
                    noflexheight,
                    terminal):
    """ xxx """
    return_data = ''
    navbarcontent = ''
    metarefresh = ''
    if nonavbar is None:
        navbarcontent = navbar(burl, 0, terminal)
    if refresh_in_second is not None:
        metarefresh = '<meta http-equiv="refresh" content="'+ str(refresh_in_second) +'">'

    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           metarefresh +\
                           get_metatags(burl, terminal) +\
                           redirect_if_not_logged_in(burl, '') +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))

    return_data = return_data + get_body(get_loading_body(), navbarcontent +\
                                         get_widget_content(burl,
                                                            nonavbar,
                                                            funcname,
                                                            noflexheight))
    return_data = set_page(return_data)
    return return_data
