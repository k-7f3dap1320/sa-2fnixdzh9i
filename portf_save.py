# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import Flask, make_response, request, redirect
from sa_db import *
from sa_func import *
from app_cookie import *
import datetime
import time
from datetime import timedelta

access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def set_portf_date():
    d = datetime.datetime.now();
    r = datetime.datetime.strptime(d, '%Y%m%d')
    return r

def set_portf_symbol():
    r = ''
    try:
        symbol = ''
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT part_three FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol = symbol + row[0]
        d = datetime.datetime.now(); frmd = datetime.datetime.strptime(d, '%d')
        symbol = symbol + frmd
        r = symbol
    except Exception as e: print(e)
    return r

def get_portf_asset_class(what):
    #what = "n" (name) ; what = "i" (id)
    r = ''
    try:
        suid = ''
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        select_asset_class_id = ''
        multi_asset_selected = False
        asset_class_name = ''
        asset_class_id = ''
        for i in range(5):
            suid = request.cookies.get('portf_s_' + str(i+1) )
            sql = "SELECT asset_class.asset_class_name, asset_class.asset_class_id FROM instruments "+\
            "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "JOIN asset_class ON instruments.asset_class = asset_class.asset_class_id "+\
            "WHERE symbol_list.uid = "+ str(suid)
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: asset_class_name = row[0]; asset_class_id = row[1]
            if i == 0:
                select_asset_class_id = asset_class_id
            else:
                if select_asset_class_id != asset_class_id: multi_asset_selected = True
        cr.close()
        connection.close()

        if multi_asset_selected:
            if what == 'n': r = 'Multi-asset'
            if what == 'i': r = 'MA:'
        else:
            if what == 'n': r = asset_class_name
            if what == 'i': r = asset_class_id
    except Exception as e: print(e)
    return r

def get_portf_market(what):
    #what = "n" (name) ; what = "i" (id)
    r = ''
    try:
        suid = ''
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        select_market_id = ''
        market_label = ''
        market_id = ''
        for i in range(5):
            suid = request.cookies.get('portf_s_' + str(i+1) )
            sql = "SELECT symbol_list.uid, markets.market_id, markets.market_label FROM instruments "+\
            "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "JOIN markets ON instruments.market = markets.market_id "+\
            "WHERE symbol_list.uid = " + str(suid)
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: market_id = row[0]; market_label = row[1]
        cr.close()
        connection.close()

        if what == 'n': r = market_label
        if what == 'i': r = market_id
    except Exception as e: print(e)
    return r

def set_portf_fullname(s,ac,m,st):
    #portf: symbol, asset_class_name, market_label, strategy_type
    r = ''
    try:
        fullname = portf_symbol.replace(get_portf_suffix(),'')
        r = fullname + ' ' + m + ' ' + ac + ' ' + st
    except Exception as e: print(e)
    return r

def get_portf_strategy_type():
    r = ''
    try:
        strategy_type = ''
        selected_type = ''
        is_long_short = False
        for i in range(5):
            strategy_type = request.cookies.get('portf_s_' + str(i+1) )
            if i == 0: selected_type = strategy_type
            if strategy_type == 'long/short': selected_type = 'long/short'
            if strategy_type != selected_type: selected_type = 'long/short'

        if selected_type == 'short': r = 'ultra short'
        if selected_type == 'long/short': r = selected_type
    except Exception as e: print(e)
    return r

def portf_save_generate():
    try:
        portf_symbol = get_portf_suffix() + set_portf_symbol()
        portf_asset_class_id = get_portf_asset_class('i')
        portf_asset_class_name = get_portf_asset_class('n')
        portf_market_id = get_portf_market('i')
        portf_market_name = get_portf_market('n')
        portf_strategy_type = get_portf_strategy_type()
        portf_fullname = set_portf_fullname(portf_symbol,portf_asset_class_name,portf_market_name,portf_strategy_type)
        portf_owner = user_get_uid()
        portf_description = ''
        portf_account_reference = 1000
        portf_decimal_place = 0
        portf_pip = 1
        portf_sector = 0
        portf_unit = 'pts'
        portf_creation_date = set_portf_date()
        portf_default_alloc_quantity = 1

    except Exception as e: print(e)

