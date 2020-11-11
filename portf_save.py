""" Strategy portfolio selection save function """
import datetime
import random
import pymysql.cursors
from flask import make_response, request, redirect
from sa_func import get_portf_suffix, get_nickname
from app_cookie import get_lang, user_get_uid

from portf_gen_data import generate_portfolio

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

################################################################################
def set_portf_date():
    """ xxx """
    date_now = datetime.datetime.now()
    return_data = datetime.datetime.strftime(date_now, '%Y%m%d')
    return return_data

def set_portf_symbol():
    """ xxx """
    return_data = ''
    symbol = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT part_three FROM randwords ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        symbol = symbol + row[0]
    #d = datetime.datetime.now(); frmd = datetime.datetime.strftime(d, '%d')
    symbol = symbol + str(random.randint(1, 999))
    return_data = symbol.upper()
    cursor.close()
    connection.close()
    return return_data

def get_portf_asset_class(what):
    """ xxx """
    #what = "n" (name) ; what = "i" (id)
    return_data = ''
    suid = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    select_asset_class_id = ''
    multi_asset_selected = False
    asset_class_name = ''
    asset_class_id = ''
    for i in range(5):
        suid = request.cookies.get('portf_s_' + str(i+1))
        if suid != None:
            sql = "SELECT asset_class.asset_class_name, asset_class.asset_class_id FROM instruments "+\
            "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "JOIN asset_class ON instruments.asset_class = asset_class.asset_class_id "+\
            "WHERE symbol_list.uid = "+ str(suid)
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                asset_class_name = row[0]
                asset_class_id = row[1]
            if i == 0:
                select_asset_class_id = asset_class_id
            else:
                if select_asset_class_id != asset_class_id:
                    multi_asset_selected = True
    cursor.close()
    connection.close()

    if multi_asset_selected:
        if what == 'n':
            return_data = 'Multi-asset'
        if what == 'i':
            return_data = 'MA:'
    else:
        if what == 'n':
            return_data = asset_class_name
        if what == 'i':
            return_data = asset_class_id
    return return_data

def get_portf_market(what):
    """ xxx """
    #what = "n" (name) ; what = "i" (id); what = "cur" (currency); what = "conv" (conversion rate)
    return_data = ''
    suid = ''
    market_id = 0
    market_label = ''
    currency_code = ''
    conv_to_usd = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    market_label = ''
    market_id = ''
    for i in range(5):
        suid = request.cookies.get('portf_s_' + str(i+1))
        if suid != None:
            sql = "SELECT markets.market_id, markets.market_label, "+\
            "markets.currency_code, markets.conv_to_usd FROM instruments "+\
            "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "JOIN markets ON instruments.market = markets.market_id "+\
            "WHERE symbol_list.uid = " +\
            str(suid)
    
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                market_id = row[0]
                market_label = row[1]
                currency_code = row[2]
                conv_to_usd = row[3]
    cursor.close()
    connection.close()

    if what == 'n':
        return_data = market_label
    if what == 'i':
        return_data = market_id
    if what == 'cur':
        return_data = currency_code
    if what == 'conv':
        return_data = conv_to_usd
    return return_data

def set_portf_fullname(symbol, asset_class, market, strategy_type):
    """ xxx """
    #portf: symbol, asset_class_name, market_label, strategy_type
    return_data = ''
    fullname = symbol.replace(get_portf_suffix(), '')
    return_data = fullname + ' ' + market + ' ' + asset_class + ' ' + strategy_type
    return return_data

def get_portf_strategy_type():
    """ xxx """
    return_data = ''
    strategy_type = ''
    selected_type = ''
    for i in range(5):
        strategy_type = request.cookies.get('portf_s_' + str(i+1) + '_type')
        if i == 0:
            selected_type = strategy_type
        if strategy_type == 'long/short':
            selected_type = 'long/short'
        if strategy_type != selected_type:
            selected_type = 'long/short'

    if selected_type == 'short':
        return_data = 'ultra short'
    if selected_type == 'long/short':
        return_data = selected_type
    return return_data

def get_portf_description(asset_class, market, strategy_type):
    """ xxx """
    return_data = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT portf_description FROM labels WHERE lang = '"+ get_lang() +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        portf_description = row[0]
    market_asset_class = asset_class + ' ' + market + ' '+ strategy_type
    nickname = get_nickname()
    portf_description = portf_description.replace('{market_asset_class}', market_asset_class)
    portf_description = portf_description.replace('{nickname}', nickname)
    return_data = portf_description
    cursor.close()
    connection.close()
    return return_data

def get_portf_decimal_place():
    """ xxx """
    return_data = 0
    suid = ''
    decimal_places = 0
    for i in range(5):
        suid = request.cookies.get('portf_s_' + str(i+1))
        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        if suid != None:
            sql = "SELECT instruments.decimal_places FROM instruments "+\
            "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "WHERE symbol_list.uid = " +\
            str(suid)
    
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                if row[0] > decimal_places:
                    decimal_places = row[0]
        cursor.close()
        connection.close()
    return_data = decimal_places
    return return_data

