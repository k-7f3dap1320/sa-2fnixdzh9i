""" Tradingview interactive chart """
import pymysql.cursors
from app_cookie import get_sa_theme
from sa_func import get_broker_affiliate_link
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_tradingview_chart(suid, width, height):
    """ Get tradingview interactive chart """
    return_data = ''
    symbol = ''
    referral_id = get_broker_affiliate_link('Tradingview', 'affiliate')
    label_not_available = 'Live chart is not available for this instrument'
    theme = get_sa_theme()
    allow_symbol_change = 'true'


    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT tradingview_chart FROM symbol_list WHERE uid ='"+ str(suid) +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        symbol = row[0]

    if str(width) == '0':
        width = '"100%"'
    if str(height) == '0':
        height = '"100%"'

    if symbol != '':
        tradingview_copyright = ''+\
        '<div class="tradingview-widget-copyright">'+\
        '<a href="https://www.tradingview.com/symbols/'+ symbol +'/" rel="noopener" target="_blank">'+\
        '<span class="blue-text">'+ symbol +' Chart</span></a> by TradingView</div>'
        
        return_data = '' +\
        '<div class="tradingview-widget-container">'+\
        ' <div id="tradingview_713ab"></div>'+\
        tradingview_copyright+\
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

    cursor.close()
    connection.close()
    return return_data
