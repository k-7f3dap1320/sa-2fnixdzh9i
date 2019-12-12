""" List of trading instruments and strategy portfolio """
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_ogp import set_ogp
from app_metatags import get_metatags
from app_title import get_title
from app_footer import get_page_footer
from bootstrap import get_bootstrap
from app_loading import get_loading_head, get_loading_body
from app_stylesheet import get_stylesheet
from app_navbar import navbar
from font_awesome import get_font_awesome
from app_cookie import get_sa_theme, theme_return_this
from googleanalytics import get_googleanalytics
from googleadsense import get_googleadsense
from list_instr_n_portf import get_box_list_instr_n_portf
from print_google_ads import print_google_ads
from purechat import get_purechat

def get_top_instr_n_portf_list():
    """ xxx """
    box_content = '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content">'+\
    print_google_ads('leaderboard', 'center') +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content

def gen_view_list_instr_n_portf(appname, burl, what, sel, terminal):
    """ xxx """
    #what = 'instr', what = 'portf'
    #sel = market or asset class
    return_data = ''
    if what == 'instr':
        numrow = 10000
    else:
        numrow = 200
    page_title = 'Top Performing Trades of the Week'

    page_desc = 'Access to thousands of financial instruments, '+\
    'stocks, forex, commodities & cryptos. '+\
    'Create your trading signals portfolio powered by Artificial intelligence.'

    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_googleadsense() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           set_ogp(burl, 2, page_title, page_desc) +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() + get_stylesheet(burl))
    return_data = return_data + get_body(get_loading_body(),
                                         navbar(burl, 0, terminal) +\
                                         get_top_instr_n_portf_list() +\
                                         get_box_list_instr_n_portf(burl,
                                                                    'view',
                                                                    what,
                                                                    1,
                                                                    numrow,
                                                                    sel) +\
                                         get_page_footer(burl) +\
                                         get_purechat(0))
    return_data = set_page(return_data)
    return return_data
