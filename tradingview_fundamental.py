# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_tradingview_fundamental_widget(uid,height,width):
    r = ''
    try:
        theme = get_sa_theme()
        symbol = ''
        url = 'http://smartalphatrade.com/s/'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT tradingview FROM symbol_list WHERE uid ='"+ str(suid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol = row[0]

        r = ' ' +\
        '<div class="tradingview-widget-container">'+\
        '  <div class="tradingview-widget-container__widget"></div>'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-financials.js" async>'+\
        '  {'+\
        '  "symbol": "'+ symbol +'",'+\
        '  "colorTheme": "'+ theme +'",'+\
        '  "isTransparent": true,'+\
        '  "largeChartUrl": "'+ url +'",'+\
        '  "displayMode": "compact",'+\
        '  "width": '+ str(width) +','+\
        '  "height": '+ str(height) +','+\
        '  "locale": "en"'+\
        '}'+\
        '  </script>'+\
        '</div>'
        print(r)
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r
