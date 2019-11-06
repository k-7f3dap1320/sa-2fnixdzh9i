
from app_cookie import *
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_tradingview_single_ticker(suid):
    return_data = ''
    url = 'https://app.smartalphatrade.com/s/'
    symbol = ''
    referral_id = 'smartalpha'
    label_not_available = 'Indicators are not available for this instrument'
    theme = get_sa_theme()

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT tradingview FROM symbol_list WHERE uid ='"+ str(suid) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: symbol = row[0]

    if symbol != '':
        return_data = '' +\
        '<div class="tradingview-widget-container">'+\
        '  <div class="tradingview-widget-container__widget"></div>'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>'+\
        '  {'+\
        '  "symbol": "'+ symbol +'",'+\
        '  "width": "100%",'+\
        '  "colorTheme": "'+ theme +'",'+\
        '  "isTransparent": true,'+\
        '  "locale": "en",'+\
        '  "largeChartUrl": "'+ url +'"'+\
        '}'+\
        '  </script>'+\
        '</div>'
    else:
        return_data = label_not_available

    cr.close()
    connection.close()
    return return_data
