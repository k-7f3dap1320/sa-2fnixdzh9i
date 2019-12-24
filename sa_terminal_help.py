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
from googleanalytics import get_googleanalytics
from app_stylesheet import get_stylesheet
from app_cookie import theme_return_this, get_sa_theme
from sa_func import redirect_if_not_logged_in
from purechat import get_purechat
from app_popup_modal import open_window_as

def get_sa_terminal_help_content(burl):
    """ Content of the page """

    box_content = ''+\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '<h4>Smartalpha Help and Support</h4>'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'

    box_content = box_content +\
   '<div class="box">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    'email: <a href="mailto:info@taatu.co">info@taatu.co</a><br />'+\
    'help and learning page: <a href="'+\
    open_window_as(burl +'h/#', 1) +'">&lt;HELP&gt;&nbsp;&lt;GO&gt;</a>'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'

    return box_content


def get_sa_terminal_help_page(appname, burl, terminal):
    """ Return the content of the entire page """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl, terminal, None) +\
                           redirect_if_not_logged_in(burl, '') +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl)+\
                           get_purechat(1))
    return_data = return_data +\
    get_body(get_loading_body(),
             get_sa_terminal_help_content(burl) +\
             get_page_footer(burl, False))
    return_data = set_page(return_data)
    return return_data
