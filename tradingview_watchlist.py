""" Tradingview watchlist """
import pymysql.cursors
from sa_func import get_broker_affiliate_link, get_user_default_profile
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_tradingview_watchlist(width,height):
    """ xxx """
    if width == '0':
        width = '100%'
    if height == '0':
        height = '100%'

    ret = ''
    l_list_strategy_portfolio = 'My Strategy Portfolio'
    l_list_top_5_best_performers = 'Top 5 Best Performers'
    l_list_top_5_worst_performers = 'Top 5 Worst Performers'
    l_list_watchlist = 'Watchlist'

    url = get_broker_affiliate_link('Tradingview', 'baseurl')

    tradingview = '' +\
    '<div class="tradingview-widget-container">'+\
    '  <div class="tradingview-widget-container__widget"></div>'+\
    '  <script type="text/javascript" '+\
    'src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js" async>'+\
    '  {'+\
    '  "width": "100%",'+\
    '  "height": "100%",'+\
    '  "symbolsGroups": ['+\
    get_tradingview_list_content(l_list_strategy_portfolio,'port', False) +\
    get_tradingview_list_content(l_list_top_5_best_performers,'best', False) +\
    get_tradingview_list_content(l_list_top_5_worst_performers,'worst', False) +\
    get_tradingview_list_content(l_list_watchlist, 'watchlist', False) +\
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
    user_default_profile = get_screener_market(get_user_default_profile())
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
        sql = 'SELECT '
    elif what == 'best':
        sql = 'SELECT '
    elif what == 'worst':
        sql = 'SELECT '
    else:
        sql = 'SELECT '
    cursor.execute(sql)
    res = cursor.fetchall()

    list_content = ''+\
    '{'+\
    '  "name": "'+ str(list_name) +'",'+\
    '  "symbols": ['
    i  = 1
    sep = ''
    for row in res:
        if i != 1:
            sep = ','

        list_content = list_content +\
        sep +\
        '{'+\
        '  "name": "OANDA:SPX500USD",'+\
        '  "displayName": "S&P 500"'+\
        '}'

        i += 1

    list_content = list_content +\
    '  ]'+\
    '}'+\
    list_separator


    cursor.close()
    connection.close()

    ret = list_content
    return ret