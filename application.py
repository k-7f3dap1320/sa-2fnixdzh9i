# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask, request
from flask_compress import Compress
from search import *
from app_main import *
from portf_main import *
from signal_main import *
from app_head import *; from app_body import *; from app_page import *

application = Flask(__name__)

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6; COMPRESS_MIN_SIZE = 500; Compress(application)


@application.route('/')
@application.route('/s/', endpoint='s', methods=["POST", "GET"])
@application.route('/p/', endpoint='p', methods=["POST", "GET"])
def go():

    appname = 'Project K'

    burl = request.url_root; burl = burl.replace('http://','https://')
    c = ''

    uid = request.args.get('uid')

    if request.endpoint == 's':
        c = gen_sign_page(uid,appname,burl)

    elif request.endpoint == 'p':
        c = gen_portf_page(uid,appname,burl)

    else:
        x = request.args.get('x')
        c = gen_main_page(x,appname,burl)

    sid = request.args.get('sid')
    q = request.args.get(sid)
    try:
        if len(sid)>5:
            c = get_search_result(q)
    except Exception as e: print(e)


    if burl.find('https://app.') == -1:
        if burl.find('https://www.') > 1:
            burl = burl.replace('https://www.','https://app.')
        else:
            burl = burl.replace('https://','https://app.')
        c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl + '" />') + get_body('','') )

    return c

if __name__ == '__main__':
    application.run()
