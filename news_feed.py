# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *
from sa_func import *
from tradingview_single_ticker import *
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def get_newsfeed(x,suid,numline,show_chart):
    ### ------------------------------------------------------------------------
    # x == 0 : world top news
    # x == 1 : news based on users default market, asset_class selection
    # x == 2 : news based on users portfolio selection
    # suid == []: news from selected uid of the symbol
    # numline == []: number of line of news to return
    #show_chart == 1: show relevant chart or sentiment bar if x == 0
    ### ------------------------------------------------------------------------
    r = ''
    try:
        #theme_return_this(for_light,for_dark)
        theme = get_sa_theme()
        l_view_article = 'more >'
        l_newsfeed_title = 'Newsfeed'
        lang = 'en'
        feed_type = 3
        bsclass_left = 'col-lg-12 col-md-12 col-sm-12'
        bsclass_right = 'col-lg-12 col-md-12 col-sm-12'
        wrapstyle = 'style="white-space: nowrap;"'
        rightcol_line_sep = ''


        if x == 0 and suid == 0: l_newsfeed_title = 'World News and Top Stories'
        if x == 1 and suid == 0: l_newsfeed_title = 'Featured Articles'
        if x == 2 and suid == 0: l_newsfeed_title = 'News Top Selection'

        if show_chart == 1:
            if x == 0:
                bsclass_left = 'col-lg-10 col-md-10 col-sm-10'
                bsclass_right = 'col-lg-2 col-md-2 col-sm-2'
            if x == 1:
                bsclass_left = 'col-lg-8 col-md-7 col-sm-7'
                bsclass_right = 'col-lg-4 col-md-5 col-sm-5'
            if x == 2:
                bsclass_left = 'col-lg-10 col-md-10 col-sm-10'
                bsclass_right = 'col-lg-2 col-md-2 col-sm-2'

        query = ' '+\
        'SELECT DISTINCT short_title, '+\
        'short_description, '+\
        'url, badge, '+\
        'ranking, '+\
        '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time, symbol '+\
        'FROM feed '+\
        'WHERE '+\
        'type=3 '+\
        'AND '+\
        'symbol LIKE "%%" '+\
        'AND '+\
        'asset_class LIKE "%%" '+\
        'AND '+\
        'lang LIKE "%'+ str(lang) +'%" '+\
        'AND ranking <0.9 '+\
        'ORDER BY date DESC LIMIT '+ str(numline)

        if x == 0:
            query = 'SELECT DISTINCT short_title, short_description, url, badge, ranking, '+\
            '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time, symbol '+\
            'FROM feed '+\
            'WHERE asset_class="" AND market="" AND lang LIKE "%'+ str(lang) +'%" '+\
            'AND ranking <0.9 AND type='+ str(feed_type) + ' ' +\
            'ORDER BY date DESC LIMIT '+ str(numline)

        if x == 1:
            query = 'SELECT DISTINCT short_title, short_description, url, badge, ranking, '+\
            '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time, symbol '+\
            'FROM feed '+\
            'WHERE (asset_class LIKE "%'+ str( get_user_default_profile() ) +'%" OR market LIKE "%'+ str( get_user_default_profile() ) +'%") AND lang LIKE "%'+ str(lang) +'%" '+\
            'AND ranking <0.9 AND type='+ str(feed_type) + ' ' +\
            'ORDER BY date DESC LIMIT '+ str(numline)
            wrapstyle = 'style="" '
            rightcol_line_sep = 'border-top:0.5px; border-top-style: dotted; '

        if x == 2:
            query = ' '+\
            'SELECT DISTINCT short_title, short_description, url, badge, ranking, '+\
            '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time, symbol '+\
            'FROM feed '+\
            'WHERE symbol IN(SELECT DISTINCT portfolios.symbol FROM instruments '+\
            'JOIN portfolios ON instruments.symbol = portfolios.portf_symbol WHERE instruments.owner = (SELECT users.id FROM users WHERE uid = "'+ str( get_user() ) +'") ) AND ranking <0.9 AND type='+ str(feed_type) + ' '+\
            'ORDER BY date DESC LIMIT '+ str(numline) +';'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = query
        print(sql)
        cr.execute(sql)
        rs = cr.fetchall()
        newsrow ='<span class="sectiont"><i class="far fa-newspaper"></i>&nbsp;'+ l_newsfeed_title +'</span>'
        i = 1
        newsrow = newsrow + '<div class="row">'
        for row in rs:
            unistr = 'x'+ str( get_random_str(10) ) + 'x'
            news_url = row[2]
            news_title = str(row[0]) +' '+ str(row[3])
            news_ranking = row[4]
            news_date = get_elapsed_time( row[5] )
            symbol = str(row[6])
            contextstyle = ''

            if news_ranking<=-0.8: contextstyle = theme_return_this('color: white; background-color: red;', 'color: white; background-color: red;')
            if news_ranking>0 and news_ranking <=0.5: contextstyle = theme_return_this('color: black;','color: white;')

            news_content = str(row[1]) +' <br /><br />'+ '<a href="'+ str(row[2]) +'" target="_blank" >'+ l_view_article +'</a>'

            sentiment_badge = ''
            if news_ranking<0: sentiment_badge = '<span class="badge badge-danger">'+'neg: '+ str(round(news_ranking*100,1) )+'%'+'</span>'
            if news_ranking>0: sentiment_badge = '<span class="badge badge-success">'+'pos: '+ str(round(news_ranking*100,1) )+'%'+'</span>'


            newsrow = newsrow +\
            '    <div class="'+ bsclass_left +' col-xs-12" style="border-top:0.5px; border-top-style: dotted; "> '+\
            '       <div class="d-none d-sm-block" '+ wrapstyle +'>'+\
            '           <a href="'+ str(news_url) +'" target="_blank" style="'+ theme_return_this('color:black;','color:white;') +'" ><i class="fas fa-external-link-alt"></i></a>'+\
            '           <strong><a data-toggle="collapse" href="#'+ str(unistr)+'"  style="'+ contextstyle +'" >'+ '&nbsp;<span style="'+ theme_return_this('color:black;','color:#00ffff;') +' ">'+ str(news_date) +'</span>&nbsp;' + news_title  + '</a></strong>&nbsp;'+\
            '       </div>'+\
            '       <div class="d-sm-none" '+ wrapstyle +'>'+\
            '           <a href="'+ str(news_url) +'" target="_blank" style="'+ theme_return_this('color:black;','color:white;') +'" ><i class="fas fa-external-link-alt"></i></a>'+\
            '           <strong><a data-toggle="collapse" href="#'+ str(unistr)+'"  style="'+ contextstyle +'" >'+ '&nbsp;<span style="'+ theme_return_this('color:black;','color:#00ffff;') +' ">'+ str(news_date) +'</span>&nbsp;' + news_title  + '</a></strong>&nbsp;'+\
            '       </div>'+\
            '       <div class="collapse" id="'+ str(unistr) +'">'+ news_content +'<br /><br /></div>'+\
            '    </div>'+\
            '    <div class="'+ bsclass_right +' col-xs-1 d-none d-sm-block" style="'+ theme_return_this('background-color:white;','background-color:black;') + ' ' + rightcol_line_sep +'" >'+\
            draw_feed_chart(x,show_chart,news_ranking, symbol) +\
            '    </div>'
            i += 1
        newsrow = newsrow + '</div>'
        cr.close()
        connection.close()

        r = newsrow

    except Exception as e: print(e)
    return r

