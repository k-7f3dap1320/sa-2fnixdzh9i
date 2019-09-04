# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *

def get_tradingview_ecocal(width,height):
    r = ''
    try:
        referral_id = 'smartalpha'
        theme = get_sa_theme()

        if str(width) == '0': width = '"100%"'
        if str(height) == '0': height = '"100%"'

        r = '' +\
        '<div class="tradingview-widget-container">'+\
        '  <div class="tradingview-widget-container__widget"></div>'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>'+\
        '  {'+\
        '  "colorTheme": "'+ theme +'",'+\
        '  "isTransparent": true,'+\
        '  "width": '+ width +','+\
        '  "height": '+ height +','+\
        '  "locale": "en",'+\
        '  "importanceFilter": "-1,0,1"'+\
        '}'+\
        '  </script>'+\
        '</div>'

    except Exception as e: print(e)
    return r
