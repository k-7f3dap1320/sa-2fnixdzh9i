""" App main page """
from app_page import set_page
from app_head import get_head
from app_ogp import set_ogp
from app_cookie import user_is_login, get_sa_theme
from app_footer import get_page_footer
from app_metatags import get_metatags
from app_title import get_title
from app_body import get_body
from bootstrap import get_bootstrap
from google_chart import get_google_chart_script
from app_loading import get_loading_head, get_loading_body
from app_stylesheet import get_stylesheet
from app_navbar import navbar
from card import get_card
from trades_tab import get_trades_box
from signinbox import get_signin_box
from user_profile_header import get_box_user_profile_header
from font_awesome import get_font_awesome
from googleanalytics import get_googleanalytics
from googleadsense import get_googleadsense
from list_instr_n_portf import get_box_list_instr_n_portf
from user_control_center_aggregate_perf import get_control_center_aggregate_perf
from app_popup_modal import gen_tour_popup
from purechat import get_purechat
from news_feed import get_newsfeed
from print_google_ads import print_google_ads

def get_dashboard(burl, is_dashboard):
    ret = ''
    dashboard_content = get_box_list_instr_n_portf(burl, 'dashboard', 'portf', 0, 500, None)
    dashboard_content = dashboard_content +\
    '<div class="box">'+\
    '<div class="row">'+\
    get_control_center_aggregate_perf() +\
    '</div>'+\
    '<div class="row">' +\
    get_trades_box(0, burl, is_dashboard) +\
    '</div>'+\
    '</div>'
    ret = dashboard_content
    return ret

def get_feed(burl, terminal, selection):
    feed_content = ''
    google_ad = ''
    if user_is_login() == 1:
        google_ad = print_google_ads('leaderboard', 'center')

    if user_is_login() == 0:
        feed_content = feed_content +\
        get_newsfeed(burl, 0, 0, 10, 1, terminal) + '<br />'+ get_newsfeed(burl, 1, 0, 5, 1, terminal) + '<br />'
        feed_content = feed_content + get_card(selection, 9, burl, terminal)
    if user_is_login() == 1:
        feed_content = feed_content + get_newsfeed(burl, 0, 0, 15, 1, terminal) + '<br />'
        feed_content = feed_content + google_ad
    if user_is_login() == 1:
        feed_content = feed_content + get_newsfeed(burl, 1, 0, 5, 1, terminal) + '<br />'
    feed_content = feed_content + get_card(selection, 1, burl, terminal)
    if user_is_login() == 1:
        feed_content = feed_content + get_newsfeed(burl, 2, 0, 100, 1, terminal) + '<br />'
        
    return feed_content

def gen_main_page(selection,
                  appname,
                  burl,
                  is_dashboard,
                  tour,
                  nonavbar,
                  terminal):
    """ xxx """
    metarefresh = ''
    refresh_in_second = 900
    navbarcontent = ''
    if nonavbar is None:
        navbarcontent = navbar(burl, 0, terminal)
    page_content = ''
    if is_dashboard == str(1) and user_is_login() == 1:
        page_content = get_dashboard(burl, is_dashboard)
    else:
        get_feed(burl, terminal, selection)
        if user_is_login() == 1:
            metarefresh = '<meta http-equiv="refresh" content="'+ str(refresh_in_second) +'">'

        
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_googleadsense() +\
                           get_title(appname) +\
                           metarefresh+get_metatags(burl) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_google_chart_script() +\
                           get_stylesheet(burl))
    return_data = return_data + get_body(get_loading_body(), navbarcontent +\
                                         gen_tour_popup(tour, burl) +\
                                         get_signin_box(burl) +\
                                         get_box_user_profile_header() +\
                                         page_content + get_page_footer(burl) +\
                                         get_purechat(0))
    return_data = set_page(return_data)
    return return_data
