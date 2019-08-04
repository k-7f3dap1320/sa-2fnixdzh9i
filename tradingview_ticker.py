# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_tradingview_ticker(uid):
    r = ''
    ltvs = ''
    id = 0
    referral_id = 'smartalpha'
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)

        sql = "SELECT id FROM users WHERE uid='"+ str(uid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: id = row[0]

        sql ="SELECT DISTINCT "+\
        "symbol_list.tradingview "+\
        "FROM instruments "+\
        "JOIN portfolios ON instruments.symbol = portfolios.portf_symbol "+\
        "JOIN symbol_list ON portfolios.symbol = symbol_list.symbol "+\
        "WHERE owner='"+ str(id) +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        i = 1
        sep = ''
        for row in rs:
            if i == 1:
                sep = ''
            else:
                sep = ','

            ltvs = ltvs + sep + '{"description": "", "proName": "'+ str(row[0]) +'"}'
            i += 1
        r = ' '+\
        '<div class="tradingview-widget-container">'+\
        ' <div class="tradingview-widget-container__widget"></div>'+\
        '  <div class="tradingview-widget-copyright">'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>'+\
        '  {'+\
        '  "symbols": ['+\
        ltvs +\
        '  ],'+\
        '  "colorTheme": "dark",'+\
        '  "isTransparent": true,'+\
        '  "largeChartUrl": "http://smartalphatrade.com/s/",'+\
        '  "displayMode": "adaptive",'+\
        '  "locale": "en"'+\
        '  "referral_id": "'+ referral_id +'"'+\
        '}'+\
        '  </script>'+\
        '</div>'+\
        '</div>'
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r
