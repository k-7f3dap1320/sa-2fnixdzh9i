""" App reset password module """
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
from app_cookie import theme_return_this, get_sa_theme
from sa_func import get_random_str, get_hash_string, send_email_to_queue

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def set_new_password(burl, data, data2):
    """ xxx """
    box_content = ''

    message_content = '<a href="'+\
    burl +'logout/?resetpassword">Your password has been changed.</a>'

    new_password = get_hash_string(str(data))
    user_uid = str(data2)
    user_new_uid = str(get_random_str(99))

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'UPDATE Users SET password = "'+ new_password +'" WHERE uid="'+ str(user_uid) +'" '
    cursor.execute(sql)
    sql = 'UPDATE Users SET uid ="'+ str(user_new_uid) +'" WHERE uid="'+ str(user_uid) +'" '
    cursor.execute(sql)
    connection.commit()

    cursor.close()
    connection.close()

    box_content = ' '+\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div class="alert alert-info" role="alert">'+\
    message_content +'</div>'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content

def change_password_form(burl, data):
    """ xxx """
    box_content = ''
    l_invalid_link_content = 'Olala invalid link :O '
    l_section_title = 'Change your password'
    l_enterpassword_placeholder = 'Enter your new password'
    l_confirmpassword_placeholder = 'Re-enter your new password'
    l_password_not_match = 'Password do not match.'
    l_password_minimun_not_met = 'Password must be minimum 8 characters.'
    l_btn_label = 'Submit'
    user_uid = str(data)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT uid FROM users WHERE uid="'+ str(user_uid) +'"'
    cursor.execute(sql)
    res = cursor.fetchall()
    select_uid = ''
    for row in res:
        select_uid = row[0]
    cursor.close()
    connection.close()
    if select_uid == user_uid:
        validation_script = ' '+\
        '<script>'+\
        'function checkPassword() {'+\
        '  if (document.getElementById("data").value =='+\
        '    document.getElementById("repassword").value) {'+\
        '    document.getElementById("message").innerHTML = "";'+\
        '    document.getElementById("submitBtn").innerHTML = "'+\
        '<button type=\'submit\' '+\
        'class=\'btn btn-info btn-lg btn-block form-resetpassword-btn\'>' +\
        l_btn_label + '&nbsp;<i class=\'fas fa-arrow-right\'></i></button>' +'";'+\
        '  } else {'+\
        '    document.getElementById("message").innerHTML = "'+\
        '<div class=\'alert alert-warning\' role=\'alert\'>'+\
        l_password_not_match +'</div>";'+\
        '  }'+\
        '}'+\
        'function validateForm() {'+\
        '  var password = document.forms["passwordForm"]["data"].value;'+\
        '  var repassword = document.forms["passwordForm"]["repassword"].value;'+\
        '  if (password != repassword) {'+\
        '    alert("'+ l_password_not_match +'");'+\
        '    return false;'+\
        '  }'+\
        '  if (password.length < 8) {'+\
        '    alert("'+ l_password_minimun_not_met +'");'+\
        '    return false;'+\
        '  }'+\
        '}'+\
        '</script>'

        box_content = validation_script +\
        '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content" style="'+\
        theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +\
        '">'+\
        '               <span class="sectiont">'+\
        l_section_title +'</span>'+\
        '               <form name="passwordForm" id="passwordForm"  action="'+\
        burl+'reset/?step=4" method="post" onsubmit="return validateForm();" '+\
        'style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
        '                   <input type="hidden" id="data2" '+\
        'name="data2" value="'+\
        user_uid +'">'+\
        '                   <input type="password" id="data" '+\
        'name="data" class="form-control" aria-label="Large" '+\
        'aria-describedby="inputGroup-sizing-sm" placeholder="'+\
        l_enterpassword_placeholder +'" required>'+\
        '                   <input type="password" id="repassword" '+\
        'name="repassword" onkeyup="checkPassword();" '+\
        'class="form-control" aria-label="Large" '+\
        'aria-describedby="inputGroup-sizing-sm" placeholder="'+\
        l_confirmpassword_placeholder +'" required>'+\
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
        '            <div class="box-part rounded sa-center-content" style="'+\
        theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +\
        '">'+\
        '               <div class="alert alert-danger" role="alert">'+\
        l_invalid_link_content +'</div>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'
    return box_content

def validate_email_input(burl, data):
    """ xxx """
    box_content = ''
    l_email_subject = 'Reset your password'

    l_email_content = 'Hi {name_of_user},\n go to the following link '+\
    'to change your password: {link_to_reset_password}'

    l_email_not_found = 'Unable to find email: '+\
    str(data) +' in the system. Please contact us for assistance.'

    l_email_sent_notif = 'An email has been sent to your inbox '+\
    'with a link to reset your password. '+\
    'It might take up to 5 minutes to receive it. '+\
    'Please check as well your spam folder in case it lands there :( '

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT username, name, uid FROM users WHERE username ="'+ str(data) +'"'
    cursor.execute(sql)
    res = cursor.fetchall()
    username = ''
    name = ''
    uid = ''
    for row in res:
        username = row[0]
        name = row[1]
        uid = row[2]

    message_content = l_email_not_found
    if data.lower() == username.lower():
        link = burl +'reset/?step=3&data='+ str(uid)
        l_email_content = l_email_content.replace('{name_of_user}', name.title())
        l_email_content = l_email_content.replace('{link_to_reset_password}', link)
        send_email_to_queue(data, l_email_subject, l_email_content, 0)
        message_content = l_email_sent_notif

    box_content = ' '+\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div class="alert alert-info" role="alert">'+\
    message_content +'</div>'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'

    cursor.close()
    connection.close()
    return box_content

def get_resetpassword_email_input(burl):
    """ xxx """
    box_content = ''
    l_reset_password = 'Reset your password'
    l_email_placeholder = 'Enter your email'
    l_btn_label = 'Reset Password'

    box_content = ' '+\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <span class="sectiont">'+\
    l_reset_password +'</span>'+\
    '               <form action="'+\
    burl+'reset/?step=2" method="post" '+\
    'style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
    '                   <input type="text" id="data" name="data" '+\
    'class="form-control" aria-label="Large" '+\
    'aria-describedby="inputGroup-sizing-sm" placeholder="'+\
    l_email_placeholder +'" required>'+\
    '                   <button type="submit" '+\
    'class="btn btn-info btn-lg btn-block form-resetpassword-btn">' +\
    l_btn_label + '&nbsp;<i class="fas fa-arrow-right"></i></button>'+\
    '               </form>'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content

def get_resetpassword_page(appname, burl, step, data, data2):
    """ xxx """
    return_data = ''
    page_content = ''
    if step == str(2):
        page_content = validate_email_input(burl, data)
    elif step == str(3):
        page_content = change_password_form(burl, data)
    elif step == str(4):
        page_content = set_new_password(burl, data, data2)
    else:
        page_content = get_resetpassword_email_input(burl)

    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data + get_body(get_loading_body(),
                                         navbar(burl, 0, terminal) +\
                                         page_content +\
                                         get_page_footer(burl))
    return_data = set_page(return_data)
    return return_data
