""" Strategy portfolio template/example creation """
import datetime
import pymysql.cursors
from flask import make_response, redirect
from sa_func import get_portf_suffix
from app_cookie import user_is_login
from portf_save import portf_insert_data
from portf_gen_data import generate_portfolio



from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def gen_portf_user_example(burl, acm, notstart):
    """ xxx """
    resp = make_response(redirect(burl+'genportf?step=2&notstart='+str(notstart)))
    if acm is None:
        asset_class = '%%'
    else:
        asset_class = acm

    if user_is_login() == 1:
        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol_list.uid FROM instruments "+\
        "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
        "WHERE instruments.symbol NOT LIKE '%"+\
        get_portf_suffix() +"%' AND symbol_list.disabled=0 AND "+\
        "(instruments.y1_signal > 0 ) AND (instruments.asset_class LIKE '"+\
        asset_class +"' OR instruments.market LIKE '"+\
        asset_class +"') ORDER BY instruments.volatility_risk_st ASC, "+\
        "instruments.m6_signal DESC, instruments.m3_signal DESC LIMIT 5"
        cursor.execute(sql)
        res = cursor.fetchall()
        i = 0
        for row in res:
            resp.set_cookie('portf_s_'+str(i),
                            str(row[0]),
                            expires=datetime.datetime.now() + datetime.timedelta(days=1))
            resp.set_cookie('portf_s_'+str(i)+'_conv',
                            str('weak'),
                            expires=datetime.datetime.now() + datetime.timedelta(days=1))
            resp.set_cookie('portf_s_'+str(i)+'_type',
                            str('long/short'),
                            expires=datetime.datetime.now() + datetime.timedelta(days=1))
            i += 1
        if i < 5:
            sql = "SELECT symbol_list.uid FROM instruments "+\
            "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
            "WHERE instruments.symbol NOT LIKE '%"+\
            get_portf_suffix() +"%' AND (instruments.m6_signal > 0 ) AND "+\
            "(instruments.asset_class LIKE '"+\
            asset_class +"' OR instruments.market LIKE '"+\
            asset_class +"') AND symbol_list.disabled = 0 "+\
            "ORDER BY instruments.volatility_risk_st ASC, "+\
            "instruments.m6_signal DESC, "+\
            "instruments.m3_signal DESC LIMIT 5"
            cursor.execute(sql)
            res = cursor.fetchall()
            i = 0
            for row in cursor:
                resp.set_cookie('portf_s_' + str(i),
                                str(row[0]),
                                expires=datetime.datetime.now() + datetime.timedelta(days=1))
                resp.set_cookie('portf_s_' + str(i) + '_conv',
                                str('weak'),
                                expires=datetime.datetime.now() + datetime.timedelta(days=1))
                resp.set_cookie('portf_s_' + str(i) + '_type',
                                str('long/short'),
                                expires=datetime.datetime.now() + datetime.timedelta(days=1))
                i += 1
        if i < 5:
            add_additional_asset = "FX:"
            sql = "SELECT symbol_list.uid FROM instruments "+\
            "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
            "WHERE instruments.symbol NOT LIKE '%"+\
            get_portf_suffix() +"%' AND (instruments.y1_signal > 0 ) AND "+\
            "(instruments.asset_class LIKE '"+\
            add_additional_asset +"') AND symbol_list.disabled = 0 "+\
            "ORDER BY instruments.volatility_risk_st ASC, "+\
            "instruments.m6_signal DESC, "+\
            "instruments.m3_signal DESC LIMIT 5"
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                resp.set_cookie('portf_s_' + str(i),
                                str(row[0]),
                                expires=datetime.datetime.now() + datetime.timedelta(days=1))
                resp.set_cookie('portf_s_' + str(i) + '_conv',
                                str('weak'),
                                expires=datetime.datetime.now() + datetime.timedelta(days=1))
                resp.set_cookie('portf_s_' + str(i) + '_type',
                                str('long/short'),
                                expires=datetime.datetime.now() + datetime.timedelta(days=1))
                i += 1
    return resp

def gen_portf_validate_content(burl, notstart):
    """ xxx """
    tour = '1'
    if str(notstart) == '1':
        tour = ''
    resp = make_response(redirect(burl+'?dashboard=1&tour='+str(tour)))
    portf_symbol = portf_insert_data()
    generate_portfolio(portf_symbol)
    return resp
