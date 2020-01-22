""" Tradingview FX heatmap """
from sa_func import get_broker_affiliate_link
from app_cookie import get_sa_theme

def get_tradingview_fxheatmap(width, height, show_copyright):
    """ Get Tradingview FX heatmap """
    return_data = ''
    tradingview_copyright = ''
    url = get_broker_affiliate_link('Tradingview', 'baseurl')
    theme = get_sa_theme()

    if str(width) == '0':
        width = '"100%"'
    if str(height) == '0':
        height = '"100%"'

    if str(show_copyright) == '1':
        tradingview_copyright = ''+\
        '<div class="tradingview-widget-copyright">'+\
        '<a href="https://www.tradingview.com/markets/currencies/forex-heat-map/" rel="noopener" target="_blank">'+\
        '<span class="blue-text">Forex Heat Map</span></a> by TradingView<'+\
        '/div>'

    return_data = '' +\
    '<div class="tradingview-widget-container">'+\
    '  <div class="tradingview-widget-container__widget"></div>'+\
    tradingview_copyright+\
    '  <script type="text/javascript" '+\
    'src="https://s3.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>'+\
    '  {'+\
    '  "width": '+ str(width) +','+\
    '  "height": '+ str(height) +','+\
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
    '  "isTransparent": true,'+\
    '  "colorTheme": "'+ theme +'",'+\
    '  "locale": "en",'+\
    '  "largeChartUrl": "'+ str(url) +'"'+\
    '}'+\
    '  </script>'+\
    '</div>'

    return return_data
