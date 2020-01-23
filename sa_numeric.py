""" Numerical functions """
import math
import numpy as np
import pymysql.cursors
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_pct_change(ini_val, new_val):
    """ xxx """
    if not new_val == 0:
        if new_val < ini_val:
            return_data = ((ini_val - new_val) / ini_val) * (-1)
        else:
            return_data = (new_val - ini_val) / new_val
    else:
        return_data = 0

    return return_data


def get_stdev(sql):
    """ xxx """
    return_data = 0
    #sql with just one numerical value to compute standard deviation
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    list_data = list(cursor.fetchall())
    return_data = np.std(list_data)
    cursor.close()
    connection.close()

    return return_data

def get_volatility_risk(sql, is_portf, symbol):
    """ xxx """
    return_data = 0
    #sql with one numerical column to compute volatility risk
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    if is_portf:
        sql_i = "SELECT account_reference FROM instruments WHERE symbol='"+ str(symbol) +"'"
        cursor.execute(sql_i)
        res = cursor.fetchall()
        for row in res:
            reference = row[0]
    else:
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            reference = row[0]
    cursor.close()
    connection.close()

    stdev = get_stdev(sql)
    ref_price = reference - stdev
    return_data = abs(get_pct_change(reference, ref_price))
    return return_data

def get_mdd(sql):
    """ xxx """
    return_data = 0
    #sql with just one numerical value to compute maximum drawdown
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    res = cursor.fetchall()
    top = 0
    breset = math.pow(10, 100)
    bottom = breset
    pct_dd = 0
    cur_dd = 0
    for row in res:
        val = row[0]

        if val > top:
            top = val
            bottom = breset

        if val < bottom:
            bottom = val

        if bottom < top:
            cur_dd = abs(get_pct_change(bottom, top))
        else:
            cur_dd = 0

        if cur_dd > pct_dd:
            pct_dd = cur_dd
    cursor.close()
    connection.close()

    return_data = pct_dd
    return return_data

def get_romad(sql):
    """ xxx """
    return_data = 0
    #sql with one column as numerical value to compute return on maximum drawdown
    #ordered by date ASC
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    res = cursor.fetchall()
    i = 0
    first = 0
    last = 0
    for row in res:
        if i == 0:
            first = row[0]
        last = row[0]
        i += 1
    cursor.close()
    connection.close()

    instrument_returns = get_pct_change(first, last)
    drawdown = get_mdd(sql)

    if drawdown >0:
        return_data = instrument_returns / drawdown
    else:
        return_data = 0

    return return_data
