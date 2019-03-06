# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from trail_returns_chart import *
from sa_func import *


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_risk_table(uid):

    t = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.fullname, instruments.asset_class, instruments.market, is_benchmark, "+\
        "instruments.beta_st, instruments.alpha_st, instruments.stdev_st, instruments.sharpe_ratio_st, "+\
        "instruments.maximum_dd_st, instruments.romad_st, instruments.volatility_risk_st "+\
        "FROM smartalpha.instruments JOIN smartalpha.symbol_list "+\
        "ON instruments.symbol = symbol_list.symbol "+\
        "WHERE symbol_list.uid =" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        a_fullname=''; a_asset_class=''; a_market=''; a_is_benchmark=0
        a_beta_st=''; a_alpha_st=''; a_stdev_st=''; a_sharpe_ratio_st=''; a_maximum_dd_st=''; a_romad_st=''; a_volatility_risk_st=''
        for row in rs:
            a_fullname = row[0]
            a_asset_class = row[1]
            a_market = row[2]
            a_is_benchmark = row[3]
            a_beta_st = str( row[4] )
            a_alpha_st = str( row[5] )
            a_stdev_st = str( round(row[6],2) )
            a_sharpe_ratio_st = str( row[7] )
            a_maximum_dd_st = str( round( row[8]*100,2) ) +'%'
            a_romad_st = str( round( row[9],2 ) )
            a_volatility_risk_st = str( round( row[10]*100,2 ) ) +'%'

        sql = "SELECT instruments.fullname, instruments.asset_class, instruments.market, is_benchmark, "+\
        "instruments.beta_st, instruments.alpha_st, instruments.stdev_st, instruments.sharpe_ratio_st, "+\
        "instruments.maximum_dd_st, instruments.romad_st, instruments.volatility_risk_st "+\
        "FROM smartalpha.instruments JOIN smartalpha.symbol_list "+\
        "ON instruments.symbol = symbol_list.symbol "+\
        "WHERE instruments.asset_class='"+ a_asset_class +"' AND instruments.market='"+ a_market +"' AND is_benchmark=1 "
        cr.execute(sql)
        rs = cr.fetchall()
        b_fullname=''; b_asset_class=''; b_market=''; b_is_benchmark=0
        b_beta_st=''; b_alpha_st=''; b_stdev_st=''; b_sharpe_ratio_st=''; b_maximum_dd_st=''; b_romad_st=''; b_volatility_risk_st=''
        for row in rs:
            b_fullname = row[0]
            b_asset_class = row[1]
            b_market = row[2]
            b_is_benchmark = row[3]
            b_beta_st = str( row[4] )
            b_alpha_st = str( row[5] )
            b_stdev_st = str( round( row[6],2) )
            b_sharpe_ratio_st = str( row[7] )
            b_maximum_dd_st = str( round( row[8]*100,2) ) +'%'
            b_romad_st = str( round( row[9],2 ) )
            b_volatility_risk_st = str( round( row[10]*100,2 ) ) +'%'
        cr.close()
        connection.close()

        l_row_descr = 'Ratio/metric'
        l_volatility_risk_st = 'Volatility over last 30 days (%)'
        l_maximum_dd_st = 'Max drawdown over last 30 days'
        l_romad_st = 'Return over max drawdown (30 days)'
        content = '<div>&nbsp;</div>'+\
        '<table class="table table-hover table-sm sa-table-sm">'+\
        '  <thead>'+\
        '    <tr>'+\
        '      <th scope="col">'+ l_row_descr +'</th>'+\
        '      <th scope="col">'+ a_fullname +'</th>'+\
        '      <th scope="col">'+ b_fullname +'</th>'+\
        '    </tr>'+\
        ' </thead>'+\
        ' <tbody>'+\
        '    <tr>'+\
        '      <th scope="row">'+ l_volatility_risk_st  +'</th>'+\
        '      <td>'+ str(a_volatility_risk_st) +'</td>'+\
        '      <td>'+ str(b_volatility_risk_st) +'</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <th scope="row">'+ l_maximum_dd_st  +'</th>'+\
        '      <td>'+ str(a_maximum_dd_st) +'</td>'+\
        '      <td>'+ str(b_maximum_dd_st) +'</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <th scope="row">'+ l_romad_st  +'</th>'+\
        '      <td>'+ str(a_romad_st) +'</td>'+\
        '      <td>'+ str(b_romad_st) +'</td>'+\
        '    </tr>'+\
        '  </tbody>'+\
        '</table>'

        t = content

    except Exception as e: print(e)

    return t

def get_box_risk_content(uid):

    box_content = ''

    try:

        lang = get_selected_lang()

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portf_risk_consider FROM `recommendations` WHERE lang='"+ lang +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            text_content = row[0]

        sql = "SELECT instruments.account_reference, instruments.unit, "+\
        "instruments.beta_st, instruments.alpha_st, instruments.stdev_st, instruments.sharpe_ratio_st, "+\
        "instruments.maximum_dd_st, instruments.romad_st, instruments.volatility_risk_st " +\
        "FROM instruments "+\
        "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
        "WHERE symbol_list.uid=" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            account_reference = row[0]
            unit = row[1]
            beta_st = row[2]
            alpha_st = row[3]
            stdev_st = row[4]
            sharpe_ratio_st = row[5]
            maximum_dd_st = row[6]
            romad_st = row[7]
            volatility_risk_st = row[8]
        cr.close()
        connection.close()

        dollar_amount = round( stdev_st , 2)
        percentage = round( volatility_risk_st*100, 2 )

        text_content = text_content.replace('{account_reference}', str( int(account_reference) ) )
        text_content = text_content.replace('{unit}', str(unit) )
        text_content = text_content.replace('{dollar_amount}', str(dollar_amount) )
        text_content = text_content.replace('{percentage}', str(percentage) + "%" )

        l_title = 'Risk considerations'

        box_content = '' +\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-signal-recomm-trail-ret">'+\
        '               <div><h6>'+ l_title +'</h6></div>'+\
        '                   <div>'+ text_content +'</div>'+\
        '<div>'+ get_risk_table(uid) +'</div>'+\
        '            </div>'+\
        '        </div>'

    except Exception as e: print(e)

    return box_content


def get_box_trail_returns_content(uid):

    box_content = ''

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.fullname FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            fullname = row[0]

        l_title = fullname + ' portfolio trailing returns'
        box_content = '' +\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-signal-recomm-trail-ret">'+\
        '               <div><h6>'+ l_title +'</h6></div>'+\
        get_trailing_returns(uid) +\
        '            </div>'+\
        '        </div>'
        cr.close()
        connection.close()

    except Exception as e: print(e)

    return box_content

def get_portf_risk_trail_returns(uid):
    return get_box_risk_content(uid) + get_box_trail_returns_content(uid)
