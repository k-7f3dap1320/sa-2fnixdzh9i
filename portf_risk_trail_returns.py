""" Portfolio trail return graph """
import pymysql.cursors
from app_cookie import theme_return_this
from trail_returns_chart import get_trailing_returns
from sa_func import get_selected_lang
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_risk_table(uid):
    """ xxx """
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname, instruments.asset_class, "+\
    "instruments.market, is_benchmark, "+\
    "instruments.beta_st, instruments.alpha_st, "+\
    "instruments.stdev_st, instruments.sharpe_ratio_st, "+\
    "instruments.maximum_dd_st, instruments.romad_st, instruments.volatility_risk_st "+\
    "FROM smartalpha.instruments JOIN smartalpha.symbol_list "+\
    "ON instruments.symbol = symbol_list.symbol "+\
    "WHERE symbol_list.uid =" + str(uid)
    cursor.execute(sql)
    res = cursor.fetchall()
    a_fullname = ''
    a_asset_class = ''
    a_market = ''
    a_maximum_dd_st = ''
    a_romad_st = ''
    a_volatility_risk_st = ''
    for row in res:
        a_fullname = row[0]
        a_asset_class = row[1]
        a_market = row[2]
        a_maximum_dd_st = str(round(row[8]*100, 2)) +'%'
        a_romad_st = str(round(row[9], 2))
        a_volatility_risk_st = str(round(row[10]*100, 2)) +'%'

    sql = "SELECT instruments.fullname, instruments.asset_class, "+\
    "instruments.market, is_benchmark, "+\
    "instruments.beta_st, instruments.alpha_st, "+\
    "instruments.stdev_st, instruments.sharpe_ratio_st, "+\
    "instruments.maximum_dd_st, instruments.romad_st, instruments.volatility_risk_st "+\
    "FROM smartalpha.instruments JOIN smartalpha.symbol_list "+\
    "ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.asset_class='"+\
    a_asset_class +"' AND instruments.market='"+\
    a_market +"' AND is_benchmark=1 "
    cursor.execute(sql)
    res = cursor.fetchall()
    b_fullname = ''
    b_maximum_dd_st = ''
    b_romad_st = ''
    b_volatility_risk_st = ''
    for row in res:
        b_fullname = row[0]
        b_maximum_dd_st = str(round(row[8]*100, 2)) +'%'
        b_romad_st = str(round(row[9], 2))
        b_volatility_risk_st = str(round(row[10]*100, 2)) +'%'
    cursor.close()
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
    ret = content
    return ret

def get_box_risk_content(uid):
    """ xxx """
    box_content = ''
    lang = get_selected_lang()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT portf_risk_consider FROM `recommendations` WHERE lang='"+ lang +"' "
    cursor.execute(sql)
    res = cursor.fetchall()
    text_content = ''
    for row in res:
        text_content = row[0]

    sql = "SELECT instruments.account_reference, instruments.unit, "+\
    "instruments.beta_st, instruments.alpha_st, instruments.stdev_st, "+\
    "instruments.sharpe_ratio_st, "+\
    "instruments.maximum_dd_st, instruments.romad_st, instruments.volatility_risk_st " +\
    "FROM instruments "+\
    "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid=" + str(uid)
    cursor.execute(sql)
    res = cursor.fetchall()
    account_reference = 0
    unit = ''
    stdev_st = 0
    volatility_risk_st = 0
    for row in res:
        account_reference = row[0]
        unit = row[1]
        stdev_st = row[4]
        volatility_risk_st = row[8]
    cursor.close()
    connection.close()

    dollar_amount = round(stdev_st, 2)
    percentage = round(volatility_risk_st*100, 2)

    text_content = text_content.replace('{account_reference}', str(int(account_reference)))
    text_content = text_content.replace('{unit}', str(unit))
    text_content = text_content.replace('{dollar_amount}', str(dollar_amount))
    text_content = text_content.replace('{percentage}', str(percentage) + "%")

    l_title = 'Risk considerations'

    box_content = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-signal-recomm-trail-ret" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    '                   <div>'+ text_content +'</div>'+\
    '<div>'+ get_risk_table(uid) +'</div>'+\
    '            </div>'+\
    '        </div>'
    return box_content


def get_box_trail_returns_content(uid):
    """ xxx """
    box_content = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname FROM instruments "+\
    "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid=" + str(uid)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        fullname = row[0]

    l_title = fullname + ' portfolio trailing returns'
    box_content = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-signal-recomm-trail-ret" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    get_trailing_returns(uid) +\
    '            </div>'+\
    '        </div>'
    cursor.close()
    connection.close()
    return box_content

def get_portf_risk_trail_returns(uid):
    """ xxx """
    return get_box_risk_content(uid) + get_box_trail_returns_content(uid)
