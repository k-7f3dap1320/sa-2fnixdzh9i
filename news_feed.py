# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *
from sa_func import *
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
        l_view_article = 'View original article'
        lang = 'en'
        bsclass_left = 'col-lg-11 col-md-12 col-sm-12'
        bsclass_right = 'col-lg-11 col-md-12 col-sm-12'

        if show_chart == 1:
            bsclass_left = 'col-lg-7 col-md-7 col-sm-6'
            bsclass_right = 'col-lg-4 col-md-5 col-sm-6'
            if x == 0:
                bsclass_left = 'col-lg-9 col-md-9 col-sm-9'
                bsclass_right = 'col-lg-2 col-md-3 col-sm-3'


        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = ' '+\
        'SELECT short_title, short_description, url, badge, ranking FROM feed '+\
        'WHERE '+\
        'type=3 '+\
        'AND '+\
        'symbol LIKE "%%" '+\
        'AND '+\
        'asset_class LIKE "%%" '+\
        'AND '+\
        'lang LIKE "%'+ str(lang) +'%" '+\
        'AND ABS(ranking)>=0.4 AND ranking <0.9 '+\
        'ORDER BY date DESC LIMIT '+ str(numline)
        cr.execute(sql)
        rs = cr.fetchall()
        newsrow = ''
        i = 1
        for row in rs:
            unistr = 'x'+ str( get_random_str(10) ) + 'x'
            news_url = row[2]
            news_title = str(row[0]) +' '+ str(row[3])
            news_ranking = row[4]
            contextstyle = ''
            if news_ranking<=-0.8: contextstyle = theme_return_this('color: white; background-color: red;', 'color: white; background-color: red;')
            if news_ranking>0 and news_ranking <=0.5: contextstyle = theme_return_this('color: black;','color: white;')

            news_content = str(row[1]) +' <br /><br />'+ '<a href="'+ str(row[2]) +'" target="_blank" >'+ l_view_article +'</a>'

            sentiment_badge = ''
            if news_ranking<0: sentiment_badge = '<span class="badge badge-danger">'+'neg: '+ str(round(news_ranking*100,1) )+'%'+'</span>'
            if news_ranking>0: sentiment_badge = '<span class="badge badge-success">'+'pos: '+ str(round(news_ranking*100,1) )+'%'+'</span>'


            newsrow = newsrow +\
            '<div class="row">'+\
            '    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 d-none d-lg-block"></div>'+\
            '    <div class="'+ bsclass_left +' col-xs-12" style="border-top:0.5px; border-top-style: dotted; "> '+\
            '       <a href="'+ str(news_url) +'" target="_blank" style="'+ theme_return_this('color:black;','color:white;') +'" ><i class="fas fa-external-link-alt"></i></a>'+\
            '       <strong><a data-toggle="collapse" href="#'+ str(unistr)+'"  style="'+ contextstyle +'" >'+ news_title +'</a></strong>&nbsp;'+\
            sentiment_badge +\
            '       <div class="collapse" id="'+ str(unistr) +'">'+ news_content +'<br /><br /></div>'+\
            '    </div>'+\
            '    <div class="'+ bsclass_right +' col-xs-1 d-none d-sm-block" >'+\
            draw_feed_chart(x,show_chart,news_ranking) +\
            '    </div>'+\
            '</div>'
            i += 1

        cr.close()
        connection.close()

        r = newsrow

    except Exception as e: print(e)
    return r

def draw_feed_chart(x,show_chart,score):
    r = ''
    try:
        if show_chart == 1:
            if x == 0: r = get_sentiment_progressbar(score)
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
        '<div class="progress" style="width: 100px;">'+\
        '  <div class="progress-bar bg-success progress-bar-striped" role="progressbar" style="width: '+ str(pos) +'%" aria-valuenow="'+ str(pos) +'" aria-valuemin="0" aria-valuemax="100"></div>'+\
        '  <div class="progress-bar bg-danger progress-bar-striped" role="progressbar" style="width: '+ str(neg) +'%" aria-valuenow="'+ str(neg) +'" aria-valuemin="0" aria-valuemax="100"></div>'+\
        '</div>'

        r = content

    except Exception as e: print(e)
    return r
