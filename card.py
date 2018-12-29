# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
from sa_func import *
from card_chart import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def get_card(x,t):

    r = ''

    try:
        if t == 1:
            sql = "SELECT short_title, short_description, content, url, ranking, badge, symbol FROM feed "+\
            "WHERE (asset_class LIKE '%"+x+"%' OR market LIKE '"+x+"') AND type=1 ORDER BY ranking DESC LIMIT 40"
        if t == 9:
            sql = "SELECT short_title, short_description, content, url, ranking, badge, symbol FROM feed "+\
            "WHERE (asset_class LIKE '%"+x+"%' OR market LIKE '"+x+"') AND type=9 ORDER BY ranking DESC LIMIT 20"
    except:
        if t == 1:
            sql = "SELECT short_title, short_description, content, url, ranking, badge, symbol FROM feed "+\
            "WHERE type=1 ORDER BY ranking DESC LIMIT 40"
        if t == 9:
            sql = "SELECT short_title, short_description, content, url, ranking, badge, symbol FROM feed "+\
            "WHERE type=9 ORDER BY ranking DESC LIMIT 20"
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        cr.execute(sql)
        rs = cr.fetchall()
        r = '<div class="box"><div class="row">'
        for row in rs:
            short_title = row[0]
            short_description = row[1]
            content = row[2]
            url = row[3]
            ranking = row[4]
            badge = row[5]
            symbol = row[6]
            uid = get_uid(symbol)
            color = "black"
            portf_content_end_part = 'Portfolio'

            if badge.find('-') == -1:
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


            r = r + get_card_chart(uid,color)

            ### Trading Instruments ###
            if t == 1:
                r = r + ''+\
                '        <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">'+\
                '            <div class="box-part text-center">'+\
                '                <div id="chart_div_'+str( uid )+'"></div>'+\
                '                <div class="title"><h6>'+short_title+'&nbsp;<a href="' + url + '" class="'+badge_class+'" data-toggle="tooltip" data-placement="bottom" title="'+ expl_label +'" >'+badge+'</a></h6></div>'+\
                '                <div class="text"><span class="desc">'+content+': '+short_description+'</span></div>'+\
                '                <a href="' + url + '" class="btn btn-outline-primary" role="button" aria-pressed="true">'+link_label+'</a>'+\
                '                <div class="text"><span class="expl">'+expl_label+'</span></div>'+\
                '            </div>'+\
                '        </div>'

            ### Portfolios ###
            if t == 9:
                r = r + ''+\
                '        <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">'+\
                '            <div class="box-part text-center">'+\
                '                <div id="chart_div_'+str( get_uid(symbol) )+'"></div>'+\
                '                <div class="title"><h6>'+short_description+'&nbsp;<a href="' + url + '" class="'+badge_class+'" data-toggle="tooltip" data-placement="bottom" title="'+ expl_label +'" >'+badge+'</a></h6></div>'+\
                '                <div class="text"><span class="desc">'+ content + ' ' + portf_content_end_part +'</span></div>'+\
                '                <a href="' + url + '" class="btn btn-outline-primary" role="button" aria-pressed="true">'+link_label+'</a>'+\
                '                <div class="text"><span class="expl">'+expl_label+'</span></div>'+\
                '            </div>'+\
                '        </div>'


        r = r + '</div></div>'
        cr.close()
        connection.close()
    except Exception as e: print(e)

    return r
