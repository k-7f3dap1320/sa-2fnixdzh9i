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

def save_settings(name,nickname,username,default_profile,email_subscription):
    r = ''
    try:
        user_uid = user_get_uid()
        l_error_message_settings = 'Invalid data: '
        l_error_message_nickname_exists = 'This nickname is already taken. Try another one.'

        if name == '': r= l_error_message_settings + ' ' + 'name'
        if nickname == '': r= r + ' '+ 'nickname'

        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT nickname FROM users WHERE nickname="'+ str(nickname) +'" AND uid<>"'+ str(user_uid) +'"'
        cr.execute(sql)
        rs = cr.fetchall()
        checknickname = ''
        for row in rs: checknickname = row[0]
        if checknickname.lower() == nickname.lower():
            r = r + ' '+ l_error_message_nickname_exists

        if r == '':
            sql = 'UPDATE users SET name="'+ str(name) +'", nickname="'+ str(nickname) +'", '+\
            'username="'+ str(username) +'", default_profile="'+ str(default_profile) +'", '+\
            'email_subscription="'+ str(email_subscription) +'" WHERE uid="'+ str(user_uid) +'"'
            cr.execute(sql)
            connection.commit()

        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r

def get_settings_content(burl,step,message):
    box_content = ''
    try:
        l_profile_section = 'Profile Settings'
        l_fullname = 'Fullname'
        l_nickname = 'Displayed Nickname'
        l_email = 'Email address'
        l_password = 'Password and Security'
        l_market_ac = 'Default asset class / market to show in your newsfeed'
        l_email_subscr = 'Email Subscription'
        l_password_label = 'Password'
        l_password_btn = 'Change Password'
        l_save_btn = 'Save changes'
        l_saved_changes = 'Saved changes.'
        l_cancel_link = 'Cancel'
        popup_message = ''

        user_uid = user_get_uid()

        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT name, nickname, username, default_profile, email_subscription, lang FROM users WHERE uid="'+ str(user_uid) +'"'
        cr.execute(sql)
        rs = cr.fetchall()
        name=''; nickname=''; username_email=''; default_profile='';language=''

        for row in rs:
            name = row[0]
            nickname = row[1]
            username_email = row[2]
            default_profile = row[3]
            email_subscription = row[4]
            language = row[5]

        cr.close()
        connection.close()

        if step == str(2):
            success = 0
            if message == '':
                message = l_saved_changes
                success = 1
            popup_message = popup_after_submit(message,success)

        box_content = ' '+\
        '<div class="box-top">' +\
        popup_message +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        '               <form name="settingsForm" id="settingsForm" method="post" action="'+ burl +'settings/?step=2" >'+\
        '                   <span class="sectiont"><i class="fas fa-sliders-h"></i>&nbsp;'+ l_profile_section +'</span><div style="height: 30px;"></div>'+\
        '                   <!--------------------- Name --------------------->'+\
        '                   <div class="input-group" style="max-width:888px">'+\
        '                       <span class="text-primary" style="width:200px;">'+ l_fullname +'</span><span>&nbsp;&nbsp;</span>'+\
        '                       <div class="input-group-prepend">'+\
        '                           <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-user-alt" style="font-size: large;"></i></span>'+\
        '                       </div>'+\
        '                           <input type="text" id="name" name="name" value="'+ str(name) +'" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_fullname +'" required autofocus>'+\
        '                   </div>'+\
        '                   <!--------------------- Nickname ----------------->'+\
        '                   <div class="input-group" style="max-width:888px">'+\
        '                       <span class="text-primary" style="width:200px;">'+ l_nickname +'</span><span>&nbsp;&nbsp;</span>'+\
        '                       <div class="input-group-prepend">'+\
        '                           <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-user-ninja" style="font-size: 20px;"></i></span>'+\
        '                       </div>'+\
        '                           <input type="text" id="nickname" name="nickname" value="'+ str(nickname) +'" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_nickname +'" required autofocus>'+\
        '                   </div>'+\
        '                   <!--------------------- Email -------------------->'+\
        '                   <div class="input-group" style="max-width:888px">'+\
        '                       <span class="text-primary" style="width:200px;">'+ l_email +'</span><span>&nbsp;&nbsp;</span>'+\
        '                       <div class="input-group-prepend">'+\
        '                           <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-at" style="font-size: large;"></i></span>'+\
        '                       </div>'+\
        '                           <input type="email" id="username" name="username" value="'+ str(username_email) +'" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_email +'" required autofocus>'+\
        '                   </div>'+\
        '                   <div style="height: 30px;"></div>'+\
        '                   <div class="row" style="margin:0px">'+\
        '                     <!---------------- Trader: Market ---------------->'+\
        '                       <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '                          <div>'+\
        '                               <span class="text-primary">'+ l_market_ac +'</span><div style="height: 15px;"></div>'+\
        get_radio_button_Trader_prf(default_profile) +\
        '                          </div>'+\
        '                          <div style="height: 30px;"></div>'+\
        '                       </div>'+\
        '                       <!-------------- Email Subscription -------------->'+\
        '                       <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '                           <div>'+\
        '                               <span class="text-primary">'+ l_email_subscr +'</span><div style="height: 15px;"></div>'+\
        get_radio_button_email_subs(email_subscription) +\
        '                           </div>'+\
        '                           <div style="height: 30px;"></div>'+\
        '                       </div>'+\
        '                   </div>'+\
        '                       <div style="height: 30px;"></div>'+\
        '                       <span class="text-info" style="width:200px;"><a href="'+ burl +'?cancel">'+ l_cancel_link +'</a></span><span>&nbsp;&nbsp;</span>'+\
        '                       <input type="submit" class="btn btn-info btn-lg active" style="max-width:800px; width: 100%" value="'+ l_save_btn +'">'+\
        '               </form>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'+\
        '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        '               <span class="sectiont"><i class="fas fa-key"></i>&nbsp;'+ l_password +'</span><div style="height: 30px;"></div>'+\
        '               <span class="text-primary" style="width:200px;">'+ l_password_label +'</span><span>&nbsp;&nbsp;</span>'+\
        '               <a href="'+ burl +'reset/?password" class="btn btn-primary btn-md active" role="button" aria-pressed="true">'+ l_password_btn +'</a>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content


