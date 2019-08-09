# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_title import *; from app_metatags import *; from bootstrap import *
from app_stylesheet import *
from sa_func import *

def get_tradingview_profile_widget(uid):
    r = '<iframe src="../ip/?uid='+ str(uid) +'" frameborder="0" width="100%" height="100%"></iframe>'
    return r

def get_tradingview_profile(uid):
    r = ''
    url = 'http://smartalphatrade.com/s'
    theme = 'light'
    try:
        symbol = ''
        referral_id = 'smartalpha'
        label_not_available = 'Instrument Profile is not available for this instrument'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT tradingview FROM symbol_list WHERE uid ='"+ str(uid) +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol = row[0]

        if symbol != '':
            r = 'https://s.tradingview.com/embed-widget/symbol-profile/?locale=en&symbol='+\
            symbol +\
            '#%7B%22width%22%3A%22100%25%22%2C%22height%22%3A%22100%25%22%2C%22colorTheme%22%3A%22'+\
            theme +\
            '%22%2C%22isTransparent%22%3Atrue%2C%22largeChartUrl%22%3A%22'+\
            url +\
            '%22%2C%22utm_source%22%3A%22www.tradingview.com%22%2C%22utm_medium%22%3A%22widget_new%22%2C%22utm_campaign%22%3A%22symbol-profile%22%7D'
        else:
            r = label_not_available

    except Exception as e: print(e)
    return r

def get_redirect_to_tradingview_ip(uid,burl):
    img = '<img src="'+ burl + 'static/loader.gif' +'?'+ get_random_str(9)+'" width="50"/>&nbsp;'
    l = img + 'Loading Instrument Profile. Mmmhh...if not, <a href="'+ get_tradingview_profile(uid) +'">click here</a>.'
    r = '<body onmouseover="document.location.href=\''+ get_tradingview_profile(uid) +'\'"><div style="width: 100%; height:100%; position:fixed; background-color:rgba(242, 241, 246, 1);"><div style="width:88%; height:88; position:absolute; left:50%; top:50%; transform: translate(-50%, -50%); font-size:small; text-align:center;">'+ l +'</div></div></body>'
    return r


def get_tradingview_profile_page(uid,burl):
    r = ''
    try:
        r = get_head( get_metatags(burl) + get_bootstrap() + get_stylesheet(burl))
        r = r + get_redirect_to_tradingview_ip(uid,burl)
        r = set_page(r)
    except Exception as e: print(e)

    return r
