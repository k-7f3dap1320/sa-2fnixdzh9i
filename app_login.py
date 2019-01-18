# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_title import *; from app_metatags import *; from bootstrap import *; from awesomplete import *; from font_awesome import *
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from app_cookie import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_login_form(burl):

    r = ''
    try:
        r = '' +\
        '<div class="form-signin-text"><img src="'+ burl +'static/logo.png" height="30">&nbsp;Sign In</div>'+\
        '    <form class="form-signin" method="POST" action="'+ burl+'login/' +'">'+\
        '      <label for="user" class="sr-only">Email address</label>'+\
        '      <input type="email" id="user" name="user" class="form-control btn-outline-info" placeholder="Email address" required autofocus>'+\
        '      <label for="password" class="sr-only">Password</label>'+\
        '      <input type="password" id="password" name="password" class="form-control btn-outline-info" placeholder="Password" required>'+\
        '      <button class="btn btn-lg btn-info btn-block form-signin-btn" type="submit">Login</button>'+\
        '    </form>'
    except Exception as e: print(e)
    return r

def get_signin_content(burl):

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        get_login_form(burl) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content

def get_signin_page(appname,burl,err):
    r = ''
    try:
        r = get_head( get_loading_head() + get_title( appname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_signin_content(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r


def user_logout(burl):

    resp = ''
    try:
        resp = make_response( redirect("/") )
        resp.set_cookie('user', '0')
    except Exception as e: print(e)

    return resp


def user_login(usr,pwd,burl):

    c = ''

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        usr = usr.lower()
        sql = "SELECT uid FROM users WHERE username ='"+ str(usr) +"' AND password ='"+ str(pwd) +"' LIMIT 1"
        print(sql)
        cr.execute(sql)
        rs = cr.fetchall()
        uid = ''
        for row in rs: uid = row[0]
        cr.close()
        connection.close()

        if not uid == '':
            c = set_sa_cookie(uid, set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + '" />') + get_body('','') ) )
        else:
            c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + 'signin/" />') + get_body('','') )

    except Exception as e: print(e)

    return c