def get_radio_button_email_subs(selected):
    r = ''
    try:
        l_radioBtn_name = 'email_subscription'
        checkedRadio_all = ''
        checkedRadio_no = ''
        checkedRadio_dir = ''
        checkedRadio_prt = ''

        l_label_all_email = 'Receive all emails'
        l_label_no_email = 'Do not send any emails'
        l_label_dir_email = 'Intelligence Report (daily)'
        l_label_prt_email = 'Recommendations and tips (periodically)'

        if selected == 'ALL': checkedRadio_all ='checked'
        if selected == 'NO': checkedRadio_no ='checked'
        if selected == 'DIR': checkedRadio_dir ='checked'
        if selected == 'PRT': checkedRadio_prt ='checked'

        r = ' '+\
        '<input type="radio" name="'+ l_radioBtn_name +'" value="ALL" '+ checkedRadio_all +'>&nbsp;'+ str(l_label_all_email)+'<br>'+\
        '<input type="radio" name="'+ l_radioBtn_name +'" value="NO" '+ checkedRadio_no +'>&nbsp;'+ str(l_label_no_email)+'<br>'+\
        '<input type="radio" name="'+ l_radioBtn_name +'" value="DIR" '+ checkedRadio_dir +'>&nbsp;'+ str(l_label_dir_email)+'<br>'+\
        '<input type="radio" name="'+ l_radioBtn_name +'" value="PRT" '+ checkedRadio_prt +'>&nbsp;'+ str(l_label_prt_email)+'<br>'

    except Exception as e: print(e)
    return r

def get_radio_button_Trader_prf(default_profile):
    r = ''
    try:
        l_market = 'market'
        l_radioBtn_name = 'default_profile'
        value =''; label =''
        checkedRadio = ''

        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT market_id, market_label FROM markets ORDER BY market_label'
        print(sql)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            value = row[0]
            label = row[1]
            checkedRadio =''
            if value.lower() == default_profile.lower(): checkedRadio = 'checked'
            r = r + '<input type="radio" name="'+ l_radioBtn_name +'" value="'+ str(value) +'" '+ checkedRadio +'>&nbsp;'+ str(label) +'&nbsp;'+ l_market +'<br>'
        print(sql)
        sql = 'SELECT asset_class_id, asset_class_name FROM asset_class  WHERE asset_class_id<>"'+ get_portf_suffix() +'" AND asset_class_id<>"MA:" ORDER BY asset_class_name'
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            value = row[0]
            label = row[1]
            checkedRadio =''
            if value.lower() == default_profile.lower(): checkedRadio = 'checked'
            r = r + '<input type="radio" name="'+ l_radioBtn_name +'" value="'+ str(value) +'" '+ checkedRadio +'>&nbsp;'+ str(label)+'<br>'
        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r

def popup_after_submit(message,result):
    #if result == 1: success else: error
    r = ''
    l_content = '<i class="fas fa-exclamation-circle"></i>&nbsp;'+ str(message)
    l_class = ''
    l_class_error = 'alert alert-danger'
    l_class_success = 'alert alert-success'

    try:
        if result == 1:
            l_class = l_class_success
        else:
            l_class = l_class_error

        r = ''+\
        '<div class="'+ l_class +'" role="alert">' +\
        '  <strong>'+ l_content +'</strong><br>'+\
        '</div><div>&nbsp;</div>'

    except Exception as e: print(e)
    return r

def get_settings_page(appname,burl,step,message):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + redirect_if_not_logged_in(burl,'') + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl,0) + get_settings_content(burl,step,message) + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
