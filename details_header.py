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



def get_details_header(uid):

    cr_s = connection.cursor(pymysql.cursors.SSCursor)
    sql_s = "SELECT symbol_list.symbol, feed.short_description, feed.content, feed.badge, feed.asset_class, feed.market, symbol_list.isin FROM symbol_list "+\
    "JOIN feed ON symbol_list.symbol = feed.symbol WHERE symbol_list.uid =" + str(uid) + " LIMIT 1"
    cr_s.execute(sql_s)
    rs_s = cr_s.fetchall()
    for row in rs_s:
        symbol = row[0]
        instr_name = row[1]
        sector = row[2]
        badge = row[3]
        asset_class = row[4]
        market = row[5]
        isin = row[6]

        if len(isin)>1:
            isin = ' | ISIN: '+ str(isin)
        else:
            isin = ''

    if badge.find('-') == -1:
        badge_class = 'badge badge-success'
    else:
        badge_class = 'badge badge-danger'

    p_header = '' +\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part">'+\
    '                <div class="title"><h5>'+ instr_name +'&nbsp;<span class="'+badge_class+'">'+badge+'</span></h5></div>'+\
    '                <div class="text"><span class="desc">'+ sector + ' | ' + asset_class + market + symbol + isin +'</span></div>'+\
    '            </div>'+\
    '        </div>'

    cr_s.close()


    return p_header