def portf_save_conviction(burl,mode,x):
    #mode = "type1", "type2", "type3", "conv1", "conv2"...
    #x = "long/short", "long", "short", "neutral", "weak", "strong"
    try:
            resp = make_response( redirect(burl+'p/?ins=3') )
            if mode == "type1": resp.set_cookie('portf_s_1_type', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            if mode == "type2": resp.set_cookie('portf_s_2_type', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            if mode == "type3": resp.set_cookie('portf_s_3_type', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            if mode == "type4": resp.set_cookie('portf_s_4_type', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            if mode == "type5": resp.set_cookie('portf_s_5_type', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )

            if mode == "conv1": resp.set_cookie('portf_s_1_conv', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            if mode == "conv2": resp.set_cookie('portf_s_2_conv', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            if mode == "conv3": resp.set_cookie('portf_s_3_conv', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            if mode == "conv4": resp.set_cookie('portf_s_4_conv', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )
            if mode == "conv5": resp.set_cookie('portf_s_5_conv', str(x), expires=datetime.datetime.now() + datetime.timedelta(days=1) )


    except Exception as e:
        print(e)
    return resp

def get_portf_table_rows(burl):
    r = ''
    try:
        for i in range(5):

            strategy_order_type = request.cookies.get('portf_s_' + str(i+1) + '_type' )
            strategy_conviction = request.cookies.get('portf_s_' + str(i+1) + '_conv' )
            instr_selection = ''
            uid = request.cookies.get('portf_s_' + str(i+1) )

            if not uid is None or uid == '':
                connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
                cr = connection.cursor(pymysql.cursors.SSCursor)
                sql = "SELECT instruments.fullname, instruments.symbol FROM instruments JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
                "WHERE symbol_list.uid=" + str(uid)
                cr.execute(sql)
                rs = cr.fetchall()
                for row in rs: instr_selection = '<strong>' + row[0] + '</strong>&nbsp;('+ row[1] +')'
                cr.close()

            if strategy_order_type == 'long/short': class_order_type = 'btn-secondary'
            if strategy_order_type == 'long': class_order_type = 'btn-success'
            if strategy_order_type == 'short': class_order_type = 'btn-danger'


            r = r + ''+\
            '    <tr>'+\
            '      <th scope="row">'+\
            '       <div class="dropdown">'+\
            '           <button class="btn '+ class_order_type +' dropdown-toggle" type="button" id="strategy_order_type_'+ str(i+1) +'" name="strategy_order_type_'+ str(i+1) +'" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+\
            strategy_order_type +\
            '           </button>'+\
            '           <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'+\
            '               <a class="dropdown-item" href="'+ burl + 'p/?ins=4&mode=type'+str(i+1)+'&x=long/short'+'">Buy and Sell (long/short)</a>'+\
            '               <a class="dropdown-item" href="'+ burl + 'p/?ins=4&mode=type'+str(i+1)+'&x=long'+'">Buy Only (long)</a>'+\
            '               <a class="dropdown-item" href="'+ burl + 'p/?ins=4&mode=type'+str(i+1)+'&x=short'+'">Sell Only (short)</a>'+\
            '           </div>'+\
            '       </div>'+\
            '       </th>'+\
            '       <td>'+\
            '       <div class="dropdown">'+\
            '           <button class="btn btn-secondary dropdown-toggle" type="button" id="strategy_conviction_'+ str(i+1) +'" name="strategy_conviction_'+ str(i+1) +'" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+\
            strategy_conviction +\
            '           </button>'+\
            '           <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'+\
            '               <a class="dropdown-item" href="'+ burl + 'p/?ins=4&mode=conv'+str(i+1)+'&x=weak'+'">weak</a>'+\
            '               <a class="dropdown-item" href="'+ burl + 'p/?ins=4&mode=conv'+str(i+1)+'&x=strong'+'">strong</a>'+\
            '               <a class="dropdown-item" href="'+ burl + 'p/?ins=4&mode=conv'+str(i+1)+'&x=neutral'+'">neutral</a>'+\
            '           </div>'+\
            '       </div>'+\
            '      </td>'+\
            '      <td width="100%">'+ instr_selection +'</td>'+\
            '    </tr>'
    except Exception as e:
        print(e)
    return r

def get_list_portf_alloc(burl):
    r = ''
    try:
        l_conviction = 'What is your conviction?'
        l_buttonSave = 'Save and generate portfolio'
        r = '' +\
        '<table class="table table-hover">'+\
        '  <thead>'+\
        '    <tr>'+\
        '      <th scope="col" colspan="3">'+ l_conviction +'</th>'+\
        '    </tr>'+\
        '  </thead>'+\
        '  <tbody>'+\
        get_portf_table_rows(burl) +\
        '  </tbody>'+\
        '</table>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<form method="GET" action="'+ burl +'p/">'+\
        '   <input type="hidden" id="ins" name="ins" value="5">'+\
        '   <button type="submit" class="btn btn-info btn-lg form-signin-btn"><i class="fas fa-save"></i>&nbsp;'+ l_buttonSave +'</button>'+\
        '</form>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'+\
        '<span>&nbsp;</span>'
    except Exception as e:
        print(e)
    return r

def get_box_portf_save(burl):

    box_content = ''

    try:

        box_content = '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-center-content sa-instr-n-portf-list">'+\
        get_list_portf_alloc(burl)+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


        #cr.close()
        #connection.close()

    except Exception as e: print(e)

    return box_content
