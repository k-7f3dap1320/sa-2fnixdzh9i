""" Numerical functions """
import sys
import os
from pathlib import Path
import numpy as np
import math as math
from math import exp, expm1
from sa_db import *

access_obj = sa_db_access()
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

import pymysql.cursors

def get_pct_change(ini_val,new_val):
    """ xxx """
    if not new_val == 0:
        if new_val < ini_val:
            return_data =  ( (ini_val - new_val) / ini_val ) * (-1)
        else:
            return_data = (new_val - ini_val) / new_val
    else:
        return_data = 0

    return return_data


def get_stdev(sql):
    """ xxx """
    return_data = 0
    #sql with just one numerical value to compute standard deviation
    connection = pymysql.connect(host=db_srv, user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    cr.execute(sql)
    a = list( cr.fetchall() )
    return_data = np.std(a)
    cr.close()
    connection.close()

    return return_data

def get_volatility_risk(sql,is_portf,s):
    """ xxx """
    return_data = 0
    #sql with one numerical column to compute volatility risk
    connection = pymysql.connect(host=db_srv, user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)

    if is_portf:
        sql_i = "SELECT account_reference FROM instruments WHERE symbol='"+ s +"'"
        cr.execute(sql_i)
        rs = cr.fetchall()
        for row in rs: lp = row[0]
        cr.close()
    else:
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: lp = row[0]
        cr.close()

    stdev = get_stdev(sql)
    rp = lp - stdev
    return_data = abs( get_pct_change(lp,rp)  )
    connection.close()
    return return_data

def get_mdd(sql):
    """ xxx """
    return_data = 0
    #sql with just one numerical value to compute maximum drawdown
    connection = pymysql.connect(host=db_srv, user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    cr.execute(sql)
    rs = cr.fetchall()
    top = 0
    breset = math.pow(10,100)
    bottom = breset
    pct_dd = 0
    cur_dd = 0
    for row in rs:
        val = row[0]

        if val > top:
            top = val
            bottom = breset

        if val < bottom:
            bottom = val

        if bottom < top:
            cur_dd = abs( get_pct_change(bottom,top) )
        else:
            cur_dd = 0

        if cur_dd > pct_dd:
            pct_dd = cur_dd
    cr.close()

    return_data = pct_dd
    connection.close()
    return return_data

def get_romad(sql):
    """ xxx """
    return_data = 0
    #sql with one column as numerical value to compute return on maximum drawdown
    #ordered by date ASC
    connection = pymysql.connect(host=db_srv, user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    cr.execute(sql)
    rs = cr.fetchall()
    i = 0
    first = 0
    last = 0
    for row in rs:
        if i == 0:
            first = row[0]
        last = row[0]
        i += 1
    cr.close()

    rt = get_pct_change(first,last)
    dd = get_mdd(sql)

    return_data = rt / dd
    connection.close()
    return return_data
