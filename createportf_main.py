# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_head import *
from app_metatags import *
from app_title import *
from app_body import *
from bootstrap import *
from app_loading import *
from app_stylesheet import *
from awesomplete import *
from app_navbar import *
from font_awesome import *
from app_cookie import *

from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def get_selectportf_box(burl):

    box_content = ''

    try:
        l_desc_part_1 = "What do you most frequently trade?"
        l_desc_part_2 = "Pick a Market from the list below..."
        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-center-content">'+\
        '                   <div class="alert alert-success" role="alert">' +\
        '                       <h5><i class="fas fa-chart-line"></i>&nbsp;'+ l_desc_part_1 +'</h5>'+ l_desc_part_2 +\
        '                   </div><div>&nbsp;</div>'+\
        get_market_list(burl) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content


def gen_selectportf_page(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_title( appname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_selectportf_box(burl) )
        r = set_page(r)
    except Exception as e: print(e)
    return r
