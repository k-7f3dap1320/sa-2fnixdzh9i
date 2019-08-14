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
from app_stylesheet import *

def get_intel_content(burl):

    box_content = ''

    try:

        box_content = ''+\
        '<div class="box-top">' +\
        '<div class="row">' +\
        '    <div class="col-xs-12"><div class="box-part rounded sa-center-content"></div></div>'+\
        '    <div class="col-sm-6 col-md-3"><div class="box-part rounded sa-center-content"></div></div>'+\
        '    <div class="col-sm-6 col-md-3"><div class="box-part rounded sa-center-content"></div></div>'+\
        '    <div class="col-md-6"><div class="box-part rounded sa-center-content"></div></div>'+\
        '    <div class="col-xs-12"><div class="box-part rounded sa-center-content"></div></div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def get_intel_page(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_intel_content(burl) + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
