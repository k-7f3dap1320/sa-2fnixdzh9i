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
from portf_save import *
import datetime
import time
from datetime import timedelta

from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def get_selectportf_box(burl,step,mode,x):

    box_content = ''
    min_sel = '5'
    try:
        portf_category = ''
        progress_value = '0'
        try:
            if x is None: x = get_user_default_profile()
        except Exception as e: print(e)

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT asset_class_name FROM asset_class WHERE asset_class_id ='"+ str(x) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: portf_category = row[0]

        if portf_category == '':
            sql = "SELECT market_label FROM markets WHERE market_id='"+ str(x) +"'"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: portf_category = row[0] + ' Equity'
        cr.close()
        connection.close()

        if not portf_category == '': portf_category = portf_category + ' '

        if step == '1':
            l_desc_part_1 = "Let's Create your "+ str(portf_category)  +"portfolio (Step "+ str(step) +" of "+ str(min_sel) +")"
            progress_value = '20'
            l_desc_part_2 = "Find and pick an item from the list below"
        if step == '2':
            l_desc_part_1 = "Pick another item to add to your "+ str(portf_category) +"portfolio (Step "+ str(step) +" of "+ str(min_sel) +")"
            progress_value = '40'
            l_desc_part_2 = "Find and pick an item from the list below"
        if step == '3':
            l_desc_part_1 = "Almost there, pick another one (Step "+ str(step) +" of "+ str(min_sel) +")"
            progress_value = '60'
            l_desc_part_2 = "Find and pick an item from the list below"
        if step == '4':
            l_desc_part_1 = "You selected 3 items for your portfolio, choose another one, we need 5 of them (Step "+ str(step) +" of "+ str(min_sel) +")"
            progress_value = '80'
            l_desc_part_2 = "Find and pick an item from the list below"
        if step == '5':
            l_desc_part_1 = "One more and your are done :) (Step "+ str(step) +" of "+ str(min_sel) +")"
            progress_value = '95'
            l_desc_part_2 = "Find and pick an item from the list below"
        if step == '6':
            l_desc_part_1 = "Save portfolio"
            progress_value = '100'
            l_desc_part_2 = ""

        l_back_button = 'back'
        l_skip_process_button = 'Skip this process'

        button_back = '<button type="button" style="font-size: medium;" class="btn btn-lg btn-success" onClick="javascript:history.back();">'+ l_back_button +'</button>'
        button_process_skip = '<a href="'+ burl +'" style="font-size: medium;" class="btn btn-lg btn-primary">'+ l_skip_process_button +'</a>'

        portf_selection = '<h5>'
        for i in range(5):
            select_instr = get_portf_select(i+1)
            if not select_instr == '':
                portf_selection = portf_selection + '<span class="badge badge-info"><i class="fas fa-chart-pie">&nbsp;</i>'+ select_instr +'</span>&nbsp;&nbsp;'
        portf_selection = portf_selection + '</h5>'

        try:
            if int(step) > 1 and int(step) < 6:
                portf_selection = 'your portfolio selection: ' + portf_selection
            else:
                portf_selection = ''
        except:
            pass

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-center-content rounded">'+\
        '                   <div class="alert alert-success" role="alert">' +\
        '                       <h5><i class="fas fa-list-ol"></i>&nbsp;'+ l_desc_part_1 +'</h5>'+ button_back + '&nbsp;&nbsp;' + l_desc_part_2 + '&nbsp;&nbsp;' + button_process_skip +\
        '                          <div>&nbsp;</div> '+\
        '                          <div class="progress">'+\
        '                               <div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width: '+ str(progress_value) +'%" aria-valuenow="'+ str(progress_value) +'" aria-valuemin="0" aria-valuemax="100"></div>'+\
        '                          </div>'+\
        '                   </div>'+\
        portf_selection +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content

def save_portf_select(appname,burl,step,mode,x,portf,uid):
    r = ''
    try:
        next_step = int(step) +1
        if int(step) < 5:
            resp = make_response( redirect(burl+'p/?ins=1&step='+ str(next_step) ) )
            resp.set_cookie('portf_s_'+str(step), str(uid), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
        else:
            resp = make_response( redirect(burl+'p/?ins=3' ) )
            resp.set_cookie('portf_s_'+str(step), str(uid), expires=datetime.datetime.now() + datetime.timedelta(days=1) )

    except Exception as e:
        print(e)
    return resp

def get_portf_select(select):
    r = ''
    try:
        uid = request.cookies.get('portf_s_' + str(select) )

        if not uid is None or uid == '':
            connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT instruments.fullname FROM instruments JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "WHERE symbol_list.uid=" + str(uid)
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: r = row[0]
            cr.close()

    except Exception as e:
        print(e)
    return r


def ini_portf_select(r):
    try:
        resp = make_response(r)
        conviction = 'neutral'
        for i in range(5):

            if get_random_num(3) == 1: conviction = 'neutral'
            if get_random_num(3) == 2: conviction = 'weak'
            if get_random_num(3) == 3: conviction = 'strong'

            resp.set_cookie('portf_s_' + str(i+1),'0',expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            resp.set_cookie('portf_s_' + str(i+1) + '_type','long/short',expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            resp.set_cookie('portf_s_' + str(i+1) + '_conv',conviction,expires=datetime.datetime.now() + datetime.timedelta(days=1))

    except Exception as e:
        print(e)
    return resp

def gen_selectportf_page(appname,burl,step,mode,x,portf):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_selectportf_box(burl,step,mode,x) + get_box_list_instr_n_portf(burl,'portf_select','instr',step,portf,1000,x) )
        r = set_page(r)
        if step == '1': r = ini_portf_select(r)
    except Exception as e: print(e)
    return r

def custom_save_portf_page(appname,burl,mode,x):
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_selectportf_box(burl,'6',mode,x) + get_box_portf_save(burl) )
        r = set_page(r)

    except Exception as e:
        print(e)
    return r
