# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_head import *
from app_metatags import *
from app_title import *
from app_body import *
from bootstrap import *
from google_chart import *
from app_loading import *
from app_stylesheet import *
from awesomplete import *
from app_navbar import *
from details_header import *
from signal_header import *
from signal_ta_chart import *
from signal_recomm import *

from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def gen_sign_page(uid,appname,burl):

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname FROM `symbol_list` JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
        "WHERE symbol_list.uid = " + str(uid)

    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        instfullname = row[0]

    r = get_head(  get_loading_head() + get_title( appname +' - Market intelligence - ' + instfullname ) + get_metatags() + get_bootstrap() + get_awesomplete() + get_google_chart_script() + get_stylesheet(burl) )
    r = r + get_body( get_loading_body(), navbar(burl) + '<div class="box"><div class="row">' + get_details_header(uid) + get_sign_header(uid) + get_sign_ta_chart(uid) + get_sign_recommend(uid) + '</div></div>')
    r = set_page(r)

    cr.close()

    return r
