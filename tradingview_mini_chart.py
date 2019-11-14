""" Tradingview mini chart """
import pymysql.cursors
from app_cookie import get_sa_theme, theme_return_this
from sa_func import get_broker_affiliate_link, get_signal

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_tradingview_mini_chart(suid,width,height,autosize,dateRange,area_chart):
    """ Get tradingview mini chart """
    return_data = ''
    url = get_broker_affiliate_link('Tradingview','baseurl')
    symbol = ''
    label_not_available = 'Symbol is not available'
    theme = get_sa_theme()
    
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT tradingview_chart FROM symbol_list WHERE uid ='"+ str(suid) +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: symbol = row[0]

    trendLineColor = '#37a6ef'
    underLineColor = '#e3f2fd'
    if get_signal(suid)=='b':
        if area_chart == 1:
            trendLineColor = theme_return_this('rgba(106, 168, 79, 1)', 'rgba(255,255,255,0.4)')
        else:
            trendLineColor = theme_return_this('rgba(217, 234, 211, 1)','rgba(102,255,51,1)')
        underLineColor = theme_return_this('rgba(217, 234, 211, 1)','rgba(102,255,51,'+ str(area_chart) +')')
    else:
        if area_chart == 1:
            trendLineColor = theme_return_this('rgba(255, 0, 0, 1)','rgba(255,255,255,0.4)')
        else:
            trendLineColor = theme_return_this('rgba(244, 204, 204, 1)','rgba(217,83,79, 1)')
        underLineColor = theme_return_this('rgba(244, 204, 204, 1)','rgba(217,83,79,'+ str(area_chart) +')')

    if symbol != '':
        return_data = '' +\
        '<div class="tradingview-widget-container">'+\
        '  <div class="tradingview-widget-container__widget"></div>'+\
        '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>'+\
        '  {'+\
        '  "symbol": "'+ symbol +'",'+\
        '  "width": "'+ width +'",'+\
        '  "height": "'+ height +'",'+\
        '  "locale": "en",'+\
        '  "dateRange": "'+dateRange+'",'+\
        '  "colorTheme": "'+ theme +'",'+\
        '  "trendLineColor": "'+ trendLineColor +'",'+\
        '  "underLineColor": "'+ underLineColor +'",'+\
        '  "isTransparent": true,'+\
        '  "autosize": '+ autosize +','+\
        '  "largeChartUrl": "'+ url +'"'+\
        '}'+\
        '  </script>'+\
        '</div>'
    else:
        return_data = label_not_available

    cr.close()
    connection.close()
    return return_data
