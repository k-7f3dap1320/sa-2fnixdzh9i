
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
    return_data = ''
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
    return_data = p1 + p2 + num
    return return_data

def send_email_notification(broker,name,username):
    lang = 'en'
    new_user_welcome_subject = ''
    new_user_welcome_content = ''

    connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT new_user_welcome_subject, new_user_welcome_content FROM email_templates WHERE lang="'+ str(lang) +'"'
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        new_user_welcome_subject = row[0].replace('{fullname}', name.title() )
        new_user_welcome_content = row[1].replace('{fullname}', name.title() ).replace('{email}', username.lower() )
    cr.close()
    connection.close()

    send_email_to_queue(username,new_user_welcome_subject,new_user_welcome_content,2)
    send_email_to_queue('','A new user has been created ['+ str(broker) +']',str(name)+'; '+str(username),9)

def gen_createuser_page(uid,appname,burl,name,username,password,from_ip,broker,username_broker):
    return_data = ''
    if uid == '0':
        return_data = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( 'light',burl ) + get_font_awesome() + get_stylesheet(burl) )
        return_data = return_data + get_body( get_loading_body(), navbar(burl,0) + get_user_creation_form(burl,broker) + get_page_footer(burl) )
        return_data = set_page(return_data)
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
            broker = str(broker)
            username_broker = str(username_broker)
            sql = "INSERT INTO users(uid, name, nickname, username, password, created_on, referred_by_code, avatar_id, from_ip,lang,email_subscription,broker,username_broker) "+\
            "VALUES ('"+ str(uid) +"','"+ str(name) +"','"+ str(nickname) +"','"+ str(username) +"','"+ str(password) +"',"+\
            str(d) +", '"+ str(referred_by_code) +"', "+ str(avatar_id) +", '"+ str(from_ip) + "', '"+ str( get_lang() )  +"', 'ALL','"+\
            str(broker)+"', '"+ str(username_broker) +"' )"
            cr.execute(sql)
            connection.commit()
            return_data = set_sa_cookie(uid, set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + 'n/?step=c" />') + get_body('','') ) )
            #send_email_notification(broker,name,username)
        else:
            return_data = 'user already exists :P !'
        cr.close()
        connection.close()
    return return_data

def get_user_ip_input():
    return_data = ''
    return_data = '' +\
    '<script type="application/javascript">'+\
    '  function getIP(json) {'+\
    '    document.write("<input type=\'hidden\' value=\' ", json.ip,"\' id=\'from_ip\' name=\'from_ip\' >");'+\
    '  }'+\
    '</script>'+\
    '<script type="application/javascript" src="https://api.ipify.org?format=jsonp&callback=getIP"></script>'
    return return_data

def get_broker_signin_spec_form(broker):
    return_data = ''
    if broker is not None:
        connection = pymysql.connect(host=db_srv, user=db_usr, password=db_pwd, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT COUNT(*) FROM brokers WHERE broker_id = "'+ str(broker) +'"'
        cr.execute(sql)
        rs = cr.fetchall()
        broker_count = 0
        for row in rs: broker_count = row[0]
        cr.close()
        connection.close()

        if str(broker_count) == '1':
            l_username_placeholder = 'enter your '+ str(broker) + ' username or id'
            return_data = ' '+\
            '        <div>'+\
            '            <div>'+\
            '               <div class="input-group input-group-lg">'+\
            '                 <div class="input-group-prepend">'+\
            '                   <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fas fa-user-tie"></i></span>'+\
            '                 </div>'+\
            '                 <input type="text" id="username_broker" name="username_broker" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_username_placeholder +'" required autofocus>'+\
            '                 <input type="hidden" id="broker" name="broker" value="'+ str(broker) +'">'+\
            '               </div>'+\
            '            </div>'+\
            '        </div>'
        else:
            return_data = ' '+\
            '<script>'+\
            'window.location.replace("/");'+\
            '</script>'
    else:
        return_data = ' '+\
        '<input type="hidden" id="username_broker" name="username_broker" value="">'+\
        '<input type="hidden" id="broker" name="broker" value="">'
    return return_data


def get_user_creation_form(burl,broker):
    box_content = ''
    l_enter_name = "Enter Name"
    l_enter_email = "Enter Email"
    l_received_payment_subscription_thank_you = "We have received your payment thank you."
    l_note_user_creation_after_payment = "You are just 1 step away. Create your account."
    l_affiliate_submit_form = ''

    if broker is not None:
        l_create_broker_account = "If you do not have a trading account at "+ str(broker) + ", create one with our affilate link: "
        l_create_broker_account_btn_label = 'Create' + ' ' + str(broker) + ' ' +'account'
        uniqid = broker + '_affiliate_link'
        l_affiliate_href = go_to_url( get_broker_affiliate_link(broker) ,'link',uniqid)
        l_affiliate_submit_form = go_to_url( get_broker_affiliate_link(broker) ,'form',uniqid)
        l_create_broker_account_btn = '<a '+ l_affiliate_href + ' target="_blank" class="btn btn-success form-signin-btn" role="button">'+ l_create_broker_account_btn_label +'&nbsp;<i class="fas fa-external-link-alt"></i></a>'

    user_creation_header = ''
    if broker is None:
        user_creation_header = ' '+\
        '<div style="text-align: center;"><span class="text-success"><h2>'+ l_received_payment_subscription_thank_you +'</h2></span></div>'+\
        '<div style="text-align: center;">'+ l_note_user_creation_after_payment +'</div>'
    else:
        user_creation_header = '<div style="text-align: center;">'+ l_create_broker_account + ' '+ l_create_broker_account_btn +'</div>'

    box_content = l_affiliate_submit_form +\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded">'+\
    '     <form method="POST" action="'+ burl +'n/?uid='+ get_random_str(99)  +'" style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
    '         <div>'+\
    '            <div>'+\
    user_creation_header+\
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
    return box_content
