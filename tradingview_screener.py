""" Tradingview Screener """
from app_cookie import get_sa_theme
from sa_func import get_broker_affiliate_link, get_user_default_profile

def get_tradingview_screener(width, height):
    """ xxx """
    ret = ''
    if str(width) == '0':
        width = '100%'
    if str(height) == '0':
        height = '100%'
    market_selection = get_screener_market(get_user_default_profile())
    theme = get_sa_theme()
    url = get_broker_affiliate_link('Tradingview', 'baseurl')

    tradingview = '' +\
    '<div class="tradingview-widget-container">'+\
    '  <div class="tradingview-widget-container__widget"></div>'+\
    '  <script type="text/javascript" '+\
    'src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>'+\
    '  {'+\
    '  "width": "'+ str(width) +'",'+\
    '  "height": "'+ str(height) +'",'+\
    '  "defaultColumn": "overview",'+\
    '  "defaultScreen": "general",'+\
    '  "market": "'+ str(market_selection) +'",'+\
    '  "showToolbar": true,'+\
    '  "colorTheme": "'+ str(theme) +'",'+\
    '  "locale": "en",'+\
    '  "isTransparent": true,'+\
    '  "largeChartUrl": "'+ str(url) +'"'+\
    '}'+\
    '  </script>'+\
    '</div>'

    ret = tradingview
    return ret

def get_screener_market(market):
    """ xxx """
    ret = 'forex'

    if market == 'FX:':
        ret = 'forex'
    if market == 'US>':
        ret = 'america'
    if market == 'GB>':
        ret = 'uk'
    if market == 'DE>':
        ret = 'germany'

    return ret
