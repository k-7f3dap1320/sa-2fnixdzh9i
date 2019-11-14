""" App login functionalities """
from app_head import *; from app_body import *; from app_page import *
from sa_func import *
import pymysql.cursors
from app_cookie import *
import datetime
import time
from datetime import timedelta
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

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

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
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
