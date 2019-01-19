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


def get_selectportf_box(burl,step):

    box_content = ''
    min_sel = '5'
    try:
        l_desc_part_1 = "Let's Create a portfolio (Step "+ str(step) +" of "+ str(min_sel) +")"
        l_desc_part_2 = "Search and pick an item from the grid below"
        l_placeholder = "Type to search for an instrument..."
        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-center-content">'+\
        '                   <div class="alert alert-success" role="alert">' +\
        '                       <h5><i class="fas fa-list-ol"></i>&nbsp;'+ l_desc_part_1 +'</h5>'+ l_desc_part_2 +\
        '                   </div><div>&nbsp;</div>'+\
        '                    <form method="POST" action="'+ burl +'/p" style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
        '                               <div class="form-group">'+\
        '                                   <div class="input-group mb-2 mr-sm-2 mb-sm-0">'+\
        '                                       <div class="input-group-addon" style="width: 2.6rem"><i class="fas fa-search" style="font-size: xx-large;"></i></div>'+\
        '                                       <input type="text" name="search" class="form-control btn-outline-info" id="search" placeholder="'+ l_placeholder +'" required autofocus>'+\
        '                                   </div>'+\
        '                               </div>'+\
        '                   </form>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content


def gen_selectportf_page(appname,burl,step):
    r = ''
    try:
        r = get_head( get_loading_head() + get_title( appname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_selectportf_box(burl,step) )
        r = set_page(r)
    except Exception as e: print(e)
    return r
