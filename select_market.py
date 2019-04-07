# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_head import *
from app_ogp import *
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
from googleanalytics import *

from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def save_selectmarket(burl,mode,x):
    r = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + 'p/?ins=1&step=1" />') + get_body('','') )
    try:
        user_id = user_get_uid()
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "UPDATE users SET default_profile='"+ str(x) +"' WHERE uid='" + str(user_id) +"'"
        cr.execute(sql)
        connection.commit()
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_market_list(burl,mode):

    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT asset_class_id, asset_class_name FROM asset_class ORDER BY asset_class_id"
        cr.execute(sql)
        rs = cr.fetchall()
        label = 'x'
        r = '<div class="list-group">'
        for row in rs:
            asset_class_id = row[0]; asset_class_name = row[1]
            label = asset_class_name
            #handle particularities
            if asset_class_id == 'EQ:': label = 'All stocks'
            if asset_class_id == 'MA:': label = '<strong>I don`t know, choose for me...</strong>'; asset_class_id = ''
            if asset_class_id == 'BD:': label = 'x'
            if asset_class_id == 'CO:': label = 'x'
            if asset_class_id == 'PF:': label = 'x'
            if not label == 'x': r = r + ' <a href="'+ burl +'genportf/?acm='+ asset_class_id +'&step=1" class="list-group-item list-group-item-action">'+ label +'</a>'

        sql = "SELECT market_id, market_label FROM markets order by market_label"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            market_id = row[0]; market_label = row[1]
            label = market_label + ' Market'
            #Handle particularities
            if market_id == 'GO>': label = 'x'
            if not label == 'x': r = r + ' <a href="'+ burl +'genportf/?acm='+ market_id +'&step=1" class="list-group-item list-group-item-action">'+ label +'</a>'

        r = r + '</div>'


        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r

def get_selectmarket_box(burl,mode):

    box_content = ''

    try:
        if mode == 'portf':
            l_desc_part_1 = "Select a market for your portfolio"
            l_desc_part_2 = "Pick from the list below..."
        else:
            l_desc_part_1 = "What do you most frequently trade?"
            l_desc_part_2 = "Pick a Market from the list below..."

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content">'+\
        '                   <div class="alert alert-success" role="alert">' +\
        '                       <h5><i class="fas fa-chart-line"></i>&nbsp;'+ l_desc_part_1 +'</h5>'+ l_desc_part_2 +\
        '                   </div><div>&nbsp;</div>'+\
        get_market_list(burl,mode) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content


def gen_selectmarket_page(appname,burl,mode):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_selectmarket_box(burl,mode) )
        r = set_page(r)
    except Exception as e: print(e)
    return r
