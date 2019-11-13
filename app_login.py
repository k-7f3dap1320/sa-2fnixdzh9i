""" App login functionalities """
from app_head import *; from app_body import *; from app_page import *
from sa_db import *
from sa_func import *
access_obj = sa_db_access()
import pymysql.cursors
from app_cookie import *
import datetime
import time
from datetime import timedelta
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

def user_logout(burl):
    """ xxx """
    resp = ''
    resp = make_response( redirect(burl + '?logout') )
    resp.set_cookie('user', '0')
    return resp

def user_login(usr,pwd,burl,redirect):
    """ xxx """
    content = ''
    redirectUrl = burl
    d = datetime.datetime.now()
    dstr = d.strftime("%Y%m%d")
    pwd = get_hash_string(pwd)

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    usr = usr.lower()
    sql = "SELECT uid FROM users WHERE username ='"+ str(usr) +"' AND password ='"+ str(pwd) +"' AND deactivated=0 LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    uid = ''
    for row in rs: uid = row[0]
    sql = 'UPDATE users SET last_logon = '+ dstr + ' WHERE uid ="'+ str(uid) +'"'
    cr.execute(sql)
    connection.commit()
    cr.close()
    connection.close()

    if redirect != '':
        redirectUrl = redirect
    else: redirectUrl = burl +'#'

    if not uid == '':
        content = set_sa_cookie(uid, set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + redirectUrl + '" />') + get_body('','') ) )
    else:
        content = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + 'signin/?err=1&redirect='+ redirectUrl +'" />') + get_body('','') )

    return content
