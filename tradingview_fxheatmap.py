""" Tradingview FX heatmap """
#from app_cookie import get_sa_theme

def get_tradingview_fxheatmap(width,height):
    """ Get Tradingview FX heatmap """
    return_data = ''
    referral_id = 'smartalpha'
    #theme = get_sa_theme()
    url = 'https://app.smartalphatrade.com/s'

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
