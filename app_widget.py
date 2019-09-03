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
#-------------------------------------------------------------------------------

def get_widget_content(burl,nonavbar,funcname):

    box_content = ''
    box_class = 'box'

    try:
        if nonavbar is None: box_class ='box-top'

        #eval(funcname)+\
        box_content = '<div class="'+ box_class +'">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" style="height: 100vh;">'+\
        '            <div class="box-part rounded sa-center-content" style="height: 100%">'+\
        get_tradingview_chart(1,'"100%"','"100%"')+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def get_widget_page(appname,burl,nonavbar,funcname):
    r = ''
    navbarcontent = ''
    footercontent  = ''
    try:
        if nonavbar is None:
            navbarcontent = navbar(burl,0)
            footercontent = get_page_footer(burl)


        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbarcontent + get_widget_content(burl,nonavbar,funcname) + footercontent )
        r = set_page(r)
    except Exception as e: print(e)

    return r
