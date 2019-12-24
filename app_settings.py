""" App settings """
import pymysql.cursors
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_loading import get_loading_head, get_loading_body
from app_footer import get_page_footer
from app_ogp import set_ogp
from app_title import get_title
from app_metatags import get_metatags
from bootstrap import get_bootstrap
from font_awesome import get_font_awesome
from app_navbar import navbar
from googleanalytics import get_googleanalytics
from app_stylesheet import get_stylesheet
from app_cookie import theme_return_this, get_sa_theme, user_get_uid
from sa_func import get_portf_suffix, redirect_if_not_logged_in

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def save_settings(name, nickname, username, default_profile, email_subscription):
    """ xxx """
    return_data = ''
    user_uid = user_get_uid()
    if nickname is None:
        nickname = ''
    l_error_message_settings = 'Invalid data: '
    l_error_message_nickname_exists = 'Nickname "{nickname}" is already taken. Try another one.'

    if name == '':
        return_data = l_error_message_settings + ' ' + 'name'
    if nickname == '':
        return_data = return_data + ' '+ 'nickname'

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT nickname FROM users WHERE nickname="'+\
    str(nickname) +'" AND uid<>"'+ str(user_uid) +'"'
    cursor.execute(sql)
    res = cursor.fetchall()
    checknickname = ''
    for row in res:
        checknickname = row[0]
    if checknickname.lower() == nickname.lower():
        return_data = return_data +\
        ' '+ l_error_message_nickname_exists.replace('{nickname}', nickname)

    if return_data == '':
        sql = 'UPDATE users SET name="'+ str(name) +'", nickname="'+ str(nickname) +'", '+\
        'username="'+ str(username) +'", default_profile="'+ str(default_profile) +'", '+\
        'email_subscription="'+ str(email_subscription) +'" WHERE uid="'+ str(user_uid) +'"'
        cursor.execute(sql)
        connection.commit()

    cursor.close()
    connection.close()
    return return_data

def get_settings_content(burl, step, message):
    """ xxx """
    box_content = ''
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
    popup_message = ''

    user_uid = user_get_uid()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT name, nickname, username, default_profile, '+\
    'email_subscription, lang FROM users WHERE uid="'+ str(user_uid) +'"'
    cursor.execute(sql)
    res = cursor.fetchall()
    name = ''
    nickname = ''
    username_email = ''
    default_profile = ''

    for row in res:
        name = row[0]
        nickname = row[1]
        username_email = row[2]
        default_profile = row[3]
        email_subscription = row[4]

    cursor.close()
    connection.close()

    if step == str(2):
        success = 0
        if message == '':
            message = l_saved_changes
            success = 1
        popup_message = popup_after_submit(message, success)

    box_content = ' '+\
    '<div class="box-top">' +\
    popup_message +\
    '   <div class="row d-none d-sm-block">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <form name="settingsForm" id="settingsForm" method="post" action="'+\
    burl +'settings/?step=2" >'+\
    '                   <span class="sectiont"><i class="fas fa-sliders-h"></i>&nbsp;'+\
    l_profile_section +'</span><div style="height: 30px;"></div>'+\
    '                   <!--------------------- Name --------------------->'+\
    '                   <div class="input-group" style="max-width:888px">'+\
    '                       <span class="text-primary" style="width:200px;">'+\
    l_fullname +'</span><span>&nbsp;&nbsp;</span>'+\
    '                       <div class="input-group-prepend">'+\
    '                           <span class="input-group-text" id="inputGroup-sizing-lg">'+\
    '<i class="fa fa-user-alt" style="font-size: large;"></i></span>'+\
    '                       </div>'+\
    '                           <input type="text" id="name" name="name" value="'+\
    str(name) +'" class="form-control" aria-label="Large" '+\
    'aria-describedby="inputGroup-sizing-sm" placeholder="'+\
    l_fullname +'" required autofocus>'+\
    '                   </div>'+\
    '                   <!--------------------- Nickname ----------------->'+\
    '                   <div class="input-group" style="max-width:888px">'+\
    '                       <span class="text-primary" style="width:200px;">'+\
    l_nickname +'</span><span>&nbsp;&nbsp;</span>'+\
    '                       <div class="input-group-prepend">'+\
    '                           <span class="input-group-text" id="inputGroup-sizing-lg">'+\
    '<i class="fa fa-user-ninja" style="font-size: 20px;"></i></span>'+\
    '                       </div>'+\
    '                           <input type="text" id="nickname" name="nickname" value="'+\
    str(nickname) +'" class="form-control" aria-label="Large" '+\
    'aria-describedby="inputGroup-sizing-sm" placeholder="'+\
    l_nickname +'" required autofocus>'+\
    '                   </div>'+\
    '                   <!--------------------- Email -------------------->'+\
    '                   <div class="input-group" style="max-width:888px">'+\
    '                       <span class="text-primary" style="width:200px;">'+\
    l_email +'</span><span>&nbsp;&nbsp;</span>'+\
    '                       <div class="input-group-prepend">'+\
    '                           <span class="input-group-text" id="inputGroup-sizing-lg">'+\
    '<i class="fa fa-at" style="font-size: large;"></i></span>'+\
    '                       </div>'+\
    '                           <input type="email" id="username" name="username" value="'+\
    str(username_email) +'" class="form-control" aria-label="Large" '+\
    'aria-describedby="inputGroup-sizing-sm" placeholder="'+\
    l_email +'" required autofocus>'+\
    '                   </div>'+\
    '                   <div style="height: 30px;"></div>'+\
    '                   <div class="row" style="margin:0px">'+\
    '                     <!---------------- Trader: Market ---------------->'+\
    '                       <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '                          <div>'+\
    '                               <span class="text-primary">'+\
    l_market_ac +'</span><div style="height: 15px;"></div>'+\
    get_radio_button_trader_prf(default_profile) +\
    '                          </div>'+\
    '                          <div style="height: 30px;"></div>'+\
    '                       </div>'+\
    '                       <!-------------- Email Subscription -------------->'+\
    '                       <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '                           <div>'+\
    '                               <span class="text-primary">'+\
    l_email_subscr +'</span><div style="height: 15px;"></div>'+\
    get_radio_button_email_subs(email_subscription) +\
    '                           </div>'+\
    '                           <div style="height: 30px;"></div>'+\
    '                       </div>'+\
    '                   </div>'+\
    '                       <div style="height: 30px;"></div>'+\
    '                       <input type="submit" class="btn btn-info btn-lg active" '+\
    'style="max-width:888px; width: 100%" value="'+\
    l_save_btn +'">'+\
    '               </form>'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'+\
    '<div class="box">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <span class="sectiont"><i class="fas fa-key"></i>&nbsp;'+\
    l_password +'</span><div style="height: 30px;"></div>'+\
    '               <span class="text-primary" style="width:200px;">'+\
    l_password_label +'</span><span>&nbsp;&nbsp;</span>'+\
    '               <a href="'+\
    burl +'reset/?password" class="btn btn-primary btn-md active" role="button" '+\
    'aria-pressed="true">'+\
    l_password_btn +'</a>'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content


