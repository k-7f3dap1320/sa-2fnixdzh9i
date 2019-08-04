# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_tradingview_ticker():
    r = ''
    try:
        r = ' '+\
        '<div class="tradingview-widget-container">'+\
        ' <div class="tradingview-widget-container__widget"></div>'+\
        '  <div class="tradingview-widget-copyright">'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>'+\
        '  {'+\
        '  "symbols": ['+\
        '  {'+\
        '      "description": "",'+\
        '      "proName": "BTCUSD"'+\
        '    },'+\
        '    {'+\
        '      "description": "",'+\
        '      "proName": "EURUSD"'+\
        '    },'+\
        '    {'+\
        '      "description": "",'+\
        '      "proName": "GBPUSD"'+\
        '    },'+\
        '    {'+\
        '      "description": "",'+\
        '      "proName": "USDJPY"'+\
        '    }'+\
        '  ],'+\
        '  "colorTheme": "dark",'+\
        '  "isTransparent": true,'+\
        '  "largeChartUrl": "http://smartalphatrade.com/s/",'+\
        '  "displayMode": "adaptive",'+\
        '  "locale": "en"'+\
        '}'+\
        '  </script>'+\
        '</div>'+\
        '</div>'        
    except Exception as e: print(e)
    return r
