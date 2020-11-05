""" Tradingview symbol info widget """
import pymysql.cursors
#from app_cookie import get_sa_theme

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_tradingview_chartoverview(suid):
    """ Get tradingview symbol info widget """
    return_data = ''
    symbol = ''
    label_not_available = 'Indicators are not available for this instrument'
    #theme = get_sa_theme()
    theme = 'dark'
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT tradingview FROM symbol_list WHERE uid ='"+ str(suid) +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        symbol = row[0]

    if symbol != '':
        return_data = '' +\
        '<div class="tradingview-widget-container">'+\
        '  <div id="tradingview_b336e"></div>'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>'+\
        '  <script type="text/javascript">'+\
        '  new TradingView.MediumWidget('+\
        '  {'+\
        '  "symbols": ['+\
        '    ['+\
        '      "'+ str(symbol) +'|12M"'+\
        '    ]'+\
        '  ],'+\
        '  "chartOnly": false,'+\
        '  "width": "100%",'+\
        '  "height": "100%",'+\
        '  "locale": "en",'+\
        '  "colorTheme": "'+ str(theme) +'",'+\
        '  "gridLineColor": "#2a2e39",'+\
        '  "trendLineColor": "rgba(255, 255, 255, 1)",'+\
        '  "fontColor": "#787b86",'+\
        '  "underLineColor": "rgba(55, 166, 239, 0.15)",'+\
        '  "isTransparent": true,'+\
        '  "autosize": true,'+\
        '  "container_id": "tradingview_b336e"'+\
        '}'+\
        '  );'+\
        '  </script>'+\
        '</div>'
    else:
        return_data = label_not_available
    cursor.close()
    connection.close()
    return return_data
