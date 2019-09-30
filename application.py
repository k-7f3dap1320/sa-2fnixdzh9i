# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
DEV_MODE = False

from flask import Flask, request
from flask_compress import Compress
from app_main import *; from portf_main import *; from signal_main import *
from app_widget import *
from createuser_main import *; from select_avatar import *; from select_market import *
from createportf_main import *
from portf_delete import *
from app_head import *; from app_body import *; from app_page import *
from app_cookie import *
from sa_func import *
from signin_main import *
from view_list_instr_n_portf import *
from payment_page import *
from error_page import *
from portf_gen_user_example import *
from how_page import *
from tradingview_fundamental import *
from tradingview_profile import *
from intel_report import *
from set_theme import *
from app_settings import *
from app_search import *
from reset_password import *

application = Flask(__name__)

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6; COMPRESS_MIN_SIZE = 500; Compress(application)

@application.route('/')
@application.route('/s/', endpoint='s', methods=["POST", "GET"])
@application.route('/p/', endpoint='p', methods=["POST", "GET"])
@application.route('/ls/', endpoint='ls', methods=["POST", "GET"])
@application.route('/n/', endpoint='n', methods=["POST", "GET"])
@application.route('/join/', endpoint='join', methods=["POST", "GET"])
@application.route('/h/', endpoint='h', methods=["POST","GET"])
@application.route('/w/', endpoint='w', methods=["POST","GET"])
@application.route('/fd/', endpoint='fd', methods=["POST","GET"])
@application.route('/ip/', endpoint='ip', methods=["POST","GET"])
@application.route('/intelligence/', endpoint='intelligence', methods=["POST","GET"])
@application.route('/theme/', endpoint='theme', methods=["POST","GET"])
@application.route('/login/', endpoint='login', methods=["POST", "GET"])
@application.route('/logout/', endpoint='logout', methods=["POST", "GET"])
@application.route('/signin/', endpoint='signin', methods=["POST", "GET"])
@application.route('/genportf/', endpoint='genportf', methods=["POST","GET"])
@application.route('/pricing/', endpoint='pricing', methods=["POST","GET"])
@application.route('/settings/', endpoint='settings', methods=["POST","GET"])
@application.route('/reset/', endpoint='reset', methods=["POST","GET"])
@application.route('/search/', endpoint='search', methods=["POST","GET"])
@application.route('/error/', endpoint='error', methods=["POST","GET"])
@application.route('/url/', endpoint='url', methods=["POST","GET"])
@application.route('/w/url/', endpoint='url', methods=["POST","GET"])

