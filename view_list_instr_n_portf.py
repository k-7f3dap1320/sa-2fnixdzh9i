# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import Flask, make_response, request, redirect
from app_page import *
from app_head import *
from app_ogp import *
from app_metatags import *
from app_title import *
from app_body import *
from app_footer import *
from bootstrap import *
from app_loading import *
from app_stylesheet import *
from awesomplete import *
from tablesorter import *
from app_navbar import *
from font_awesome import *
from app_cookie import *
from sa_func import *
from googleanalytics import *
from googleadsense import *
from list_instr_n_portf import *
from print_google_ads import *


def get_top_instr_n_portf_list():

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content">'+\
        print_google_ads('leaderboard','center') +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def gen_view_list_instr_n_portf(appname,burl,what,x,nonavbar):
    #what = 'instr', what = 'portf'
    #x = market or asset class
    r = ''
    try:

        navbarcontent = ''
        footercontent = ''
        if nonavbar is None:
            navbarcontent = navbar(burl,0)
            footercontent = get_page_footer(burl)

        if what == 'instr':
            numrow = 5000
        else:
            numrow = 200
        page_title = 'Top Performing Trades of the Week'
        page_desc = 'Access to thousands of financial instruments, stocks, forex, commodities & cryptos. Create your trading signals portfolio powered by Artificial intelligence.'
        r = get_head( get_loading_head() + get_googleanalytics() + get_googleadsense() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,2,page_title,page_desc) + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbarcontent + get_top_instr_n_portf_list() + get_box_list_instr_n_portf(burl,'view',what,1,None,numrow,x) + footercontent )
        r = set_page(r)
    except Exception as e: print(e)
    return r
