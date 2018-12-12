# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
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



def get_portf_desc(uid):

    '''
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT "
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs_s:
        symbol = row[0]
    '''

    descr_box = '' +\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part">'+\
    '            </div>'+\
    '        </div>'

    return descr_box