def go():

    appname = 'SmartAlpha | Trading Intelligence'
    c = ''; burl = request.url_root;
    if not DEV_MODE: burl = burl.replace('http://','https://')

    uid = request.args.get('uid')
    ref = request.args.get('ref')
    lang = request.args.get('lang')
    theme = request.args.get('theme')
    nonavbar = request.values.get('nonavbar')
    x = request.args.get('x');


    err = request.args.get('err')

    ############################################################################
    if request.endpoint == 's':
        tvws = request.args.get('tvwidgetsymbol')
        c = gen_sign_page(uid,tvws,appname,burl)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'p':
        ins = request.values.get('ins')
        step = request.values.get('step')
        mode = request.values.get('mode')
        portf = request.values.get('portf')
        pop = request.values.get('pop')
        delete = request.values.get('delete')
        dashboard = request.values.get('dashboard')
        button = request.values.get('button')
        if ins != '' or ins != None:
            if x == '' or x == None : x = get_user_default_profile()
        if ins == '1': c = gen_selectportf_page(appname,burl,step,mode,x,portf)
        if ins == '2': c = save_portf_select(appname,burl,step,mode,x,portf,uid)
        if ins == '3': c = custom_save_portf_page(appname,burl,mode,x)
        if ins == '4': c = portf_save_conviction(burl,mode,x)
        if ins == '5': c = portf_save(appname,burl)
        if ins is None: c = gen_portf_page(uid,appname,burl,pop)
        if delete != None: c = del_portf(delete,burl,x,dashboard)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'ls':
        what = request.values.get('w')
        c = gen_view_list_instr_n_portf(appname,burl,what,x)

    elif request.endpoint == 'n':
        name = request.values.get('name')
        username = request.values.get('email')
        password = request.values.get('password')
        from_ip = request.values.get('from_ip')
        nickname = request.values.get('nickname')
        step = request.args.get('step')
        broker = request.args.get('broker')
        broker_username = request.values.get('broker_username')
        mode = request.values.get('mode')
        if step == 'a': c = gen_createuser_avatar(appname,burl,err)
        elif step == 'b': c = save_avatar(burl,nickname)
        elif step == 'c': c = gen_selectmarket_page(appname,burl,mode)
        elif step == 'd': c= save_selectmarket(burl,mode,x)
        else: c = gen_createuser_page(uid,appname,burl,name,username,password,from_ip,broker,broker_username)

    elif request.endpoint == 'join':
        broker = request.args.get('broker')
        c = gen_createuser_page('0',appname,burl,'','','','',broker)

    elif request.endpoint == 'h':
        c = get_help_page(appname,burl)

    elif request.endpoint == 'w':
        funcname = request.values.get('funcname')
        refreshw = request.values.get('refreshw')
        noflexheight = request.values.get('noflexheight')
        c = get_widget_page(appname,burl,nonavbar,funcname,refreshw,noflexheight)

    elif request.endpoint == 'fd':
        c = get_tradingview_fundamental_page(uid,burl)

    elif request.endpoint == 'ip':
        c = get_tradingview_profile_page(uid,burl)

    elif request.endpoint == 'intelligence':
        c = get_intel_page(appname,burl)

    elif request.endpoint == 'theme':
        try:
            switch_to = ''
            if get_sa_theme() == 'dark':
                switch_to = 'light'
            else:
                switch_to = 'dark'
            c = theme_redirect(burl)
            c = set_sa_theme(switch_to, c )

        except Exception as e: print(e)

    elif request.endpoint == 'login':
        user = request.values.get('user')
        password = request.values.get('password')
        redirect = request.values.get('redirect')
        c = user_login(user,password, burl, redirect)

    elif request.endpoint == 'logout':
        c = user_logout(burl)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'signin':
        redirect = request.values.get('redirect')
        c = get_signin_page(appname,burl,err,redirect)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'pricing':
        c = get_plan_selection_page(appname,burl)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'settings':
        step = request.args.get('step')
        name = request.values.get('name')
        nickname = request.values.get('nickname')
        username = request.values.get('username')
        default_profile = request.values.get('default_profile')
        email_subscription = request.values.get('email_subscription')
        message = save_settings(name,nickname,username,default_profile,email_subscription)
        c = get_settings_page(appname,burl,step,message)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'reset':
        step = request.args.get('step')
        data = request.values.get('data')
        data2 = request.values.get('data2')
        c = get_resetpassword_page(appname,burl,step,data,data2)

    elif request.endpoint == 'search':
        nonavbar = request.args.get('nonavbar')
        c = get_search_page(appname,burl,nonavbar)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'genportf':
        acm = request.args.get('acm')
        step = request.args.get('step')
        notstart = request.args.get('notstart')
        if step == '1': c = gen_portf_user_example(burl,acm,notstart)
        if step == '2': c = gen_portf_validate_content(burl,notstart)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'error':
        c = get_error_page(appname,burl)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'url':
        url_q = request.values.get('q')
        c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + str(url_q) + '" />') + get_body('','') )
    else:
        if x == '' or x == None : x = get_user_default_profile()
        dashboard = request.args.get('dashboard')
        tour = request.args.get('tour')
        c = gen_main_page(x,appname,burl,dashboard,tour,nonavbar)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)
    ############################################################################

    sid = request.args.get('sid')
    q = request.args.get(sid)
    try:
        if len(sid)>5:
            c = get_search_result(q)
    except Exception as e: print(e)


    if not DEV_MODE:
        if burl.find('https://app.') == -1:
            if burl.find('https://www.') > -1:
                burl = burl.replace('https://www.','https://app.')
            else:
                burl = burl.replace('https://','https://app.')
            c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + '" />') + get_body('','') )
    return c

if __name__ == '__main__':
    #For dev_mode and testing --> application.run(host='0.0.0.0', port=80, threaded=True)
    #For AWS Beanstalk --> application.run()
    if not DEV_MODE:
        application.run()
    else:
        application.run(host='0.0.0.0', port=80, threaded=True)
