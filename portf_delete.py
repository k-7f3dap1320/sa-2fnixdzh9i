# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import make_response, redirect
from sa_db import sa_db_access
access_obj = sa_db_access()
import pymysql.cursors
from sa_func import get_user_numeric_id


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def del_portf(this,burl,x,dashboard):
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
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
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
