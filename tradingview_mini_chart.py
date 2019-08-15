# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_tradingview_mini_chart(suid,width,height,autosize):
    r = ''
    url = 'http://smartalphatrade.com/s/'
    try:
        symbol = ''
        referral_id = 'smartalpha'
        label_not_available = 'Symbol is not available'
        theme = 'light'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT tradingview FROM symbol_list WHERE uid ='"+ str(suid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol = row[0]

        trendLineColor = '#37a6ef'
        underLineColor = '#e3f2fd'
        if get_signal(uid)=='b':
            trendLineColor = 'rgba(106, 168, 79, 1)'
            underLineColor = 'rgba(217, 234, 211, 1)'
        else:
            trendLineColor = 'rgba(255, 0, 0, 1)'
            underLineColor = 'rgba(244, 204, 204, 1)'

        if symbol != '':
            r = '' +\
            '<div class="tradingview-widget-container">'+\
            '  <div class="tradingview-widget-container__widget"></div>'+\
            '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>'+\
            '  {'+\
            '  "symbol": "'+ symbol +'",'+\
            '  "width": "'+ width +'",'+\
            '  "height": "'+ height +'",'+\
            '  "locale": "en",'+\
            '  "dateRange": "1m",'+\
            '  "colorTheme": "'+ theme +'",'+\
            '  "trendLineColor": "'+ trendLineColor +'",'+\
            '  "underLineColor": "'+ underLineColor +'",'+\
            '  "isTransparent": true,'+\
            '  "autosize": '+ autosize +','+\
            '  "largeChartUrl": "'+ url +'"'+\
            '}'+\
            '  </script>'+\
            '</div>'
            print(r)
        else:
            r = label_not_available

        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r
