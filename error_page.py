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
from app_cookie import *

def popup_error_msg(burl):
    r = ''
    l_error_title = '<i class="fas fa-exclamation-circle"></i>&nbsp;The page or content cannot be found.'
    l_error_descr = 'The page might not be available anymore. <div>&nbsp;</div><div><a href="'+ burl +'" class="btn btn-sm btn-info">Back to homepage</a></div>'
    l_error_class = 'alert alert-danger'

    l_class = 'alert alert-warning'

    try:

        l_title = l_error_title
        l_descr = l_error_descr
        l_class = l_error_class

        r = ''+\
        '<div class="'+ l_class +'" role="alert">' +\
        '  <strong>'+ l_title +'</strong><br>'+ l_descr +\
        '</div><div>&nbsp;</div>'

    except Exception as e: print(e)
    return r

def get_error_page_content(burl):

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded">'+\
        popup_error_msg(burl) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def get_error_page(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl,0) + get_error_page_content(burl) + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
