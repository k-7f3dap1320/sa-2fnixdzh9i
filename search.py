# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from kdb import *
access_obj = sa_db_access()
import pymysql.cursors
from head import *
from body import *
from page import *


db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_search_suggestions():


    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT search FROM feed ORDER BY search"
    cr.execute(sql)
    rs = cr.fetchall()
    s = ''

    i = 1

    for row in rs:
        search = row[0]
        if i == 1:
            s = search
        else:
            s = s + ',' + search
        i += 1

    r = s

    return r

def get_search_result(q):

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT url FROM feed WHERE search LIKE '%"+ str(q) +"%'"
    cr.execute(sql)
    rs = cr.fetchall()
    url = ''
    c = ''

    for row in rs:
        url = row[0]
        c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + str(url) + '" />') + get_body('','') )

    return c
