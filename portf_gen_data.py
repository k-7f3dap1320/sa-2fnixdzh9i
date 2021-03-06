""" Strategy portfolio content generation """
import random
import datetime
from datetime import timedelta
import pymysql.cursors
from sa_func import get_portf_suffix, get_hash_string
from sa_numeric import get_stdev, get_mdd, get_romad, get_volatility_risk

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_portf_content(user_id):
    """ xxx """
    return_data = ''
    nickname = ''
    avatar_id = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT nickname, avatar_id FROM users WHERE id="+ str(user_id)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: nickname = row[0]; avatar_id = row[1]

    return_data = '<img alt="" src="{burl}static/avatar/'+\
    str(avatar_id) +\
    '.png" style="vertical-align: middle;border-style: none;width: 30px;">'+\
    '&nbsp;<strong>'+nickname+'</strong>'

    cr.close()
    connection.close()
    return return_data

def set_portf_feed(symbol):
    """ xxx """
    feed_id = 9

    d = datetime.datetime.now()
    d = d.strftime("%Y%m%d")
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, instruments.market, instruments.w_forecast_change, instruments.w_forecast_display_info, symbol_list.uid, instruments.owner, instruments.romad_st FROM instruments "+\
    "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol = '"+ str(symbol) +"'"

    cr.execute(sql)
    rs = cr.fetchall()
    i = 0
    inserted_value = ''
    for row in rs:
        symbol = row[0]
        fullname = row[1].replace("'","")
        asset_class = row[2]
        market = row[3]
        w_forecast_display_info = row[5]
        uid = row[6]
        owner = row[7]
        romad_st = row[8]

        short_title = fullname
        short_description = symbol
        content = get_portf_content(owner)
        url = "{burl}p/?uid="+str(uid)
        ranking = str( romad_st )
        feed_type = str(feed_id)

        badge = w_forecast_display_info
        search = asset_class + market + symbol + " " + fullname
        feed_hash = get_hash_string(symbol)

        if i == 0:
            sep = ''
        else:
            sep = ','
        inserted_value = inserted_value + sep +\
        "('"+d+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+feed_type+"','"+badge+"',"+\
        "'"+search+"','"+feed_hash+"','"+asset_class+"','"+market+"')"
        i += 1
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr_i = connection.cursor(pymysql.cursors.SSCursor)
    sql_i = "DELETE FROM feed WHERE (symbol = '"+ symbol+"' AND date<='"+d+"')"
    cr_i.execute(sql_i)
    connection.commit()

    if inserted_value != '':
        sql_i = "INSERT IGNORE INTO feed"+\
        "(date, short_title, short_description, content, url,"+\
            " ranking, symbol, type, badge, "+\
        "search, hash, asset_class, market) VALUES " + inserted_value
        cr_i.execute(sql_i)
        connection.commit()
    cr_i.close()
    cr.close()
    connection.close()


def get_pct_from_date(d, sql_select, lp):
    """ xxx """
    pct = 0
    pp = 0

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

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
    """ xxx """
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
        """ xxx """
        self.s = symbol

        connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

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
            for row in rs: self.lp_signal = row[0]


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
        """ xxx """
        return self.uid

    def get_lp(self):
        """ xxx """
        return self.lp

    def get_ticker(self):
        """ xxx """
        return self.s

    def get_pct_1Yp(self):
        """ xxx """
        str_date = self.d_1Yp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_6Mp(self):
        """ xxx """
        str_date = self.d_6Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_3Mp(self):
        """ xxx """
        str_date = self.d_3Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Mp(self):
        """ xxx """
        str_date = self.d_1Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Wp(self):
        """ xxx """
        str_date = self.d_1Wp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Yp_signal(self):
        """ xxx """
        str_date = self.d_1Yp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_6Mp_signal(self):
        """ xxx """
        str_date = self.d_6Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_3Mp_signal(self):
        """ xxx """
        str_date = self.d_3Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_1Mp_signal(self):
        """ xxx """
        str_date = self.d_1Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_1Wp_signal(self):
        """ xxx """
        str_date = self.d_1Wp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))