def get_radio_button_email_subs(selected):
    """ xxx """
    return_data = ''
    l_radio_btn_name = 'email_subscription'
    checked_radio_all = ''
    checked_radio_no = ''
    checked_radio_dir = ''
    checked_radio_prt = ''

    l_label_all_email = 'Receive all emails'
    l_label_no_email = 'Do not send any emails'
    l_label_dir_email = 'Intelligence Report (daily)'
    l_label_prt_email = 'Recommendations and tips (periodically)'

    if selected == 'ALL':
        checked_radio_all = 'checked'
    if selected == 'NO':
        checked_radio_no = 'checked'
    if selected == 'DIR':
        checked_radio_dir = 'checked'
    if selected == 'PRT':
        checked_radio_prt = 'checked'

    return_data = ' '+\
    '<input type="radio" name="'+\
    l_radio_btn_name +'" value="ALL" '+\
    checked_radio_all +'>&nbsp;'+ str(l_label_all_email)+'<br>'+\
    '<input type="radio" name="'+\
    l_radio_btn_name +'" value="NO" '+\
    checked_radio_no +'>&nbsp;'+ str(l_label_no_email)+'<br>'+\
    '<input type="radio" name="'+\
    l_radio_btn_name +'" value="DIR" '+\
    checked_radio_dir +'>&nbsp;'+ str(l_label_dir_email)+'<br>'+\
    '<input type="radio" name="'+\
    l_radio_btn_name +'" value="PRT" '+\
    checked_radio_prt +'>&nbsp;'+ str(l_label_prt_email)+'<br>'

    return return_data

def get_radio_button_trader_prf(default_profile):
    """ xxx """
    return_data = ''
    l_market = 'market'
    l_radio_btn_name = 'default_profile'
    value = ''
    label = ''
    checked_radio = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT market_id, market_label FROM markets ORDER BY market_label'
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        value = row[0]
        label = row[1]
        checked_radio = ''
        if value.lower() == default_profile.lower():
            checked_radio = 'checked'

        return_data = return_data +\
        '<input type="radio" name="'+\
        l_radio_btn_name +'" value="'+\
        str(value) +'" '+\
        checked_radio +'>&nbsp;'+\
        str(label) +'&nbsp;'+\
        l_market +'<br>'

    sql = 'SELECT asset_class_id, asset_class_name FROM asset_class '+\
    'WHERE asset_class_id<>"'+\
    get_portf_suffix() +'" AND asset_class_id<>"MA:" ORDER BY asset_class_name'
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        value = row[0]
        label = row[1]
        checked_radio = ''
        if value.lower() == default_profile.lower():
            checked_radio = 'checked'

        return_data = return_data +\
        '<input type="radio" name="'+\
        l_radio_btn_name +'" value="'+ str(value) +'" '+\
        checked_radio +'>&nbsp;'+ str(label)+'<br>'

    cursor.close()
    connection.close()
    return return_data

def popup_after_submit(message, result):
    """ xxx """
    #if result == 1: success else: error
    return_data = ''
    l_content = '<i class="fas fa-exclamation-circle"></i>&nbsp;'+ str(message)
    l_class = ''
    l_class_error = 'alert alert-danger'
    l_class_success = 'alert alert-success'
    if result == 1:
        l_class = l_class_success
    else:
        l_class = l_class_error

    return_data = ''+\
    '<div class="'+ l_class +'" role="alert">' +\
    '  <strong>'+ l_content +'</strong><br>'+\
    '</div><div>&nbsp;</div>'
    return return_data

def get_settings_page(appname, burl, step, message, terminal):
    """ xxx """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl, terminal) +\
                           redirect_if_not_logged_in(burl, '') +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_settings_content(burl, step, message) +\
             get_page_footer(burl, False))
    return_data = set_page(return_data)
    return return_data
