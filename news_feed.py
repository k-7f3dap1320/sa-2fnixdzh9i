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
        lang = 'en'
        bsclass = 'col-lg-10 col-md-12'
        if show_chart == 1: bsclass = 'col-lg-5 col-md-6'


        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = ' '+\
        'SELECT short_title, short_description, url, badge, date FROM feed '+\
        'WHERE '+\
        'type=3 '+\
        'AND '+\
        'symbol LIKE "%%" '+\
        'AND '+\
        'asset_class LIKE "%%" '+\
        'AND '+\
        'lang LIKE "%'+ str(lang) +'%" '+\
        'ORDER BY date DESC, ABS(ranking) DESC LIMIT '+ str(numline)
        cr.execute(sql)
        rs = cr.fetchall()
        newsrow = ''
        for row in rs:
            unistr = get_random_str(20)
            news_title = str(row[0]) +' '+ str(row[3])
            news_content = str(row[1]) +' </ br></ br>'+ '<a href="'+ str(row[2]) +'" target="_blank">'+ str(row[2]) +'</a>'

            newsrow = newsrow +\
            '<div class="row">'+\
            '    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 d-none d-md-block"></div>'+\
            '    <div class="'+ bsclass +' col-sm-12 col-xs-12"> '+\
            '       <strong><i class="fas fa-newspaper"></i></strong>&nbsp;'+\
            '       <strong><a data-toggle="collapse" href="#'+ str(unistr)+'">'+ news_title +'</a></strong>'+\
            '       <div class="collapse" id="'+ str(unistr)+str(i) +'">'+ news_content +'</div>'+\
            '    </div>'+\
            '    <div class="'+ bsclass +' col-sm-1 col-xs-1 d-sm-block"></div>'+\
            '    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 d-none d-md-block"></div>'+\
            '</div>'

        cr.close()
        connection.close()

        r = newsrow

    except Exception as e: print(e)
    return r