def portf_get_user_numeric_id():
    """ xxx """
    return_data = ''
    uid = user_get_uid()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT id FROM users WHERE uid='"+ str(uid) +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        return_data = row[0]
    cursor.close()
    connection.close()
    return return_data

def portf_gen_portf_t_instruments():
    """ xxx """
    return_data = ''
    portf_symbol = get_portf_suffix() + set_portf_symbol()
    portf_asset_class_id = get_portf_asset_class('i')
    portf_asset_class_name = get_portf_asset_class('n')
    portf_market_id = get_portf_market('i')
    portf_market_name = get_portf_market('n')
    portf_strategy_type = get_portf_strategy_type()
    portf_fullname = set_portf_fullname(portf_symbol,
                                        portf_asset_class_name,
                                        portf_market_name,
                                        portf_strategy_type)
    portf_owner = portf_get_user_numeric_id()
    portf_description = get_portf_description(portf_asset_class_name,
                                              portf_market_name,
                                              portf_strategy_type)
    portf_account_reference = 1000
    portf_decimal_place = get_portf_decimal_place()
    portf_pip = 1
    portf_sector = 0
    portf_unit = get_portf_market('cur')
    portf_creation_date = set_portf_date()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "INSERT INTO symbol_list(symbol) VALUES('"+ str(portf_symbol) +"')"
    cursor.execute(sql)
    connection.commit()

    sql = "INSERT INTO instruments(symbol,fullname,description,"+\
    "asset_class,market,decimal_places,pip, sector,unit,"+\
    "account_reference,owner,creation_date) "+\
    "VALUES ('"+\
    str(portf_symbol) +"','"+\
    str(portf_fullname) +"','"+\
    str(portf_description) +"','"+\
    str(portf_asset_class_id) +"','"+\
    str(portf_market_id) +"','"+\
    str(portf_decimal_place) +"','"+\
    str(portf_pip) +"','"+\
    str(portf_sector) +"','"+\
    str(portf_unit) +"','"+\
    str(portf_account_reference) +"','"+\
    str(portf_owner) +"','"+\
    str(portf_creation_date) +"')"

    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    return_data = portf_symbol
    return return_data

def portf_add_allocation(portf_symbol):
    """ xxx """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    portf_suid = ''
    portf_s = ''
    portf_fullname = ''
    portf_type = ''
    portf_conv = ''
    insert_values = ''

    for i in range(5):
        portf_suid = request.cookies.get('portf_s_' + str(i+1))
        portf_type = request.cookies.get('portf_s_' + str(i+1) + '_type')
        portf_conv = request.cookies.get('portf_s_' + str(i+1) + '_conv')

        if str(portf_suid) != '' and str(portf_suid) != '0' and portf_suid != None:
            sql = "SELECT instruments.symbol, instruments.fullname FROM instruments "+\
            "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "WHERE symbol_list.uid = " +\
            str(portf_suid)

            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                portf_s = row[0]
                portf_fullname = row[1]

            if i != 0:
                insert_values = insert_values + ','

            insert_values = insert_values + "('"+\
            str(portf_symbol) +"','"+\
            str(portf_s) +"','"+\
            str(portf_fullname) +"',1,'"+\
            str(portf_type) +"','"+\
            str(portf_conv) +"')"

    if portf_suid() != None:
        sql = "INSERT IGNORE INTO "+\
        "portfolios(portf_symbol,symbol,alloc_fullname,quantity,"+\
        "strategy_order_type,strategy_conviction) VALUES "+\
        insert_values
        cursor.execute(sql)
        connection.commit()

    cursor.close()
    connection.close()

def portf_insert_data():
    """ xxx """
    return_data = ''
    portf_symbol = portf_gen_portf_t_instruments()
    return_data = portf_symbol
    portf_add_allocation(portf_symbol)
    return return_data

################################################################################

def get_portf_uid_from_symbol(symbol):
    """ xxx """
    return_data = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT uid FROM symbol_list WHERE symbol = '"+ symbol +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        return_data = row[0]
    cursor.close()
    connection.close()
    return return_data

def portf_save(burl):
    """ xxx """
    portf_symbol = portf_insert_data()
    generate_portfolio(portf_symbol)
    portf_uid = get_portf_uid_from_symbol(portf_symbol)
    resp = make_response(redirect(burl+'p/?uid='+ str(portf_uid) + '&pop=1'))
    return resp