def get_portf_perf_summ(s,uid):
    """ xxx """
    pps = instr_sum_data(s, uid)
    y1 = pps.get_pct_1Yp(); m6 = pps.get_pct_6Mp(); m3 = pps.get_pct_3Mp(); m1 = pps.get_pct_1Mp(); w1 = pps.get_pct_1Wp()
    dm = datetime.datetime.now() - timedelta(days=30) ; dm = dm.strftime('%Y%m%d')
    sql = "SELECT price_close FROM chart_data WHERE uid="+ str(uid) +" AND date >="+ str(dm) +" ORDER BY date"
    stdev_st = get_stdev(sql)
    maximum_dd_st = get_mdd(sql)
    romad_st = get_romad(sql)
    volatility_risk_st = get_volatility_risk(sql,True,s)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "UPDATE instruments SET y1="+ str(y1) +", m6="+ str(m6) +", m3="+ str(m3) +", m1="+ str(m1) +", w1="+ str(w1) +", "+\
    " stdev_st="+ str(stdev_st) + ", maximum_dd_st="+ str(maximum_dd_st) + ", romad_st="+ str(romad_st) + ", volatility_risk_st="+ str(volatility_risk_st) +\
    " WHERE symbol='"+ str(s)  +"' "
    cr.execute(sql)
    connection.commit()
    cr.close()
    connection.close()

def get_portf_perf(s):
    """ xxx """
    df = datetime.datetime.now() - timedelta(days=370)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol_list.symbol, symbol_list.uid, instruments.fullname, instruments.account_reference "+\
    "FROM `symbol_list` INNER JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.symbol = '"+s+"' ORDER BY symbol_list.symbol"
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        portf_symbol = row[0]
        portf_uid = row[1]
        account_reference = row[3]

        i = 0
        j = 370
        d = df
        inserted_value = ''
        portf_nav = account_reference

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM chart_data WHERE uid = "+ str(portf_uid)
        cr_i.execute(sql_i)
        connection.commit()
        cr_i.close()

        while (i <= j):

            d = d + timedelta(days=1)
            d_str = d.strftime("%Y%m%d")
            portf_pnl = 0

            #get portfolio allocations
            #for each item get the pnl
            if d < datetime.datetime.now():
                cr_c = connection.cursor(pymysql.cursors.SSCursor)
                sql_c = "SELECT price_instruments_data.pnl, portfolios.quantity, instruments.pip, "+\
                "price_instruments_data.pnl_long, price_instruments_data.pnl_short, portfolios.strategy_order_type " +\
                "FROM portfolios JOIN price_instruments_data ON portfolios.symbol = price_instruments_data.symbol "+\
                "JOIN instruments ON portfolios.symbol = instruments.symbol "+\
                "WHERE portfolios.portf_symbol = '"+ portf_symbol +"' AND date="+ d_str +" ORDER BY portfolios.portf_symbol"

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
                    if strategy_order_type_c == 'long' and pnl_long_c != 999:
                        portf_pnl = portf_pnl + (pnl_long_c * quantity_c * pip_c)
                    if strategy_order_type_c == 'short' and pnl_short_c != 999:
                        portf_pnl = portf_pnl + (pnl_short_c * quantity_c * pip_c)
                portf_nav = round( portf_nav + portf_pnl, 2)

                if i > 0:
                    sep = ', '
                else:
                    sep = ''
                inserted_value = inserted_value + sep + "(" + str(portf_uid) + ",'"+ str(portf_symbol) +"','" + str(d_str) + "'," + str(portf_nav) + ")"
            i +=1

        if inserted_value != '':
            cr_i = connection.cursor(pymysql.cursors.SSCursor)
            sql_i = "INSERT IGNORE INTO chart_data(uid, symbol, date, price_close) VALUES "+\
            inserted_value
            cr_i.execute(sql_i)
            connection.commit()
            cr_i.close()
            connection.close()
        get_portf_perf_summ(portf_symbol, portf_uid)
    cr.close()




