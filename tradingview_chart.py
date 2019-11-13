""" Tradingview interactive chart """
from app_cookie import *
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_tradingview_chart(suid,width,height):
    """ Get tradingview interactive chart """
    return_data = ''
    symbol = ''
    referral_id = 'smartalpha'
    label_not_available = 'Live chart is not available for this instrument'
    theme = get_sa_theme()
    allow_symbol_change = 'false'

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT tradingview_chart FROM symbol_list WHERE uid ='"+ str(suid) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: symbol = row[0]

    if str(width) == '0': width = '"100%"'
    if str(height) == '0': height = '"100%"'

    if symbol != '':
        return_data = '' +\
        '<div class="tradingview-widget-container">'+\
        ' <div id="tradingview_713ab"></div>'+\
        '<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>'+\
        '<script type="text/javascript">'+\
        'new TradingView.widget('+\
        '{'+\
        '"autosize": true,'+\
        '"width": '+ str(width) +','+\
        '"height": '+ str(height) +','+\
        '"symbol": "'+ symbol +'",'+\
        '"interval": "D",'+\
        '"timezone": "Etc/UTC",'+\
        '"theme": "'+ theme +'",'+\
        '"style": "1",'+\
        '"locale": "en",'+\
        '"toolbar_bg": "#f1f3f6",'+\
        '"enable_publishing": false,'+\
        '"save_image": false,'+\
        '"allow_symbol_change": '+ allow_symbol_change +','+\
        '"referral_id": "'+ referral_id +'",'+\
        '"container_id": "tradingview_713ab",'+\
        '"hide_side_toolbar": false,'+\
        '}'+\
        '  );'+\
        ' </script>'+\
        '</div>'
    else:
        return_data = label_not_available

    cr.close()
    connection.close()
    return return_data
