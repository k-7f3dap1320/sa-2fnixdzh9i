# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
from sa_func import *
from card_chart import *
from app_cookie import *
from print_google_ads import *
access_obj = sa_db_access()
import pymysql.cursors

from tradingview_mini_chart import *


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_card(x,t,burl):

    r = ''
    try:
        if t == 1:
            sql = "SELECT short_title, short_description, content, url, ranking, badge, symbol FROM feed "+\
            "WHERE (asset_class LIKE '%"+x+"%' OR market LIKE '%"+x+"%') AND type=1 ORDER BY ranking DESC LIMIT 15"
        if t == 9:
            if user_is_login() == 0:
                sql = "SELECT short_title, short_description, content, url, ranking, badge, symbol FROM feed "+\
                "WHERE (asset_class LIKE '%"+x+"%' OR market LIKE '%"+x+"%') AND globalrank<>0 AND type=9 ORDER BY globalrank ASC LIMIT 11"
            else:
                sql = "SELECT * FROM (SELECT feed.short_title, feed.short_description, feed.content, feed.url, feed.ranking, feed.badge, feed.symbol FROM feed JOIN instruments "+\
                "ON feed.symbol = instruments.symbol WHERE instruments.owner = "+ str(get_user_numeric_id() ) +" AND feed.type=9 ORDER BY feed.globalRank) AS Q1 "+\
                "UNION "+\
                "SELECT * FROM (SELECT feed.short_title, feed.short_description, feed.content, feed.url, feed.ranking, feed.badge, feed.symbol FROM feed JOIN instruments ON feed.symbol = instruments.symbol WHERE feed.globalRank <> 0 AND instruments.y1 > 0 AND (feed.asset_class LIKE '%"+x+"%' OR feed.market LIKE '%"+x+"%') AND type=9 ORDER BY feed.globalrank LIMIT 10) AS Q2"
    except:
        if t == 1:
            sql = "SELECT short_title, short_description, content, url, ranking, badge, symbol FROM feed "+\
            "WHERE type=1 ORDER BY ranking DESC LIMIT 15"
        if t == 9:
            if user_is_login() == 0:
                sql = "SELECT short_title, short_description, content, url, ranking, badge, symbol FROM feed "+\
                "WHERE type=9 ORDER BY ranking DESC LIMIT 12"
            else:
                sql = "SELECT * FROM (SELECT feed.short_title, feed.short_description, feed.content, feed.url, feed.ranking, feed.badge, feed.symbol FROM feed JOIN instruments "+\
                "ON feed.symbol = instruments.symbol WHERE instruments.owner = "+ str(get_user_numeric_id() ) +" AND feed.type=9 ORDER BY feed.globalRank) AS Q1 "+\
                "UNION "+\
                "SELECT * FROM (SELECT feed.short_title, feed.short_description, feed.content, feed.url, feed.ranking, feed.badge, feed.symbol FROM feed JOIN instruments ON feed.symbol = instruments.symbol WHERE feed.globalRank <> 0 AND instruments.y1 > 0 AND type=9 ORDER BY feed.globalrank LIMIT 11) AS Q2"
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        cr.execute(sql)
        rs = cr.fetchall()
        title_portf = "Top Portfolios by Members"
        button_portf = "More Portfolios"
        button_portf_link = burl + 'ls/?w=portf&x='+ str(x)
        title_signals = "Top Trading Signals"
        button_signals = "More Trading Signals"
        button_signals_link = burl + 'ls/?w=instr&x='+ str(x)

        if t == 9: r = '<div class="box"><span class="sectiont"><i class="fas fa-chart-pie"></i>&nbsp;'+ title_portf +'</span><div class="row">'
        if t == 1: r = '<div class="box"><span class="sectiont"><i class="fas fa-chart-line"></i>&nbsp;'+ title_signals +'</span><div class="row">'

        r = r + '' +\
        '<div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">'+\
        '   <div class="text-center rounded" style="margin-left: 5px;margin-top: 50px;">'+\
        print_google_ads('rectangle','center') +\
        '   </div>'+\
        '</div>'

        for row in rs:
            short_title = row[0]
            short_description = row[1]
            content = row[2]
            url = row[3].replace('{burl}',burl)
            ranking = row[4]
            badge = row[5]
            symbol = row[6]
            uid = get_uid(symbol)

            color = "black"
            portf_content_by = 'Portfolio by '

            if (badge.find('-0') == -1 and badge.find('-1') == -1 and
            badge.find('-2') == -1 and badge.find('-3') == -1 and
            badge.find('-4') == -1 and badge.find('-5') == -1 and
            badge.find('-6') == -1 and badge.find('-7') == -1 and
            badge.find('-8') == -1 and badge.find('-9') == -1) :
                badge_class = 'badge badge-success'
                expl_label = "*Potential returns in the next 7 days"
                if t == 1:
                    color = "green"
            else:
                badge_class = 'badge badge-danger'
                expl_label = "*Potential risk in the next 7 days"
                if t == 1:
                    color = "red"

            if t == 9:
                expl_label = "*Potential returns in the next 7 days"

            link_label = "Click here for details"


            ### Trading Instruments ###
            if t == 1:
                r = r + '' +\
                '        <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">'+\
                '            <div class="box-part text-center rounded">'+\
                get_tradingview_mini_chart(uid,'90%','200','true','1y') +\
                '                <div class="title"><h6>'+short_title+'&nbsp;<a href="' + url + '" class="'+badge_class+'" data-toggle="tooltip" data-placement="bottom" title="'+ expl_label +'" >'+badge+'</a></h6></div>'+\
                '                <div class="text"><span class="desc">'+content+': '+short_description+'</span></div>'+\
                '                <a href="' + url + '" class="btn btn-outline-primary" role="button" aria-pressed="true">'+link_label+'</a>'+\
                '                <div class="text"><span class="expl">'+expl_label+'</span></div>'+\
                '            </div>'+\
                '        </div>'

            ### Portfolios ###
            if t == 9:
                r = r + get_card_chart(uid,color) +\
                '        <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">'+\
                '            <div class="box-part text-center rounded">'+\
                '                <div id="chart_div_'+str( get_uid(symbol) )+'"></div>'+\
                '                <div class="title"><h6 style="line-height: 1.5;">'+short_title+'&nbsp;<a href="' + url + '" class="'+badge_class+'" data-toggle="tooltip" data-placement="bottom" title="'+ expl_label +'" >'+badge+'</a></h6></div>'+\
                '                <div class="text"><span class="desc">'+ portf_content_by + content.replace('{burl}',burl) +'</span></div>'+\
                '                <a href="' + url + '" class="btn btn-outline-primary" role="button" aria-pressed="true">'+link_label+'</a>'+\
                '                <div class="text"><span class="expl">'+expl_label+'</span></div>'+\
                '            </div>'+\
                '        </div>'

        if t == 9: r = r + '</div></div><a href="'+ button_portf_link +'" role="button" class="btn btn-outline-secondary btn-lg btn-block"><strong>'+button_portf+'&nbsp;<i class="fas fa-angle-double-down"></i></strong></a>'
        if t == 1: r = r + '</div></div><a href="'+ button_signals_link +'" role="button" class="btn btn-outline-secondary btn-lg btn-block"><strong>'+button_signals+'&nbsp;<i class="fas fa-angle-double-down"></i></strong></a>'

        cr.close()
        connection.close()
    except Exception as e: print(e)

    return r
