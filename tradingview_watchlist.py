""" Tradingview watchlist """
import pymysql.cursors
from sa_func import get_broker_affiliate_link, get_user_default_profile, get_user_numeric_id
from app_cookie import get_sa_theme
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_tradingview_watchlist(width, height):
    """ xxx """
    if str(width) == '0':
        width = '100%'
    if str(height) == '0':
        height = '100%'
    
    theme = get_sa_theme()
    url = get_broker_affiliate_link('Tradingview', 'baseurl')
    
    ret = ''
    l_list_strategy_portfolio = 'My Strategy Portfolio'
    l_list_top_5_best_performers = 'Top 5 Positive Movers'
    l_list_top_5_worst_performers = 'Top 5 Negative Movers'
    l_list_watchlist = 'In the Radar'

    url = get_broker_affiliate_link('Tradingview', 'baseurl')

    tradingview = '' +\
    '<div class="tradingview-widget-container">'+\
    '  <div class="tradingview-widget-container__widget"></div>'+\
    '  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js" async>'+\
    '  {'+\
    '  "colorTheme": "'+ theme +'",'+\
    '  "dateRange": "12m",'+\
    '  "showChart": true,'+\
    '  "locale": "en",'+\
    '  "width": "'+ width +'",'+\
    '  "height": "'+ height +'",'+\
    '  "largeChartUrl": "'+ url +'",'+\
    '  "isTransparent": true,'+\
    '  "plotLineColorGrowing": "rgba(25, 118, 210, 1)",'+\
    '  "plotLineColorFalling": "rgba(25, 118, 210, 1)",'+\
    '  "gridLineColor": "rgba(42, 46, 57, 1)",'+\
    '  "scaleFontColor": "rgba(120, 123, 134, 1)",'+\
    '  "belowLineFillColorGrowing": "rgba(33, 150, 243, 0.12)",'+\
    '  "belowLineFillColorFalling": "rgba(33, 150, 243, 0.12)",'+\
    '  "symbolActiveColor": "rgba(33, 150, 243, 0.12)",'+\
    '  "tabs": ['+\
    get_tradingview_list_content(l_list_strategy_portfolio, 'port', False) +\
    get_tradingview_list_content(l_list_top_5_best_performers, 'best', False) +\
    get_tradingview_list_content(l_list_top_5_worst_performers, 'worst', False) +\
    get_tradingview_list_content(l_list_watchlist, 'watchlist', True) +\
    '  ],'+\
    '  "locale": "en",'+\
    '  "largeChartUrl": "'+ str(url) +'"'+\
    '}'+\
    '  </script>'+\
    '</div>'

    ret = tradingview
    return ret

def get_tradingview_list_content(list_name, what, is_last_one):
    """
    Args:
        String: Name of the list (display as separation)
        String: list of instruments:
            port = strategy portfolio
            best = top performers
            worst = worst performers
            watchlist = list according to user's default profile
        Boolean: If True, then no comma will be added.
    Returns:
        String: list content
    """
    ret = ''
    user_default_profile = get_user_default_profile()
    user_id = get_user_numeric_id()
    if is_last_one:
        list_separator = ''
    else:
        list_separator = ','

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    if what == 'port':
        sql = 'SELECT DISTINCT symbol_list.tradingview, inst_2.fullname FROM portfolios '+\
        'JOIN instruments as inst_1 ON portfolios.portf_symbol = inst_1.symbol '+\
        'JOIN instruments as inst_2 ON  inst_2.symbol = portfolios.symbol '+\
        'JOIN symbol_list ON symbol_list.symbol = portfolios.symbol '+\
        'WHERE inst_1.owner = '+ str(user_id) +' ORDER BY ABS(inst_1.d1) DESC'
    elif what == 'best':
        sql = 'SELECT symbol_list.tradingview, instruments.fullname FROM instruments '+\
        'JOIN symbol_list ON instruments.symbol = symbol_list.symbol '+\
        'WHERE symbol_list.disabled=0 AND (instruments.asset_class LIKE "%'+ str(user_default_profile) +\
        '%" OR instruments.market LIKE "%'+ str(user_default_profile) +'%") '+\
        'ORDER BY instruments.d1 DESC LIMIT 5'
    elif what == 'worst':
        sql = 'SELECT symbol_list.tradingview, instruments.fullname FROM instruments '+\
        'JOIN symbol_list ON instruments.symbol = symbol_list.symbol '+\
        'WHERE symbol_list.disabled=0 AND (instruments.asset_class LIKE "%'+ str(user_default_profile) +\
        '%" OR instruments.market LIKE "%'+ str(user_default_profile) +'%") '+\
        'ORDER BY instruments.d1 LIMIT 5'
    else:
        sql = 'SELECT symbol_list.tradingview, instruments.fullname FROM instruments '+\
        'JOIN symbol_list ON instruments.symbol = symbol_list.symbol '+\
        'WHERE symbol_list.disabled=0 AND (instruments.asset_class LIKE "%'+ str(user_default_profile) +\
        '%" OR instruments.market LIKE "%'+ str(user_default_profile) +'%") '+\
        'ORDER BY ABS(instruments.d1) DESC LIMIT 100'


    cursor.execute(sql)
    res = cursor.fetchall()

    list_content = ''+\
    '{'+\
    '  "title": "'+ str(list_name) +'",'+\
    '  "symbols": ['
    i = 1
    sep = ''
    symbol = ''
    display_name = ''
    for row in res:
        symbol = row[0]
        display_name = row[1]
        if i != 1:
            sep = ','

        list_content = list_content +\
        sep +\
        '{'+\
        '  "s": "'+ str(symbol) +'",'+\
        '  "d": "'+ str(display_name) +'"'+\
        '}'

        i += 1

    list_content = list_content +\
    '  ],'+\
    '    "originalTitle": "'+ str(list_name) +'"'+\
    '}'+\
    list_separator


    cursor.close()
    connection.close()

    ret = list_content
    return ret