def draw_feed_chart(x,show_chart,score,symbol):
    r = ''
    try:
        if show_chart == 1:
            if x == 0:
                r = get_sentiment_progressbar(score)
            if x == 1:
                if symbol != '': r = get_tradingview_single_ticker( get_uid(str(symbol)) )
            if x == 2:
                r = get_sentiment_progressbar(score)
    except Exception as e: print(e)
    return r

def get_sentiment_progressbar(score):
    r = ''
    try:
        t = 1
        pos = 0; neg = 0
        if score < 0:
            pos = 1+score
            neg = abs(score)
        if score > 0:
            pos = score
            neg = 1-score
        pos = pos *100; neg = neg *100

        content = ' '+\
        '<div class="progress" style="width: 100%;">'+\
        '  <div class="progress-bar bg-success progress-bar-striped" role="progressbar" style="width: '+ str(pos) +'%" aria-valuenow="'+ str(pos) +'" aria-valuemin="0" aria-valuemax="100"></div>'+\
        '  <div class="progress-bar bg-danger progress-bar-striped" role="progressbar" style="width: '+ str(neg) +'%" aria-valuenow="'+ str(neg) +'" aria-valuemin="0" aria-valuemax="100"></div>'+\
        '</div>'

        r = content

    except Exception as e: print(e)
    return r
