# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *

def get_tradingview_fxcross(width,height):
    r = ''
    try:
        referral_id = 'smartalpha'
        theme = get_sa_theme()
        url = 'http://smartalphatrade.com/s'

        if str(width) == '0': width = '"100%"'
        if str(height) == '0': height = '"100%"'

        r = '' +\
'<div class="tradingview-widget-container">'+\
'  <div class="tradingview-widget-container__widget"></div>'+\
'  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>'+\
'  {'+\
'  "width": '+ str(width) +','+\
'  "height": "'+ str(height) +'",'+\
'  "currencies": ['+\
'    "EUR",'+\
'    "USD",'+\
'    "JPY",'+\
'    "GBP",'+\
'    "CHF",'+\
'    "AUD",'+\
'    "CAD",'+\
'    "NZD",'+\
'    "CNY",'+\
'    "SGD",'+\
'    "RUB"'+\
'  ],'+\
'  "locale": "en",'+\
'  "largeChartUrl": "'+ str(url) +'"'+\
'}'+\
'  </script>'+\
'</div>'

    except Exception as e: print(e)
    return r
