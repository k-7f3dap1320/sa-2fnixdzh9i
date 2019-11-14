""" Strategy portfolio delete function """
from flask import make_response, redirect
import pymysql.cursors
from sa_func import get_user_numeric_id

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def del_portf(this,burl,x,dashboard):
    """ xxx """
    #Only owner of the portfolio can delete it. to delete URL: /p/?delete={portf_id}
    if x is None: x = ''
    return_url_list = burl + 'ls/?w=portf&x='+ str(x)
    return_url_dash = burl + '?dashboard=1'

    if dashboard == '1':
        return_url = return_url_dash
    else:
        return_url = return_url_list

    portf_symbol = ''
    user_id = get_user_numeric_id()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol FROM symbol_list WHERE uid=" + str(this)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: portf_symbol = row[0]
    portf_owner = 0
    sql = "SELECT owner FROM instruments WHERE symbol = '"+ portf_symbol +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: portf_owner = row[0]

    if int(user_id) == int(portf_owner):

        sql = "DELETE FROM portfolios WHERE portf_symbol = '"+ portf_symbol +"'"; cr.execute(sql)
        sql = "DELETE FROM instruments WHERE symbol = '"+ portf_symbol +"'"; cr.execute(sql)
        sql = "DELETE FROM symbol_list WHERE symbol = '"+ portf_symbol +"'"; cr.execute(sql)
        sql = "DELETE FROM feed WHERE symbol = '"+ portf_symbol +"'"; cr.execute(sql)
        sql = "DELETE FROM chart_data WHERE symbol = '"+ portf_symbol +"'"; cr.execute(sql)
        connection.commit()
        cr.close()
        connection.close()

    resp = make_response( redirect( return_url ) )
    return resp
