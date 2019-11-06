
from sa_db import *
from sa_func import *
access_obj = sa_db_access()
import pymysql.cursors
import datetime
import time


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_num_orders(t):
    return_data = 0
    query_condition = ''
    dn = datetime.datetime.now(); dnstr = dn.strftime("%Y%m%d");
    i = 0

    if t == 'open':
        query_condition = " "+\
        "trades.entry_date = "+ str(dnstr) +" AND instruments.owner = '"+ str(get_user_numeric_id() ) +"' AND status = 'active' AND "+\
        "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
        "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
        "OR (portfolios.strategy_order_type = 'long/short') ) "
    if t == 'pending':
        query_condition = " "+\
        "trades.expiration_date <= "+ str(dnstr) +" AND instruments.owner = '"+ str(get_user_numeric_id() ) +"' AND status = 'active' AND "+\
        "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
        "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
        "OR (portfolios.strategy_order_type = 'long/short') ) "
    if t == 'close':
        query_condition = " "+\
        "trades.expiration_date = "+ str(dnstr) +" AND instruments.owner = '"+ str(get_user_numeric_id() ) +"' AND status = 'expired' AND "+\
        "((portfolios.strategy_order_type = 'long' AND trades.order_type = 'buy') "+\
        "OR (portfolios.strategy_order_type = 'short' AND trades.order_type = 'sell') "+\
        "OR (portfolios.strategy_order_type = 'long/short') )"

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
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
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: i +=1
    return_data = i
    cr.close()
    connection.close()

    return return_data
