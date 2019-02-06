# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_instr_fullname(uid):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            symbol = row[0]

    except Exception as e:
        print(e)
    return r

def get_list_portf_alloc():
    r = ''
    try:
        r = '' +\
        '<ul class="list-group">'+\
        '<li class="list-group-item">Cras justo odio</li>'+\
        '<li class="list-group-item">Dapibus ac facilisis in</li>'+\
        '<li class="list-group-item">Morbi leo risus</li>'+\
        '<li class="list-group-item">Porta ac consectetur ac</li>'+\
        '<li class="list-group-item">Vestibulum at eros</li>'+\
        '</ul>'

    except Exception as e:
        print(e)
    return r

def get_box_portf_save():

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-center-content">'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


        #cr.close()
        #connection.close()

    except Exception as e: print(e)

    return box_content
