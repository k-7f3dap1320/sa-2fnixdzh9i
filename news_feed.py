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
    r = ''
    try:
        #theme_return_this(for_light,for_dark)
        theme = get_sa_theme()
        l_view_article = 'View original article'
        lang = 'en'
        bsclass = 'col-lg-10 col-md-12'
        if show_chart == 1: bsclass = 'col-lg-5 col-md-6'


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
        'AND  ABS(ranking) >=0.6 '+\
        'ORDER BY date DESC LIMIT '+ str(numline)
        cr.execute(sql)
        rs = cr.fetchall()
        newsrow = ''
        i = 1
        for row in rs:
            unistr = 'x'+ str( get_random_str(10) ) + 'x'
            news_title = str(row[0]) +' '+ str(row[3])
            news_content = str(row[1]) +' </ br></ br>'+ '<a href="'+ str(row[2]) +'" target="_blank">'+ l_view_article +'</a>'
            news_ranking = row[4]

            rowbgcolor = ''
            if news_ranking >=0.8: rowbgcolor = theme_return_this('#00ff0045','darkblue')
            if news_ranking<=-0.8: rowbgcolor = theme_return_this('yellow', 'darkred')


            newsrow = newsrow +\
            '<div class="row">'+\
            '    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 d-none d-md-block"></div>'+\
            '    <div class="'+ bsclass +' col-sm-12 col-xs-12" style="border-top:0.5px; border-top-style: dotted; background-color:'+ rowbgcolor +'"> '+\
            '       <strong>'+'<i class="fas fa-rss-square"></i>'+'</strong>'+\
            '       <strong><a data-toggle="collapse" href="#'+ str(unistr)+'">'+ news_title +'</a></strong>'+\
            '       <div class="collapse" id="'+ str(unistr) +'">'+ news_content +'<br /><br /></div>'+\
            '    </div>'+\
            '    <div class="'+ bsclass +' col-sm-1 col-xs-1 d-sm-block"></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 d-none d-md-block"></div>'+\
            '</div>'
            i += 1

        cr.close()
        connection.close()

        r = newsrow

    except Exception as e: print(e)
    return r
