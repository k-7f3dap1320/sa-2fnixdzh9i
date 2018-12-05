# Copyright (c) 2018-present, Kahroo LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from kdb import *
access_obj = sa_db_access()
import pymysql.cursors


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
