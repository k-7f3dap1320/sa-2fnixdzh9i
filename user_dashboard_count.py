""" Dashboard count trade(s) of the day """
import datetime
import pymysql.cursors
from sa_func import get_user_numeric_id
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_num_orders(type_order):
    """ Get the number of orders for the day """
    return_data = 0
    query_condition = ''
    date_now = datetime.datetime.now()
    dnstr = date_now.strftime("%Y%m%d")
    i = 0

    if type_order == 'open':
        query_condition = " "+\
        "trades.entry_date = "+\
        str(dnstr) +" AND instruments.owner = '"+\
        str(get_user_numeric_id()) +"' AND status = 'active' AND "+\
        "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
        "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
        "OR (portfolios.strategy_order_type = 'long/short') ) "
    if type_order == 'pending':
        query_condition = " "+\
        "trades.expiration_date <= "+\
        str(dnstr) +" AND instruments.owner = '"+\
        str(get_user_numeric_id()) +"' AND status = 'active' AND "+\
        "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
        "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
        "OR (portfolios.strategy_order_type = 'long/short') ) "
    if type_order == 'close':
        query_condition = " "+\
        "trades.expiration_date = "+\
        str(dnstr) +" AND instruments.owner = '"+\
        str(get_user_numeric_id()) +"' AND status = 'expired' AND "+\
        "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
        "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
        "OR (portfolios.strategy_order_type = 'long/short') )"

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = ' '+\
    'SELECT '+\
    'trades.order_type, '+\
    'trades.fullname, '+\
    'trades.entry_date, '+\
    'trades.entry_price, '+\
    'trades.close_price, '+\
    'trades.expiration_date, '+\
    'trades.pnl_pct, '+\
    'trades.url, '+\
    'a_alloc.unit, '+\
    'trades.status, '+\
    'trades.uid '+\
    'FROM trades '+\
    'JOIN portfolios ON portfolios.symbol = trades.symbol '+\
    'JOIN instruments ON instruments.symbol = portfolios.portf_symbol '+\
    'JOIN instruments as a_alloc ON a_alloc.symbol = portfolios.symbol '+\
    'WHERE'+ query_condition
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        i += 1
    return_data = i
    cursor.close()
    connection.close()

    return return_data
