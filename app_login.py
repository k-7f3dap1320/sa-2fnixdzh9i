""" App login functionalities """
import datetime
import pymysql.cursors
from app_head import get_head
from app_body import get_body
from app_page import set_page
from sa_func import get_hash_string
from app_cookie import set_sa_cookie
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def user_login(usr, pwd, burl, redirect):
    """ xxx """
    content = ''
    redirect_url = burl
    date_today = datetime.datetime.now()
    dstr = date_today.strftime("%Y%m%d")
    pwd = get_hash_string(pwd)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    usr = usr.lower()
    sql = "SELECT uid FROM users WHERE username ='"+\
    str(usr) +"' AND password ='"+ str(pwd) +"' AND deactivated=0 LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    uid = ''
    for row in res:
        uid = row[0]
    sql = 'UPDATE users SET last_logon = '+ dstr +\
    ' WHERE uid ="'+ str(uid) +'"'
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

    if redirect != '':
        redirect_url = redirect
    else: redirect_url = burl +'#'

    if uid != '':
        content = set_sa_cookie(uid,
                                set_page(get_head('<meta http-equiv="refresh" content="0;URL=' +\
                                                   redirect_url +\
                                                   '" />') + get_body('', '')))
    else:
        content = set_page(get_head('<meta http-equiv="refresh" content="0;URL=' +\
                                     burl + 'signin/?err=1&redirect='+\
                                     redirect_url +'" />') + get_body('', ''))

    return content