class portf_data:
    """ xxx """
    portf_multip = 0
    portf_big_alloc_price = 0
    portf_total_alloc_amount = 0
    portf_account_ref = 0

    def __init__(self, portf_s):
        """ xxx """

        connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT account_reference FROM instruments WHERE symbol='"+ portf_s +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            self.portf_account_ref = row[0]
        cr.close()
        connection.close()

        connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol FROM portfolios WHERE portf_symbol = '"+ portf_s +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            cr_s = connection.cursor(pymysql.cursors.SSCursor)
            sql_s = "SELECT instruments.pip, price_instruments_data.price_close "+\
            "FROM instruments JOIN price_instruments_data ON instruments.symbol = price_instruments_data.symbol "+\
            "WHERE price_instruments_data.symbol='"+ str(row[0]) +"' "+\
            "ORDER BY price_instruments_data.date DESC LIMIT 1"
            cr_s.execute(sql_s)
            rs_s = cr_s.fetchall()
            for row in rs_s:
                pip_s = row[0]
                price_s = row[1]
                salloc = float( pip_s * price_s )
                if salloc == 0:
                    salloc == 1
                if salloc > self.portf_big_alloc_price:
                    self.portf_big_alloc_price = salloc
                self.portf_total_alloc_amount = self.portf_total_alloc_amount + salloc
            cr_s.close()
        cr.close()
        connection.close()
        if self.portf_total_alloc_amount != 0:
            self.portf_multip = self.portf_account_ref / self.portf_total_alloc_amount

    def get_quantity(self, alloc_s, alloc_coef):
        """ xxx """
        portf_reduce_risk_by = 4

        connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.pip, price_instruments_data.price_close, instruments.volatility_risk_st "+\
        "FROM instruments JOIN price_instruments_data ON instruments.symbol = price_instruments_data.symbol "+\
        "WHERE price_instruments_data.symbol='"+ alloc_s +"' "+\
        "ORDER BY price_instruments_data.date DESC LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        quantity = 0
        for row in rs:
            pip_s = row[0]
            price_s = row[1]
            volatility_risk_st = row[2]
            salloc = ( pip_s * price_s )
        cr.close()
        connection.close()

        portf_reduce_risk_by = round(volatility_risk_st * 200,0)
        if portf_reduce_risk_by < 1:
            portf_reduce_risk_by = 4

        quantity = round( (( (self.portf_big_alloc_price / salloc) * self.portf_multip ) / portf_reduce_risk_by )*alloc_coef , 2)
        if quantity < 0.01:
            quantity = 0.01

        if quantity > 1:
            quantity = int(quantity)
            if quantity == 0:
                quantity = 1

        return quantity


def get_conviction_coef(coef):
    """ xxx """
    return_data = 1.01
    if coef == 'weak':
        return_data = random.randint(3,8)
    if coef == 'neutral':
        return_data = random.randint(8,20)
    if coef == 'strong':
        return_data = random.randint(21,80)
    return_data = (return_data * 0.01) + 1
    return return_data

def get_market_conv_rate(market):
    """ xxx """
    return_data = ''

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT conv_to_usd FROM markets WHERE market_id = '"+ str(market) +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        return_data = row[0]
    cursor.close()
    connection.close()
    return return_data

def get_market_currency(market):
    """ xxx """
    return_data = ''

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT currency_code FROM markets WHERE market_id = '"+ str(market) +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        return_data = row[0]
    cursor.close()
    connection.close()
    return return_data

