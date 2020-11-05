""" A template page """
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_loading import get_loading_head, get_loading_body
from app_footer import get_page_footer
from app_ogp import set_ogp
from app_title import get_title
from app_metatags import get_metatags
from bootstrap import get_bootstrap
from font_awesome import get_font_awesome
from app_navbar import navbar
from googleanalytics import get_googleanalytics
from google_chart import get_google_chart_script
from app_stylesheet import get_stylesheet
from app_cookie import theme_return_this, get_sa_theme
from sa_func import redirect_if_not_logged_in
from details_header import get_details_header
from signal_main import get_sign_header
from tradingview_profile import get_tradingview_profile
from tradingview_chartoverview import get_tradingview_chartoverview
from signal_recom_trail_returns import get_chart_box

def get_tab_component(uid, burl):
    """ Get the tab component """

    tab_1_label = '[DES] Tearsheet'
    tab_1_link = burl + 's/?uid=' + str(uid)
    tab_2_label = '[FA] Financials'
    tab_2_link = '#financials'
    tab_3_label = '[PF] Profile'
    tab_3_link = '#profile'
    tab_4_label = '[AX] Analytics'
    tab_4_link = '#analytics'

    tab_component = '' +\
    '<ul id="sa-tab-sm" class="nav nav-tabs" role="tablist">'+\
    '   <li class="nav-item">'+\
    '      <a class="nav-link" href="'+\
    tab_1_link +'">'+ tab_1_label +'</a>'+\
    '   </li>'+\
    '   <li class="nav-item">'+\
    '      <a class="nav-link active" href="'+\
    tab_2_link +'">'+ tab_2_label +'</a>'+\
    '   </li>'+\
    '   <li class="nav-item">'+\
    '      <a class="nav-link" href="'+\
    tab_3_link +'">'+ tab_3_label +'</a>'+\
    '   </li>'+\
    '   <li class="nav-item">'+\
    '      <a class="nav-link" href="'+\
    tab_4_link +'">'+ tab_4_label +'</a>'+\
    '   </li>'+\
    '</ul>'

    return tab_component

def get_profile_content(uid, burl, terminal):
    """ Content of the page """

    box_content = ''+\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    get_details_header(uid, burl)+\
    get_sign_header(uid, burl, terminal)+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content">'+\
    get_tab_component(uid, burl)+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    """ Content start here """
    """"""""""""""""""""""""""
    box_content = box_content +\
   '<div class="box">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    'height: 400px; '+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    get_tradingview_profile(uid)+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '   <div class="row">'+\
    '        <div class="col-lg-6 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    'height: 350px; '+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    get_tradingview_chartoverview(uid)+\
    '            </div>'+\
    '        </div>'+\
    get_chart_box(uid)+\
    '   </div>'+\
    '</div>'

    return box_content


def get_profile_page(appname, uid, burl, terminal):
    """ Return the content of the entire page """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           redirect_if_not_logged_in(burl, '') +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_google_chart_script() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_profile_content(uid, burl, terminal) +\
             get_page_footer(burl, False),'')
    return_data = set_page(return_data)
    return return_data
