""" Tradingview Screener """
from app_cookie import get_sa_theme
from sa_func import get_broker_affiliate_link, get_user_default_profile

def get_tradingview_screener(width, height, market):
    """
    Args:
        Integer: Width of the widget component. If 0, then autosize
        Integer: Height of the widget component. If 0, then autosize
        Integer: Market to load in the screener. if 0 then default user profile
                    0 = default user profile
                    1 = forex
                    2 = U.S market
                    3 = U.K market
                    4 = Germany
                    5 = crypto
    Returns:
        None
    """
    ret = ''
    if str(width) == '0':
        width = '100%'
    if str(height) == '0':
        height = '100%'
    if str(market) == '0':
        market_selection = get_screener_market(get_user_default_profile())
    else:
        market_selection = str(market)
        
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

    if market == 'FX:' or market == '1':
        ret = 'forex'
    if market == 'US>' or market == '2':
        ret = 'america'
    if market == 'GB>' or market == '3':
        ret = 'uk'
    if market == 'DE>' or market == '4':
        ret = 'germany'
    if market == 'CR:' or market == '5':
        ret = 'crypto'

    return ret
