# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
from sa_db import *
import time
from datetime import timedelta
from sa_numeric import *

access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def get_pct_from_date(d, sql_select, lp):
    pct = 0
    pp = 0
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = sql_select + "AND date <= '"+ str(d) +"' ORDER BY date DESC LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        pp = row[0]
    cr.close()
    connection.close()

    if pp != 0:
        pct = ( (lp - pp) / pp)
    return pct


class instr_sum_data:
    s = ""
    uid = ""
    sql_select = ""
    sql_select_signal = ""
    ld = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Yp = datetime.datetime(2000, 1, 1, 1, 1)
    d_6Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_3Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wf = datetime.datetime(2000, 1, 1, 1, 1)
    lp = 0
    lp_signal = 0

    def __init__(self,symbol,uid):
        self.s = symbol
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol from symbol_list WHERE uid=" + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol_is_portf = row[0]
        if symbol_is_portf.find( get_portf_suffix() ) > -1 :
            self.sql_select = "SELECT price_close, date FROM chart_data WHERE symbol='"+ self.s +"' "
        else:
            self.sql_select = "SELECT price_close, date FROM price_instruments_data WHERE symbol='"+ self.s + "' "
            self.sql_select_signal = "SELECT signal_price, date from chart_data WHERE symbol='"+ self.s +"' AND forecast = 0 "
            sql = self.sql_select_signal+" ORDER BY Date DESC LIMIT 1"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: self.lp_signal = row[0];


        sql = self.sql_select+" ORDER BY Date DESC LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: self.lp = row[0]; self.ld = row[1]
        cr.close()
        connection.close()

        self.uid = uid
        self.d_1Yp = self.ld - ( timedelta(days=365) )
        self.d_6Mp = self.ld - ( timedelta(days=180) )
        self.d_3Mp = self.ld - ( timedelta(days=90) )
        self.d_1Mp = self.ld - ( timedelta(days=30) )
        self.d_1Wp = self.ld - ( timedelta(days=7) )
        self.d_1Wf = 0

    def get_uid(self):
        return self.uid

    def get_lp(self):
        return self.lp

    def get_ticker(self):
        return self.s

    def get_pct_1Yp(self):
        str_date = self.d_1Yp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_6Mp(self):
        str_date = self.d_6Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_3Mp(self):
        str_date = self.d_3Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Mp(self):
        str_date = self.d_1Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Wp(self):
        str_date = self.d_1Wp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Yp_signal(self):
        str_date = self.d_1Yp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_6Mp_signal(self):
        str_date = self.d_6Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_3Mp_signal(self):
        str_date = self.d_3Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_1Mp_signal(self):
        str_date = self.d_1Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_1Wp_signal(self):
        str_date = self.d_1Wp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))


def get_portf_perf_summ(s,uid):
    pps = instr_sum_data(s, uid)
    y1 = pps.get_pct_1Yp(); m6 = pps.get_pct_6Mp(); m3 = pps.get_pct_3Mp(); m1 = pps.get_pct_1Mp(); w1 = pps.get_pct_1Wp()
    dm = datetime.datetime.now() - timedelta(days=30) ; dm = dm.strftime('%Y%m%d')
    sql = "SELECT price_close FROM chart_data WHERE uid="+ str(uid) +" AND date >="+ str(dm) +" ORDER BY date"
    stdev_st = get_stdev(sql)
    maximum_dd_st = get_mdd(sql)
    romad_st = get_romad(sql)
    volatility_risk_st = get_volatility_risk(sql,True,s)

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "UPDATE instruments SET y1="+ str(y1) +", m6="+ str(m6) +", m3="+ str(m3) +", m1="+ str(m1) +", w1="+ str(w1) +", "+\
    " stdev_st="+ str(stdev_st) + ", maximum_dd_st="+ str(maximum_dd_st) + ", romad_st="+ str(romad_st) + ", volatility_risk_st="+ str(volatility_risk_st) +\
    " WHERE symbol='"+ str(s)  +"' "
    cr.execute(sql)
    connection.commit()
    cr.close()
    connection.close()

def get_portf_perf(s):
    portf_symbol_suffix = get_portf_suffix()
    df = datetime.datetime.now() - timedelta(days=370)

    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol_list.symbol, symbol_list.uid, instruments.fullname, instruments.account_reference "+\
    "FROM `symbol_list` INNER JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.symbol = '"+s+"' ORDER BY symbol_list.symbol"
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        portf_symbol = row[0]
        portf_uid = row[1]
        portf_fullname = row[2]
        account_reference = row[3]

        i = 0
        j = 370
        d = df
        inserted_value = ''
        portf_nav = account_reference

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM chart_data WHERE uid = "+ str(portf_uid)
        print(sql_i)
        cr_i.execute(sql_i)
        connection.commit()
        cr_i.close()

        while (i <= j):

            d = d + timedelta(days=1)
            d_str = d.strftime("%Y%m%d")
            portf_pnl = 0
            #portf_content = ''

            #get portfolio allocations
            #for each item get the pnl
            if d < datetime.datetime.now():
                cr_c = connection.cursor(pymysql.cursors.SSCursor)
                sql_c = "SELECT price_instruments_data.pnl, portfolios.quantity, instruments.pip, "+\
                "price_instruments_data.pnl_long, price_instruments_data.pnl_short, portfolios.strategy_order_type " +\
                "FROM portfolios JOIN price_instruments_data ON portfolios.symbol = price_instruments_data.symbol "+\
                "JOIN instruments ON portfolios.symbol = instruments.symbol "+\
                "WHERE portfolios.portf_symbol = '"+ portf_symbol +"' AND date="+ d_str +" ORDER BY portfolios.portf_symbol"
                print(sql_c)

                cr_c.execute(sql_c)
                rs_c = cr_c.fetchall()

                for row in rs_c:
                    pnl_c = row[0]
                    quantity_c = row[1]
                    pip_c = row[2]
                    pnl_long_c = row[3]
                    pnl_short_c = row[4]
                    strategy_order_type_c = row[5]
                    if strategy_order_type_c == 'long/short':
                        portf_pnl = portf_pnl + (pnl_c * quantity_c * pip_c)
                    if strategy_order_type_c == 'long':
                        portf_pnl = portf_pnl + (pnl_long_c * quantity_c * pip_c)
                        if pnl_long_c == 999: portf_pnl = 0
                    if strategy_order_type_c == 'short':
                        portf_pnl = portf_pnl + (pnl_short_c * quantity_c * pip_c)
                        if pnl_short_c == 999: portf_pnl = 0
                portf_nav = round( portf_nav + portf_pnl, 2)

                if i > 0:
                    sep = ', '
                else:
                    sep = ''
                inserted_value = inserted_value + sep + "(" + str(portf_uid) + ",'"+ str(portf_symbol) +"','" + str(d_str) + "'," + str(portf_nav) + ")"
            i +=1

        try:
            cr_i = connection.cursor(pymysql.cursors.SSCursor)
            sql_i = "INSERT IGNORE INTO chart_data(uid, symbol, date, price_close) VALUES "+\
            inserted_value
            print(sql_i)
            cr_i.execute(sql_i)
            connection.commit()
            cr_i.close()
        except Exception as e: print(e)
        get_portf_perf_summ(portf_symbol, portf_uid)

    cr.close()
    connection.close()
