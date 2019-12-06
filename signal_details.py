""" Signal details """
import pymysql.cursors
from sa_func import get_etoro_symbol_from_uid, get_broker_affiliate_link
from app_popup_modal import open_window

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_signal_details(uid, burl, mode):
    """ xxx """
    # =============================================================================
    # uid = symbol uid
    # mode = 'newsfeed','desc'
    # =============================================================================
    descr_box = ''
    broker = 'eToro'
    height = '600'
    width = '360'
    button_href = burl + 's/?uid=' + str(uid)
    etoro_symbol = get_etoro_symbol_from_uid(uid)
    trade_href = get_broker_affiliate_link(broker, 'baseurl') + str(etoro_symbol)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, "+\
    "instruments.trade_1_entry, instruments.trade_1_tp, instruments.trade_1_sl, "+\
    "instruments.trade_3_entry, instruments.trade_3_tp, instruments.trade_3_sl, "+\
    "instruments.decimal_places FROM instruments "+\
    "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid=" + str(uid)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        symbol = row[0]
        trade_1_entry = row[1]
        trade_1_tp = row[2]
        trade_1_sl = row[3]
        trade_3_entry = row[4]
        trade_3_tp = row[5]
        trade_3_sl = row[6]
        decimal_places = row[7]

    sql = "SELECT badge FROM feed JOIN symbol_list ON symbol_list.symbol = feed.symbol "+\
    "WHERE symbol_list.uid=" + str(uid) + " AND feed.type=1 "
    cursor.execute(sql)
    res = cursor.fetchall()
    badge = ''
    for row in res:
        badge = row[0]
    
    if badge.find('-999') == -1:
        if (badge.find('-0') == -1 and badge.find('-1') == -1 and
                badge.find('-2') == -1 and badge.find('-3') == -1 and
                badge.find('-4') == -1 and badge.find('-5') == -1 and
                badge.find('-6') == -1 and badge.find('-7') == -1 and
                badge.find('-8') == -1 and badge.find('-9') == -1):
            signal = '<a href="javascript:{}" '+\
            'onclick="'+ open_window(trade_href, width, height, 0, 0) +'"'+\
            ' class="btn btn-outline-success"><h4>Buy</h4></a>'
            entry = trade_1_entry
            target_price = trade_1_tp
            stop_loss = trade_1_sl
        else:
            signal = '<a href="javascript:{}" '+\
            'onclick="'+ open_window(trade_href, width, height, 0, 0) +'"'+\
            'class="btn btn-outline-danger"><h4>Sell</h4></a>'
            entry = trade_3_entry
            target_price = trade_3_tp
            stop_loss = trade_3_sl
    else:
        signal = '<a href="javascript:{}" '+\
        'onclick="'+ open_window(trade_href, width, height, 0, 0) +'"'+\
        'class="btn btn-outline-primary"><h4>Wait</h4></a>'
        entry = trade_1_entry
        target_price = trade_1_tp
        stop_loss = trade_1_sl

    hd_entry = 'Entry @'
    hd_tp = 'Target price'
    hd_sl = 'Stop loss'

    c_symbol = ''
    c_signal_column_width = 'style="width: 10%"'

    if mode == 'newsfeed':
        c_symbol = '<td rowspan="2"><a href="'+\
        button_href +\
        '" class="btn btn-outline-info"><h4>'+\
        str(symbol) +'</h4></a></td>'
        c_signal_column_width = ''

    c_signal = signal
    c_entry = str(round(entry, decimal_places))
    c_tp = str(round(target_price, decimal_places))
    c_sl = str(round(stop_loss, decimal_places))

    descr_box = '' +\
    '               <table class="table table-sm sa-table-sm">'+\
    '                   <tbody>'+\
    '                       <tr>'+\
    '                           <td '+ c_signal_column_width +' rowspan="2">'+ c_signal +'</td>'+\
    c_symbol+\
    '                           <td style="width: 10%">'+ hd_entry +'</td>'+\
    '                           <td style="width: 10%">'+ hd_tp +'</td>'+\
    '                           <td style="width: 60%">'+ hd_sl +'</td>'+\
    '                       </tr>'+\
    '                       <tr>'+\
    '                           <td><h6>'+ c_entry +'</h6></td>'+\
    '                           <td><h6>'+ c_tp +'</h6></td>'+\
    '                           <td><h6>'+ c_sl +'</h6></td>'+\
    '                       </tr>'+\
    '                   </tbody>'+\
    '               </table>'

    cursor.close()
    connection.close()

    return descr_box
