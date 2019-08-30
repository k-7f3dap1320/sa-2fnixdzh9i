# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_tradingview_chart(suid,width,height):
    r = ''
    try:
        symbol = ''
        referral_id = 'smartalpha'
        label_not_available = 'Live chart is not available for this instrument'
        theme = get_sa_theme()

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT tradingview FROM symbol_list WHERE uid ='"+ str(suid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol = row[0]

        if symbol != '':
            r = '' +\
            '<div class="tradingview-widget-container">'+\
            ' <div id="tradingview_713ab"></div>'+\
            '<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>'+\
            '<script type="text/javascript">'+\
            'new TradingView.widget('+\
            '{'+\
            '"autosize": true,'+\
            '"width": '+ str(width) +\
            '"height": '+ str(height) +\
            '"symbol": "'+ symbol +'",'+\
            '"interval": "D",'+\
            '"timezone": "Etc/UTC",'+\
            '"theme": "'+ theme +'",'+\
            '"style": "1",'+\
            '"locale": "en",'+\
            '"toolbar_bg": "#f1f3f6",'+\
            '"enable_publishing": false,'+\
            '"save_image": false,'+\
            '"referral_id": "'+ referral_id +'",'+\
            '"container_id": "tradingview_713ab"'+\
            '}'+\
            '  );'+\
            ' </script>'+\
            '</div>'
        else:
            r = label_not_available

        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r
