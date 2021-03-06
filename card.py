""" card object """
import datetime
import pymysql.cursors
from sa_func import get_uid
from card_chart import get_card_chart
from app_cookie import theme_return_this
from print_google_ads import print_google_ads
from tradingview_mini_chart import get_tradingview_mini_chart
from list_instr_n_portf import get_box_list_instr_n_portf
from app_popup_modal import open_window_as
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def found_signals(sql):
    ret = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    res = cursor.fetchall()
    i = 0
    for row in res:
        i += 1
    ret = i
    cursor.close()
    connection.close()
    return ret

def get_card(selection, type_sel, burl, terminal):
    """ Get card """
    no_signal_weekend = 'There is no trading signals at the moment.'
    return_data = ''
    if selection != '' and selection is not None:
        if type_sel == 1:
            sql = "SELECT short_title, short_description, content, "+\
            "url, ranking, badge, symbol FROM feed "+\
            "WHERE (asset_class LIKE '%"+selection+"%' OR market LIKE '%"+selection+"%') "+\
            "AND type=1 AND badge<>'-999' ORDER BY ranking DESC LIMIT 15"
            if found_signals(sql) == 0:
                sql = "SELECT short_title, short_description, content, "+\
                "url, ranking, badge, symbol FROM feed "+\
                "WHERE type=1 AND badge<>'-999' ORDER BY ranking DESC LIMIT 15"
        if type_sel == 9:
            sql = "SELECT short_title, short_description, content, "+\
            "url, ranking, badge, symbol FROM feed "+\
            "WHERE (asset_class LIKE '%"+selection+"%' OR market LIKE '%"+selection+"%') "+\
            "AND globalrank<>0 AND type=9 ORDER BY globalrank ASC LIMIT 7"
    else:
        if type_sel == 1:
            sql = "SELECT short_title, short_description, content, "+\
            "url, ranking, badge, symbol FROM feed "+\
            "WHERE type=1 and badge<>'-999' ORDER BY ranking DESC LIMIT 15"
        if type_sel == 9:
            sql = "SELECT short_title, short_description, content, "+\
            "url, ranking, badge, symbol FROM feed "+\
            "WHERE type=9 ORDER BY ranking DESC LIMIT 7"

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    res = cursor.fetchall()
    
    title_portf = "Top strategies by Members"
    button_portf = "More strategy Portfolios"
    button_portf_link = burl + 'ls/?w=portf'
    title_signals = "Top Trading Signals"
    button_signals = "More Trading Signals"
    button_signals_link = burl + 'ls/?w=instr'

    if type_sel == 9:
        return_data = '<div class="box"><span class="sectiont">'+\
        '<i class="fas fa-chart-pie"></i>&nbsp;'+ title_portf +'</span><div class="row">'
    if type_sel == 1:
        return_data = '<div class="box"><span class="sectiont">'+\
        '<i class="fas fa-chart-line"></i>&nbsp;'+ title_signals +'</span><div class="row">'

    return_data = return_data + '' +\
    '<div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">'+\
    '   <div class="text-center rounded" style="margin-left: 5px;margin-top: 50px;">'+\
    print_google_ads('rectangle', 'center') +\
    '   </div>'+\
    '</div>'
    for row in res:
        short_title = row[0]
        content = row[2]
        url = row[3].replace('{burl}', burl)
        badge = row[5]
        symbol = row[6]
        uid = get_uid(symbol)

        color = theme_return_this("#17a2b8", "orange")
        portf_content_by = 'Strategy by '

        if (badge.find('-0') == -1 and badge.find('-1') == -1 and
                badge.find('-2') == -1 and badge.find('-3') == -1 and
                badge.find('-4') == -1 and badge.find('-5') == -1 and
                badge.find('-6') == -1 and badge.find('-7') == -1 and
                badge.find('-8') == -1 and badge.find('-9') == -1):
            badge_class = 'badge badge-success'
            expl_label = "*Potential returns in the next 7 days"
            if type_sel == 1:
                color = "green"
        else:
            badge_class = 'badge badge-danger'
            expl_label = "*Potential risk in the next 7 days"
            if type_sel == 1:
                color = "red"

        if type_sel == 9:
            expl_label = "*Potential returns in the next 7 days"

        link_label = "Click here for details"


        ### Trading Instruments ###
        if type_sel == 1:
            return_data = return_data + '' +\
            '        <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">'+\
            '            <div class="box-part text-center rounded">'+\
            get_tradingview_mini_chart(uid, '100%', '250', 'true', '1y', 1,'1') +\
            '<div>&nbsp;</div>'+\
            '                <div class="title"><a href="' +\
            url + '" target="_blank" class="'+\
            badge_class+'" data-toggle="tooltip" data-placement="bottom" title="'+\
            expl_label +'" >'+\
            badge+'</a>&nbsp;<span class="expl">'+\
            expl_label+'</span></div>'+\
            '            </div>'+\
            '        </div>'

        ### Portfolios ###
        if type_sel == 9:
            return_data = return_data + get_card_chart(uid, color) +\
            '        <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">'+\
            '            <div class="box-part text-center rounded">'+\
            '                <div id="chart_div_'+str(get_uid(symbol))+'"></div>'+\
            '                <div class="title"><h6 style="line-height: 1.5;">'+\
            short_title+'&nbsp;<a href="' + url + '" target="_blank" class="'+\
            badge_class+'" data-toggle="tooltip" data-placement="bottom" title="'+\
            expl_label +'" >'+badge+'</a></h6></div>'+\
            '                <div class="text"><span class="desc">'+\
            portf_content_by +\
            content.replace('{burl}', burl) +'</span></div>'+\
            '                <a href="' +\
            url + '" target="_blank" class="btn btn-outline-primary" '+\
            'role="button" aria-pressed="true">'+\
            link_label+'</a>'+\
            '                <div class="text"><span class="expl">'+\
            expl_label+'</span></div>'+\
            '            </div>'+\
            '        </div>'
            
    button_more_signals = '</div></div><div class="box"><a href="'+\
    open_window_as(button_signals_link, terminal) +\
    '" role="button" class="btn btn-outline-secondary btn-lg btn-block">'+\
    '<strong>'+button_signals+'&nbsp;<i class="fas fa-angle-double-down"></i>'+\
    '</strong></a></div>'
    
    button_more_strategies = '</div></div><div class="box"><a href="'+\
    open_window_as(button_portf_link, terminal) +\
    '" role="button" class="btn btn-outline-secondary btn-lg btn-block">'+\
    '<strong>'+button_portf+'&nbsp;<i class="fas fa-angle-double-down"></i></strong></a></div>'

    if type_sel == 9:
        return_data = return_data + button_more_strategies
    if type_sel == 1:
        return_data = return_data + button_more_signals

    if type_sel == 1:
        date_today = datetime.datetime.now()
        no_signal_content = '<div><div><i class="fas fa-exclamation-circle"></i>&nbsp;'+\
        '<strong>'+ no_signal_weekend +'</strong><br /><br />'+ button_more_signals
        
        if date_today.weekday() == 5:
            return_data = no_signal_content
        if date_today.weekday() == 6:
            return_data = no_signal_content

    cursor.close()
    connection.close()
    return return_data
