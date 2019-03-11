# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask, request
from flask_compress import Compress
from search import *
from app_main import *; from portf_main import *; from signal_main import *
from createuser_main import *; from select_avatar import *; from select_market import *
from createportf_main import *
from app_head import *; from app_body import *; from app_page import *
from app_cookie import *
from sa_func import *
from signin_main import *

application = Flask(__name__)

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6; COMPRESS_MIN_SIZE = 500; Compress(application)


@application.route('/')
@application.route('/s/', endpoint='s', methods=["POST", "GET"])
@application.route('/p/', endpoint='p', methods=["POST", "GET"])
@application.route('/n/', endpoint='n', methods=["POST", "GET"])
@application.route('/login/', endpoint='login', methods=["POST", "GET"])
@application.route('/logout/', endpoint='logout', methods=["POST", "GET"])
@application.route('/signin/', endpoint='signin', methods=["POST", "GET"])
def go():

    appname = 'SmartAlpha | Trading Intelligence'
    dev_mode = True
    c = ''; burl = request.url_root;
    if not dev_mode: burl = burl.replace('http://','https://')

    uid = request.args.get('uid')
    ref = request.args.get('ref')
    lang = request.args.get('lang')
    x = request.args.get('x');
    if len(x)< 1 : x = get_user_default_profile()

    err = request.args.get('err')

    ############################################################################
    if request.endpoint == 's':
        c = gen_sign_page(uid,appname,burl)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'p':
        ins = request.values.get('ins')
        step = request.values.get('step')
        mode = request.values.get('mode')
        portf = request.values.get('portf')
        pop = request.values.get('pop')
        if ins == '1': c = gen_selectportf_page(appname,burl,step,mode,x,portf)
        if ins == '2': c = save_portf_select(appname,burl,step,mode,x,portf,uid)
        if ins == '3': c = custom_save_portf_page(appname,burl,mode,x)
        if ins == '4': c = portf_save_conviction(burl,mode,x)
        if ins == '5': c = portf_save(appname,burl)
        if ins is None: c = gen_portf_page(uid,appname,burl,pop)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'n':
        name = request.values.get('name')
        username = request.values.get('email')
        password = request.values.get('password')
        from_ip = request.values.get('from_ip')
        nickname = request.values.get('nickname')
        step = request.args.get('step')
        mode = request.values.get('mode')
        if step == 'a': c = gen_createuser_avatar(appname,burl,err)
        elif step == 'b': c = save_avatar(burl,nickname)
        elif step == 'c': c = gen_selectmarket_page(appname,burl,mode)
        elif step == 'd': c= save_selectmarket(burl,mode,x)
        else: c = gen_createuser_page(uid,appname,burl,name,username,password,from_ip)

    elif request.endpoint == 'login':
        user = request.values.get('user')
        password = request.values.get('password')
        c = user_login(user,password, burl )

    elif request.endpoint == 'logout':
        c = user_logout(burl)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'signin':
        c = get_signin_page(appname,burl,err)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    else:
        c = gen_main_page(x,appname,burl);
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)
    ############################################################################

    sid = request.args.get('sid')
    q = request.args.get(sid)
    try:
        if len(sid)>5:
            c = get_search_result(q)
    except Exception as e: print(e)


    if not dev_mode:
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
    application.run(host='0.0.0.0', port=80, threaded=True)
