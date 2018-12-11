# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from kdb import *
access_obj = sa_db_access()
import pymysql.cursors
import string
import random


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


class app_settings:

    address = 'http://127.0.0.1'

    def get_homepage(self):
        return self.address

    def get_navbar_logo(self):
        return self.address + '/static/logo.png'

    def get_page_loader(self):
        return self.address + '/static/loader.gif'

def get_uid(s):

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT uid FROM symbol_list WHERE symbol = '"+s+"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        uid = row[0]

    return uid

def get_random_str(n):

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
