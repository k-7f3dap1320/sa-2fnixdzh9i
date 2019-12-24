""" app Error page """
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_loading import get_loading_head, get_loading_body
from app_footer import get_page_footer
from app_ogp import set_ogp
from app_stylesheet import get_stylesheet
from app_title import get_title
from app_metatags import get_metatags
from bootstrap import get_bootstrap
from font_awesome import get_font_awesome
from app_navbar import navbar
from googleanalytics import get_googleanalytics
from app_cookie import get_sa_theme

def popup_error_msg(burl):
    """ xxx """
    return_data = ''
    message_header = 'The function or content is not available at the moment.'
    message_content = 'Please try again later. '+\
    'For support and assistance type: <a href="' + burl + 'h/?" '+\
    'style="text-decoration: none; font-weight: bolder;">&lt;HELP&gt;&nbsp;&lt;GO&gt;</a>.'

    button_back = 'Go back'

    l_error_title = '<i class="fas fa-exclamation-circle">'+\
    '</i>&nbsp;'+ message_header

    l_error_descr = message_content + ' '+\
    '<div>&nbsp;</div><div><a href="'+\
    burl +'" class="btn btn-sm btn-info">'+ button_back +'</a></div>'

    l_error_class = 'alert alert-danger'
    l_class = 'alert alert-warning'
    l_title = l_error_title
    l_descr = l_error_descr
    l_class = l_error_class
    return_data = ''+\
    '<div class="'+ l_class +'" role="alert">' +\
    '  <strong>'+ l_title +'</strong><br>'+ l_descr +\
    '</div><div>&nbsp;</div>'
    return return_data

def get_error_page_content(burl):
    """ xxx """
    box_content = ''
    box_content = '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded">'+\
    popup_error_msg(burl) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content


def get_error_page(appname, burl, terminal):
    """ xxx """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl, terminal) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_error_page_content(burl) +\
             get_page_footer(burl, False))
    return_data = set_page(return_data)
    return return_data
