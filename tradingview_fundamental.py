# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *


def get_tradingview_fundamental_widget(uid):
    r = '<iframe src="../fd/?uid='+ str(uid) +'" frameborder="0" width="100%" height="100%">'
    return r

def get_tradingview_fundamental(uid):
    r = ''
    url = 'http://smartalphatrade.com/s/'
    try:
        symbol = ''
        referral_id = 'smartalpha'
        label_not_available = 'Fundamental data is not available for this instrument'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT tradingview FROM symbol_list WHERE uid ='"+ str(uid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol = row[0]

        if symbol != '':
            r = '' +\
            'https://s.tradingview.com/embed-widget/financials/?locale=en#%7B%22symbol%22%3A%22'+\
            symbol+\
            '%22%2C%22colorTheme%22%3A%22light%22%2C%22isTransparent%22%3Atrue%2C%22largeChartUrl%22%3A%22'+\
            url+\
            '%2F%22%2C%22displayMode%22%3A%22regular%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A%22100%25%22%2C%22utm_source%22%3A%22smartalphatrade.com%22%2C%22utm_medium%22%3A%22widget_new%22%2C%22utm_campaign%22%3A%22financials%22%7D'
        else:
            r = label_not_available

    except Exception as e: print(e)
    return r

def get_redirect_to_tradingview_fd(uid):
    r = '<meta http-equiv="refresh" content="5; url='+ get_tradingview_fundamental(uid) +'">'
    return r


def get_tradingview_fundamental_page(uid):
    r = ''
    try:
        r = get_head( get_loading_head() + get_redirect_to_tradingview_fd(uid) )
        r = r + get_body( '' )
        r = set_page(r)
    except Exception as e: print(e)

    return r
