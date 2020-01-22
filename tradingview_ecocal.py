""" Tradingview economic calendar """
from app_cookie import get_sa_theme

def get_tradingview_ecocal(width, height, show_copyright):
    """ Get tradingview economic calendar """
    return_data = ''
    theme = get_sa_theme()
    tradingview_copyright = ''

    if str(width) == '0':
        width = '"100%"'
    if str(height) == '0':
        height = '"100%"'

    if str(show_copyright) == '1':
        tradingview_copyright = ''+\
        '<div class="tradingview-widget-copyright">'+\
        '<a href="https://www.tradingview.com/markets/currencies/economic-calendar/" rel="noopener" target="_blank">'+\
        '<span class="blue-text">Economic Calendar</span></a> by TradingView'+\
        '</div>'

    return_data = '' +\
    '<div class="tradingview-widget-container">'+\
    '  <div class="tradingview-widget-container__widget"></div>'+\
    tradingview_copyright+\
    '  <script type="text/javascript" '+\
    'src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>'+\
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
