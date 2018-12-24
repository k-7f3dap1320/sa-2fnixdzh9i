# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_box_content(uid):

    box_content = ''

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol_list.uid, instruments.fullname, instruments.description "+\
        "FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
        "WHERE symbol_list.uid=" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            uid = row[0]
            fullname = row[1]
            description = row[2]

        if len(description) < 1:
            box_description = 'No description available for this instrument.'
        else:
            box_description = description

        box_title = fullname + ' profile'
        box_content = '' +\
        '        <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">'+\
        '            <div class="box-part sa-signal-alt-ord-prf">'+\
        '               <div><h6>'+ box_title + '</h6></div>'+\
        '               <div>'+ box_description +'</div>'+\
        '            </div>'+\
        '        </div>'

        cr.close()
        connection.close()

    except Exception as e: print(e)


    return box_content
