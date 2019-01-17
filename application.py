# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask, request
from flask_compress import Compress
from search import *
from app_main import *
from portf_main import *
from signal_main import *
from createuser_main import *
from app_head import *; from app_body import *; from app_page import *
from app_cookie import *
from app_login import *

application = Flask(__name__)

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6; COMPRESS_MIN_SIZE = 500; Compress(application)


@application.route('/')
@application.route('/s/', endpoint='s', methods=["POST", "GET"])
@application.route('/p/', endpoint='p', methods=["POST", "GET"])
@application.route('/n/', endpoint='n', methods=["POST", "GET"])
@application.route('/login/', endpoint='login', methods=["POST", "GET"])
@application.route('/logout/', endpoint='logout', methods=["POST", "GET"])
def go():

    appname = 'SmartAlpha | Trading Intelligence'
    dev_mode = True
    c = ''; burl = request.url_root;
    if not dev_mode: burl = burl.replace('http://','https://')

    uid = request.args.get('uid')
    ref = request.args.get('ref')

    #############
    if request.endpoint == 's': c = gen_sign_page(uid,appname,burl); c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'p': c = gen_portf_page(uid,appname,burl); c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'n':
        name = request.values.get('name'); username = request.values.get('email'); password = request.values.get('password')
        c = gen_createuser_page(uid,appname,burl,name,username,password);

    elif request.endpoint == 'login':
        user = request.values.get('user'); password = request.values.get('password')
        c = user_login(user,password, set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + '" />') + get_body('','') ) )

    elif request.endpoint == 'logout': c = user_logout(burl); c = set_sa_ref_code(ref,c)

    else: x = request.args.get('x'); c = gen_main_page(x,appname,burl); c = set_sa_ref_code(ref,c)
    ############

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
    #For dev_mode and testing
    #host='0.0.0.0', port=80, threaded=True
    application.run(host='0.0.0.0', port=80, threaded=True)
