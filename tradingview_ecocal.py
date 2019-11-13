""" Tradingview economic calendar """
from app_cookie import get_sa_theme

def get_tradingview_ecocal(width,height):
    """ Get tradingview economic calendar """
    return_data = ''
    #referral_id = 'smartalpha'
    theme = get_sa_theme()

    if str(width) == '0': width = '"100%"'
    if str(height) == '0': height = '"100%"'

    return_data = '' +\
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
    return return_data
