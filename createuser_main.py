# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import *
from app_head import *
from app_ogp import *
from app_footer import *
from app_metatags import *
from app_title import *
from app_body import *
from bootstrap import *
from app_loading import *
from app_stylesheet import *
from awesomplete import *
from tablesorter import *
from app_navbar import *
from font_awesome import *
from sa_func import *
import pymysql.cursors
from sa_db import *
from app_cookie import *
import datetime
import time
from googleanalytics import *

access_obj = sa_db_access()
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def set_nickname():
    p1 = ''; p2 =''; num = ''
    r = ''
    try:
        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT part_one FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: p1 = row[0]
        sql = "SELECT part_two FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: p2 = row[0]
        cr.close()
        connection.close()
        num = str( get_random_num(99) )
        r = p1 + p2 + num
    except Exception as e: print(e)
    return r


def gen_createuser_page(uid,appname,burl,name,username,password,from_ip,broker,broker_username):
    r = ''
    if uid == '0':
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl,0) + get_user_creation_form(burl,broker) + get_page_footer(burl) )
        r = set_page(r)
    else:
        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT username FROM users WHERE uid = '"+ str(uid) +"' OR username LIKE '"+ str(username) +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        check_exists = ''
        for row in rs: check_exists = row[0]
        if check_exists == '':
            name = name.lower()
            nickname = set_nickname()
            d = datetime.datetime.now() ; d = d.strftime('%Y%m%d')
            referred_by_code = get_refer_by_code()
            avatar_id = get_random_num(19)
            email_subscription = 'ALL'
            password = get_hash_string(password)
            sql = "INSERT INTO users(uid, name, nickname, username, password, created_on, referred_by_code, avatar_id, from_ip,lang,email_subscription) "+\
            "VALUES ('"+ str(uid) +"','"+ str(name) +"','"+ str(nickname) +"','"+ str(username) +"','"+ str(password) +"',"+ str(d) +", '"+ str(referred_by_code) +"', "+ str(avatar_id) +", '"+ str(from_ip) + "', '"+ str( get_lang() )  +"', 'ALL' )"
            cr.execute(sql)
            connection.commit()
            r = set_sa_cookie(uid, set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + 'n/?step=a" />') + get_body('','') ) )
        else:
            r = 'user already exists :P !'
        cr.close()
        connection.close()
    return r

def get_user_ip_input():
    r = ''
    try:
        r = '' +\
        '<script type="application/javascript">'+\
        '  function getIP(json) {'+\
        '    document.write("<input type=\'hidden\' value=\' ", json.ip,"\' id=\'from_ip\' name=\'from_ip\' >");'+\
        '  }'+\
        '</script>'+\
        '<script type="application/javascript" src="https://api.ipify.org?format=jsonp&callback=getIP"></script>'

    except Exception as e:
        print(e)
    return r


def get_broker_signin_spec_form(broker):
    r = ''
    try:
        if broker is not None:
            l_username_placeholder = 'enter your '+ str(broker) + ' username'
            broker_input_name_id = 'username_' + str(broker).lower()
            r = ' '+\
            '        <div>'+\
            '            <div>'+\
            '               <div class="input-group input-group-lg">'+\
            '                 <div class="input-group-prepend">'+\
            '                   <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fas fa-user-tie"></i></span>'+\
            '                 </div>'+\
            '                 <input type="text" id="'+ broker_input_name_id +'" name="'+ broker_input_name_id +'" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_username_placeholder +'" required autofocus>'+\
            '               </div>'+\
            '            </div>'+\
            '        </div>'

    except Exception as e: print(e)
    return r


def get_user_creation_form(burl,broker):

    box_content = ''

    try:
        l_enter_name = "Enter Name"
        l_enter_email = "Enter Email"
        l_received_payment_subscription_thank_you = "We have received your payment thank you."
        l_note_user_creation_after_payment = "You are just 1 step away. Create your account."

        payment_completed_header = broker
        if broker is None:
            payment_completed_header = ' '+\
            '<div style="text-align: center;"><span class="text-success"><h2>'+ l_received_payment_subscription_thank_you +'</h2></span></div>'+\
            '<div style="text-align: center;">'+ l_note_user_creation_after_payment +'</div>'

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded">'+\
        '     <form method="POST" action="'+ burl +'n/?uid='+ get_random_str(99)  +'" style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
        '         <div>'+\
        '            <div>'+\
        payment_completed_header+\
        '                <hr>'+\
        '            </div>'+\
        '        </div>'+\
        get_broker_signin_spec_form(broker) +\
        '        <div>'+\
        '            <div>'+\
        '               <div class="input-group input-group-lg">'+\
        '                 <div class="input-group-prepend">'+\
        '                   <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-user-alt" style="font-size: large;"></i></span>'+\
        '                 </div>'+\
        '                 <input type="text" id="name" name="name" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_enter_name +'" required autofocus>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '               <div class="input-group input-group-lg">'+\
        '                 <div class="input-group-prepend">'+\
        '                   <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-at" style="font-size: large;"></i></span>'+\
        '                 </div>'+\
        '                 <input type="email" id="email" name="email" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_enter_email +'" required autofocus>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '               <div class="input-group input-group-lg">'+\
        '                 <div class="input-group-prepend">'+\
        '                   <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-key" style="font-size: large;"></i></span>'+\
        '                 </div>'+\
        '                 <input type="password" id="password" name="password" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="Password" required>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '                <div>&nbsp;</div>'+\
        get_user_ip_input() +\
        '                <button type="submit" class="btn btn-info btn-lg btn-block form-signin-btn">' + 'Next' + '&nbsp;<i class="fas fa-arrow-right"></i></button>'+\
        '            </div>'+\
        '        </div>'+\
        '<div class="expl" style="text-align: center;">*We respect your privacy and will never share your email address with any person or organization.</div>'+\
        '    </form>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content