def get_portf_alloc(symbol):
    """ xxx """

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, symbol_list.uid, instruments.unit, instruments.market FROM instruments "+\
    "INNER JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol = '"+ str(symbol) +"' ORDER BY instruments.symbol"
    cursor.execute(sql)
    res = cursor.fetchall()

    for row in res:
        portf_symbol = row[0]
        portf_unit = row[3]
        portf_market = row[4]
        portf_currency = get_market_currency(portf_market)
        portf_forc_return = 0
        portf_perc_return = 0
        portf_nav = 0
        alloc_forc_pnl = 0

        portfd = portf_data(portf_symbol)

        cr_pf = connection.cursor(pymysql.cursors.SSCursor)
        sql_pf = "SELECT symbol, quantity, strategy_conviction FROM portfolios WHERE portf_symbol ='"+ portf_symbol +"' ORDER BY portf_symbol"
        cr_pf.execute(sql_pf)
        rs_pf = cr_pf.fetchall()
        for row in rs_pf:

            portf_item_symbol = row[0]
            portf_item_conviction = row[2]
            portf_item_conviction_coef = get_conviction_coef(portf_item_conviction)
            portf_item_quantity = portfd.get_quantity(portf_item_symbol,portf_item_conviction_coef)

            cr_p = connection.cursor(pymysql.cursors.SSCursor)
            sql_p = "SELECT price_close, date FROM price_instruments_data WHERE symbol ='"+portf_item_symbol+"' ORDER BY date DESC LIMIT 1"
            cr_p.execute(sql_p)
            rs_p = cr_p.fetchall()
            for row in rs_p:
                alloc_price = row[0]
                alloc_date = row[1]
                alloc_expiration = alloc_date + timedelta(days=7)
                alloc_expiration = alloc_expiration.strftime("%Y%m%d")
            cr_p.close()

            cr_t = connection.cursor(pymysql.cursors.SSCursor)
            sql_t = "SELECT instruments.symbol, instruments.fullname, instruments.decimal_places, "+\
            "instruments.w_forecast_change, instruments.pip, symbol_list.uid, instruments.market FROM instruments "+\
            "INNER JOIN symbol_list ON instruments.symbol = symbol_list.symbol WHERE instruments.symbol ='"+portf_item_symbol+"'"

            cr_t.execute(sql_t)
            rs_t = cr_t.fetchall()

            for row in rs_t:
                alloc_symbol = row[0]
                alloc_fullname = row[1]
                alloc_decimal_places = row[2]
                alloc_w_forecast_change = row[3]
                alloc_pip = row[4]
                alloc_market = row[6]
                if alloc_w_forecast_change >= 0:
                    alloc_entry_level_sign = '<'
                    alloc_order_type = 'buy'
                else:
                    alloc_entry_level_sign = '>'
                    alloc_order_type = 'sell'

                if portf_currency != 'USD':
                    alloc_conv_rate = 1
                else:
                    alloc_conv_rate = get_market_conv_rate(alloc_market)

                alloc_dollar_amount = round( portf_item_quantity * alloc_price * alloc_conv_rate, int(alloc_decimal_places) ) * alloc_pip
                portf_item_quantity = round(portf_item_quantity / alloc_conv_rate,2)
                if portf_item_quantity < 0.01:
                    portf_item_quantity = 0.01


                entry_level = alloc_entry_level_sign + ' ' + str( round( float(alloc_price), alloc_decimal_places) )

                cr_x = connection.cursor(pymysql.cursors.SSCursor)
                sql_x = 'UPDATE portfolios SET quantity='+ str(portf_item_quantity) +', alloc_fullname="'+ alloc_fullname +'", order_type="' + alloc_order_type + '", '+\
                'dollar_amount='+ str(alloc_dollar_amount) +', entry_level="'+ entry_level +'", expiration='+ alloc_expiration +' '+\
                'WHERE symbol ="'+ alloc_symbol+'" AND portf_symbol ="' + portf_symbol + '" '
                cr_x.execute(sql_x)
                connection.commit()
                cr_x.close()

                alloc_forc_wf = abs(alloc_w_forecast_change)

                alloc_forc_pnl = (abs(float(alloc_forc_wf) * portf_item_quantity * alloc_pip))
                portf_forc_return = portf_forc_return + alloc_forc_pnl
                portf_nav = portf_nav + alloc_dollar_amount
            cr_t.close()
        cr_pf.close()
        if portf_forc_return != 0:
            portf_perc_return = (100/(portf_nav/portf_forc_return))/100
        w_forecast_display_info = str(round(portf_perc_return,2)) +'%'
        cr_f = connection.cursor(pymysql.cursors.SSCursor)
        sql_f = "UPDATE instruments SET w_forecast_change=" + str(portf_perc_return) + ", w_forecast_display_info='" + w_forecast_display_info + "' " +\
        "WHERE symbol='"+portf_symbol+"' "
        cr_f.execute(sql_f)
        connection.commit()
        cr_f.close()
    cursor.close()
    connection.close()


def generate_portfolio(symbol):
    """ xxx """
    get_portf_alloc(symbol)
    get_portf_perf(symbol)
    set_portf_feed(symbol)
