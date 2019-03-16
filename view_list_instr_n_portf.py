# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import Flask, make_response, request, redirect
from app_page import *
from app_head import *
from app_metatags import *
from app_title import *
from app_body import *
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
from list_instr_n_portf import *

def gen_view_list_instr_n_portf(appname,burl,what,x):
    #what = 'instr', what = 'portf'
    #x = market or asset class
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_box_list_instr_n_portf(burl,'view',what,1,None,200,x) )
        r = set_page(r)
    except Exception as e: print(e)
    return r
