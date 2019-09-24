# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *
from app_stylesheet import *
from app_cookie import *
import pymysql.cursors
from sa_db import *
from sa_func import *

# to generate new user uid
#get_random_str(99)

access_obj = sa_db_access()
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def validate_email_input(burl,data):
    box_content = ''
    try:
        l_email_subject = 'Reset your password'
        l_email_content = 'Hi {name_of_user}, go to the following link to change your password: {link_to_reset_password}'
        l_email_not_found = 'Unable to find email: '+ str(data) +' in the system. Please contact us for assistance.'
        l_email_sent_notif = 'An email has been sent to your inbox with a link to reset your password. '+\
        'It might takes up to 5 minutes to receive it. Please check as well your spam folder in case it lands there :( '

        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT username, name, uid FROM users WHERE username ="'+ str(data) +'"'
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            username = row[0]
            name = row[1]
            uid = row[2]

        if data.lower() == username.lower():
            link = burl +'reset/?step=3&uid='+ str(uid)
            l_email_content = l_email_content.replace('{name_of_user}', name.title() ).replace('{link_to_reset_password}', link)
            send_email_to_queue(data,l_email_subject,l_email_content)
            box_content = ' '+\
            '<div class="box-top">' +\
            '   <div class="row">'+\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
            '               <span class="sectiont">'+ l_email_sent_notif +'</span>'+\
            '            </div>'+\
            '        </div>'+\
            '   </div>'+\
            '</div>'
        else:
            box_content = ' '+\
            '<div class="box-top">' +\
            '   <div class="row">'+\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
            '               <span class="sectiont">'+ l_email_not_found +'</span>'+\
            '            </div>'+\
            '        </div>'+\
            '   </div>'+\
            '</div>'

        cr.close()
        connection.close()

    except Exception as e: print(e)
    return box_content

def get_resetpassword_email_input(burl):
    box_content = ''
    try:
        l_reset_password = 'Reset your password'
        l_email_placeholder = 'Enter your email'

        box_content = ' '+\
        '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        '               <span class="sectiont">'+ l_reset_password +'</span>'+\
        '               <form action="'+ burl+'reset/?step=2" method="post" style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
        '                   <input type="text" id="email" name="email" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_email_placeholder +'" required>'+\
        '                   <button type="submit" class="btn btn-info btn-lg btn-block form-resetpassword-btn">' + 'Reset password' + '&nbsp;<i class="fas fa-arrow-right"></i></button>'+\
        '               </form>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content

def get_resetpassword_page(appname,burl,step,data):
    r = ''
    try:
        page_content = ''
        if step == str(2):
            page_content = validate_email_input(burl,data)
        else:
            page_content = get_resetpassword_email_input(burl)

        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl,0) + page_content + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