def portf_save_conviction(burl, mode, sel):
    """ xxx """
    #mode = "type1", "type2", "type3", "conv1", "conv2"...
    #sel = "long/short", "long", "short", "neutral", "weak", "strong"
    resp = make_response(redirect(burl+'p/?ins=3'))
    if mode == "type1":
        resp.set_cookie('portf_s_1_type',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    if mode == "type2":
        resp.set_cookie('portf_s_2_type',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    if mode == "type3":
        resp.set_cookie('portf_s_3_type',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    if mode == "type4":
        resp.set_cookie('portf_s_4_type',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    if mode == "type5":
        resp.set_cookie('portf_s_5_type',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))

    if mode == "conv1":
        resp.set_cookie('portf_s_1_conv',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    if mode == "conv2":
        resp.set_cookie('portf_s_2_conv',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    if mode == "conv3":
        resp.set_cookie('portf_s_3_conv',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    if mode == "conv4":
        resp.set_cookie('portf_s_4_conv',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    if mode == "conv5":
        resp.set_cookie('portf_s_5_conv',
                        str(sel),
                        expires=datetime.datetime.now() + datetime.timedelta(days=1))
    return resp

def get_portf_table_rows(burl):
    """ xxx """
    return_data = ''
    for i in range(5):

        strategy_order_type = request.cookies.get('portf_s_' + str(i+1) + '_type')
        strategy_conviction = request.cookies.get('portf_s_' + str(i+1) + '_conv')
        instr_selection = ''
        uid = request.cookies.get('portf_s_' + str(i+1))
        symbol = ''
        fullname = ''
        if not uid is None or uid == '':
            connection = pymysql.connect(host=DB_SRV,
                                         user=DB_USR,
                                         password=DB_PWD,
                                         db=DB_NAME,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            cursor = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT instruments.fullname, instruments.symbol "+\
            "FROM instruments JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
            "WHERE symbol_list.uid=" + str(uid)
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                fullname = row[0]
                symbol = row[1]
                instr_selection = '<strong>' + fullname + '</strong>&nbsp;('+ symbol +')'
            cursor.close()
            connection.close()

        if strategy_order_type == 'long/short':
            class_order_type = 'btn-secondary'
        if strategy_order_type == 'long':
            class_order_type = 'btn-success'
        if strategy_order_type == 'short':
            class_order_type = 'btn-danger'

        if symbol != '':
            return_data = return_data + ''+\
            '    <tr>'+\
            '      <th style="text-align: left" scope="row">'+\
            '       <div class="dropdown">'+\
            '           <button class="btn '+\
            class_order_type +' dropdown-toggle" type="button" id="strategy_order_type_'+\
            str(i+1) +'" name="strategy_order_type_'+\
            str(i+1) +'" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+\
            strategy_order_type +\
            '           </button>'+\
            '           <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'+\
            '               <a class="dropdown-item" href="'+\
            burl + 'p/?ins=4&mode=type'+\
            str(i+1)+'&x=long/short'+'">Buy and Sell (long/short)</a>'+\
            '               <a class="dropdown-item" href="'+\
            burl + 'p/?ins=4&mode=type'+\
            str(i+1)+'&x=long'+'">Buy Only (long)</a>'+\
            '               <a class="dropdown-item" href="'+\
            burl + 'p/?ins=4&mode=type'+\
            str(i+1)+'&x=short'+'">Sell Only (short)</a>'+\
            '           </div>'+\
            '       </div>'+\
            '       </th>'+\
            '       <td style="text-align: left">'+\
            '       <div class="dropdown">'+\
            '           <button class="btn btn-secondary dropdown-toggle" '+\
            'type="button" id="strategy_conviction_'+\
            str(i+1) +'" name="strategy_conviction_'+\
            str(i+1) +'" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+\
            strategy_conviction +\
            '           </button>'+\
            '           <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'+\
            '               <a class="dropdown-item" href="'+\
            burl + 'p/?ins=4&mode=conv'+\
            str(i+1)+'&x=weak'+'">weak</a>'+\
            '               <a class="dropdown-item" href="'+\
            burl + 'p/?ins=4&mode=conv'+\
            str(i+1)+'&x=strong'+'">strong</a>'+\
            '               <a class="dropdown-item" href="'+\
            burl + 'p/?ins=4&mode=conv'+\
            str(i+1)+'&x=neutral'+'">neutral</a>'+\
            '           </div>'+\
            '       </div>'+\
            '      </td>'+\
            '      <td style="text-align: left" width="100%">'+ instr_selection +'</td>'+\
            '    </tr>'
    return return_data

def get_list_portf_alloc(burl):
    """ xxx """
    return_data = ''
    l_conviction = 'What is your conviction?'
    l_button_save = 'Save and generate strategy'
    return_data = '' +\
    '<table class="table table-hover">'+\
    '  <thead>'+\
    '    <tr>'+\
    '      <th style="text-align: left" scope="col" colspan="3">'+ l_conviction +'</th>'+\
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
    '   <button type="submit" '+\
    'class="btn btn-info btn-lg form-signin-btn">'+\
    '<i class="fas fa-save"></i>&nbsp;'+ l_button_save +'</button>'+\
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
    return return_data

def get_box_portf_save(burl):
    """ xxx """
    box_content = ''
    box_content = '<div class="box">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content sa-instr-n-portf-list">'+\
    get_list_portf_alloc(burl)+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content
