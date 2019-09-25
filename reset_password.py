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

access_obj = sa_db_access()
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def set_new_password(burl,data,data2):
    box_content = ''
    try:
        message_content = '<a href="'+ burl +'">Your password has been changed.</a>'
        new_password = str(data)
        user_uid = str(data2)
        user_new_uid = str( get_random_str(99) )

        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'UPDATE Users SET password = "'+ new_password +'" WHERE uid="'+ str(user_uid) +'" '
        cr.execute(sql)
        'UPDATE Users SET uid ="'+ str(user_new_uid) +'" WHERE uid="'+ str(user_uid) +'" '
        cr.execute(sql)
        connection.commit()

        cr.close()
        connection.close()

        box_content = ' '+\
        '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        '               <div class="alert alert-info" role="alert">'+ message_content +'</div>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'
    except Exception as e: print(e)
    return box_content

def change_password_form(burl,data):
    box_content = ''
    try:
        l_invalid_link_content = 'Olala invalid link :O '
        l_section_title = 'Change your password'
        l_enterpassword_placeholder = 'Enter your new password'
        l_confirmpassword_placeholder = 'Re-enter your new password'
        l_password_not_match = 'Password do not match.'
        l_password_contains_inval_char = 'Password should not contain special characters, such as ponctuation.'
        l_btn_label = 'Submit'
        user_uid = str(data)

        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT uid FROM users WHERE uid="'+ str(user_uid) +'"'
        cr.execute(sql)
        rs = cr.fetchall()
        select_uid = ''
        for row in rs: select_uid = row[0]
        print(str(select_uid)+ " ::: " + str(user_uid) )
        if select_uid == user_uid:
            validation_script = ' '+\
            '<script>'+\
            'function checkPassword() {'+\
            '  if (document.getElementById("data").value =='+\
            '    document.getElementById("repassword").value) {'+\
            '    document.getElementById("message").innerHTML = "";'+\
            '    document.getElementById("submitBtn").innerHTML = "'+ '<button type=\'submit\' class=\'btn btn-info btn-lg btn-block form-resetpassword-btn\'>' + l_btn_label + '&nbsp;<i class=\'fas fa-arrow-right\'></i></button>' +'";'+\
            '  } else {'+\
            '    document.getElementById("message").innerHTML = "<div class=\'alert alert-warning\' role=\'alert\'>'+ l_password_not_match +'</div>";'+\
            '  }'+\
            '}'+\
            'function validateForm() {'+\
            '  var password = document.forms["passwordForm"]["data"].value;'+\
            '  var repassword = document.forms["passwordForm"]["repassword"].value;'+\
            '  if (password != repassword) {'+\
            '    alert("'+ l_password_not_match +'");'+\
            '    return false;'+\
            '  }'+\
            '  if ( password.indexOf(",") > -1 ) {'+\
            '    alert("'+ l_password_contains_inval_char +'");'+\
            '    return false;'+\
            '  }'+\
            '}'+\
            '</script>'

            box_content = validation_script +\
            '<div class="box-top">' +\
            '   <div class="row">'+\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
            '               <span class="sectiont">'+ l_section_title +'</span>'+\
            '               <form name="passwordForm" id="passwordForm"  action="'+ burl+'reset/?step=4" method="post" onsubmit="return validateForm();" style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
            '                   <input type="hidden" id="data2" name="data2" value="'+ user_uid +'">'+\
            '                   <input type="password" id="data" name="data" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_enterpassword_placeholder +'" required>'+\
            '                   <input type="password" id="repassword" name="repassword" onkeyup="checkPassword();" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_confirmpassword_placeholder +'" required>'+\
            '                   <span id="message"></span>'+\
            '                   <span id="submitBtn"></span>'+\
            '               </form>'+\
            '            </div>'+\
            '        </div>'+\
            '   </div>'+\
            '</div>'
        else:
            box_content = '' +\
            '<div class="box-top">' +\
            '   <div class="row">'+\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
            '               <div class="alert alert-danger" role="alert">'+ l_invalid_link_content +'</div>'+\
            '            </div>'+\
            '        </div>'+\
            '   </div>'+\
            '</div>'

    except Exception as e: print(e)
    return box_content

def validate_email_input(burl,data):
    box_content = ''
    try:
        l_email_subject = 'Reset your password'
        l_email_content = 'Hi {name_of_user},\n go to the following link to change your password: {link_to_reset_password}'
        l_email_not_found = 'Unable to find email: '+ str(data) +' in the system. Please contact us for assistance.'
        l_email_sent_notif = 'An email has been sent to your inbox with a link to reset your password. '+\
        'It might take up to 5 minutes to receive it. Please check as well your spam folder in case it lands there :( '

        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT username, name, uid FROM users WHERE username ="'+ str(data) +'"'
        cr.execute(sql)
        rs = cr.fetchall()
        username = ''
        name = ''
        uid = ''
        for row in rs:
            username = row[0]
            name = row[1]
            uid = row[2]

        message_content = l_email_not_found
        if data.lower() == username.lower():
            link = burl +'reset/?step=3&data='+ str(uid)
            l_email_content = l_email_content.replace('{name_of_user}', name.title() ).replace('{link_to_reset_password}', link)
            send_email_to_queue(data,l_email_subject,l_email_content)
            message_content = l_email_sent_notif

        box_content = ' '+\
        '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        '               <div class="alert alert-info" role="alert">'+ message_content +'</div>'+\
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
        l_btn_label = 'Reset Password'

        box_content = ' '+\
        '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        '               <span class="sectiont">'+ l_reset_password +'</span>'+\
        '               <form action="'+ burl+'reset/?step=2" method="post" style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
        '                   <input type="text" id="data" name="data" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_email_placeholder +'" required>'+\
        '                   <button type="submit" class="btn btn-info btn-lg btn-block form-resetpassword-btn">' + l_btn_label + '&nbsp;<i class="fas fa-arrow-right"></i></button>'+\
        '               </form>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content

def get_resetpassword_page(appname,burl,step,data,data2):
    r = ''
    try:
        page_content = ''
        if step == str(2):
            page_content = validate_email_input(burl,data)
        elif step == str(3):
            page_content = change_password_form(burl,data)
        elif step == str(4):
            page_content = set_new_password(burl,data,data2)
        else:
            page_content = get_resetpassword_email_input(burl)

        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl,0) + page_content + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)
    return r
