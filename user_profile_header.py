""" Header with the moving tickers """
import pymysql.cursors
from app_cookie import *
from sa_func import *
from tradingview_ticker import *

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_box_user_profile_header(burl):
    """ Get the moving tickers header """
    box_content = ''
    if user_is_login() == 1:
        uid = user_get_uid()
        connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT nickname, name FROM users WHERE uid='"+ str(uid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            nickname = row[0]
            name = row[1]

        avatar_img = get_avatar(burl,60)


        box_content = '<div class="box-uhead sa-uhead-box">' +\
        '   <div class="row sa-uhead-box bg-dark">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content sa-uhead-box" style="height: 95px;">'+\
        get_tradingview_ticker(uid) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'
        cr.close()
        connection.close()
    return box_content
