""" Tradingview FX heatmap """
from sa_func import get_broker_affiliate_link

def get_tradingview_fxheatmap(width,height):
    """ Get Tradingview FX heatmap """
    return_data = ''
    url = get_broker_affiliate_link('Tradingview','baseurl')

    if str(width) == '0': width = '"100%"'
    if str(height) == '0': height = '"100%"'

    return_data = '' +\
    '<div class="tradingview-widget-container">'+\
    '  <div class="tradingview-widget-container__widget"></div>'+\
    '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-forex-heat-map.js" async>'+\
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
    '  "locale": "en",'+\
    '  "largeChartUrl": "'+ str(url) +'"'+\
    '}'+\
    '  </script>'+\
    '</div>'

    return return_data
