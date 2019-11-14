""" Main functions used thru the application """
import pymysql.cursors
import string
import random
from app_cookie import get_lang, user_get_uid, user_is_login
import hashlib


from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def get_hash_string(s):
    """ xxx """
    return_data = ''
    d = hashlib.md5(s.encode() )
    return_data = d.hexdigest()
    return return_data

def get_user():
    """ xxx """
    return_data = user_get_uid()
    return return_data

def get_avatar(burl,height):
    """ xxx """
    return_data = ''
    uid = user_get_uid()
    avatar_id = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT avatar_id FROM users WHERE uid = '"+ str(uid) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: avatar_id = row[0]
    if avatar_id != 0:
        return_data = '<img alt="" src="'+burl+'static/avatar/'+ str(avatar_id) +'.png" style="vertical-align: middle;border-style: none;width: '+ str(height) +'px;">'
    cr.close()
    connection.close()
    return return_data

def is_subscribed_user():
    """ xxx """
    return_data = 0
    uid = user_get_uid()
    is_subscribed = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT is_subscribed FROM users WHERE uid = '"+ str(uid) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: is_subscribed = row[0]
    return_data = is_subscribed
    return return_data

def redirect_if_not_logged_in(burl,redirect):
    """ xxx """
    return_data = ''
    if user_is_login() != 1:
        return_data = '<meta http-equiv="refresh" content="5; url='+burl+'signin/?redirect='+ redirect +'">'
    else:
        return_data = ''
    return return_data

def get_user_numeric_id():
    """ xxx """
    return_data = ''
    uid = user_get_uid()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT id FROM users WHERE uid = '"+ str(uid) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: return_data = row[0]
    cr.close()
    connection.close()
    return return_data

def get_nickname():
    """ xxx """
    return_data = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT nickname FROM users WHERE uid = '"+ get_user() +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: return_data = row[0]
    cr.close()
    connection.close()
    return return_data

def get_portf_suffix():
    """ Get portfolio suffix """
    return 'PRF:'

def get_uid(s):
    """ xxx """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT uid FROM symbol_list WHERE symbol = '"+s+"'"
    cr.execute(sql)
    rs = cr.fetchall()
    uid = 0
    for row in rs:
        uid = row[0]
    cr.close()
    connection.close()
    return uid

def get_etoro_symbol_from_uid(uid):
    """ xxx """
    return_data = 0
    etoro_symbol = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql ='SELECT etoro FROM symbol_list WHERE uid = "'+ str(uid) +'"'
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        etoro_symbol = row[0]
    return_data = etoro_symbol
    return return_data

def get_uid_from_symbol(s):
    """ xxx """
    return_data = 0
    uid = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql ='SELECT uid FROM symbol_list WHERE symbol = "'+ str(s) +'"'
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        uid = row[0]
    return_data = uid
    return return_data

def get_uid_from_tvws(tvws):
    """ xxx """
    uid = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT uid FROM symbol_list WHERE tradingview = '"+ str(tvws) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    uid = 0
    for row in rs:
        uid = row[0]
    cr.close()
    connection.close()
    return uid

def get_user_default_profile():
    """ xxx """
    return_data = ''
    user_uid = get_user()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT default_profile FROM users WHERE uid = '"+ str(user_uid) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    default_profile = ''
    for row in rs:
        default_profile = row[0]
    cr.close()
    connection.close()
    return_data = default_profile
    return return_data

def get_random_str(n):
    """ xxx """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def get_random_num(n):
    """ xxx """
    max = int(n)
    return random.randint(1,max)

def get_selected_lang():
    """ xxx """
    return get_lang()

def get_signal(uid):
    """ xxx """
    signal = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT badge FROM feed JOIN symbol_list ON symbol_list.symbol = feed.symbol "+\
    "WHERE symbol_list.uid=" + str(uid) + " AND feed.type=1 "
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        badge = row[0]

    if (badge.find('-0') == -1 and badge.find('-1') == -1 and
    badge.find('-2') == -1 and badge.find('-3') == -1 and
    badge.find('-4') == -1 and badge.find('-5') == -1 and
    badge.find('-6') == -1 and badge.find('-7') == -1 and
    badge.find('-8') == -1 and badge.find('-9') == -1) :
        signal = 'b'
    else:
        signal = 's'
    return signal

def get_elapsed_time(vminutes):
    """ xxx """
    return_data = ''
    return_data = 'now'
    if vminutes >0 and vminutes < 60: return_data = str(vminutes) + 'm ago'
    if vminutes >= 60 and vminutes < 1440: return_data = str( round(vminutes/60,0) ) + 'h ago'
    if vminutes >= 1440: return_data = str( round(vminutes/1440,0) ) + 'd ago'
    return return_data

def go_to_url(q,return_what,uniqid):
    """ xxx """
    #---------------------------------
    # q = [url to redirect]
    # return_what = 'form' = '<form id="form_id_xxx"><input type="hidden" value="'+ str(q) +'" id="q"></form>'
    # return_what = 'link' = 'href="javascript:{}" onclick="document.getElementById('form_id_xxx').submit(); return false;"'
    # uniqid = [a unique id to identify the form]
    #---------------------------------
    return_data = ''
    return_data = 'url/?q=' + str(q)

    content = ''
    if return_what == 'form':
        content = '<form id="'+ str(uniqid) +'" " action="'+ 'url/' +'" method="post" target="_blank"><input type="hidden" id="q" name="q" value="'+ str(q) +'"></form>'
    if return_what == 'link':
        content = 'href="javascript:{}" onclick="document.getElementById(\''+ str(uniqid) +'\').submit(); return false;"'
    return_data = content
    return return_data

def send_email_to_queue(send_to,email_subject,email_content,priority):
    """ xxx """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'INSERT INTO email_queue '+\
    '(from_email, from_email_displayname, send_to_email_bcc, email_subject, email_content, priority) '+\
    'VALUES ("", "", "'+ str(send_to) +'", "'+ str(email_subject) +'", "'+ str(email_content) +'",'+ str(priority) +')'
    cr.execute(sql)
    connection.commit()
    cr.close()
    connection.close()

def get_broker_affiliate_link(broker,what):
    """
    get the affiliate link or base url
    what: affiliate, baseurl
    """
    return_data = ''
    affiliate_link = ''
    baseurl = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT affiliate_link, burl FROM brokers WHERE broker_id ='"+ str(broker) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        affiliate_link = row[0]
        baseurl = row[1]
    cr.close()
    connection.close()
    if what == 'affiliate':
        return_data = affiliate_link
    else:
        return_data = baseurl
    return return_data
