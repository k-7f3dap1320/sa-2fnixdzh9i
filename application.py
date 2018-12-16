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

application = Flask(__name__)

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6; COMPRESS_MIN_SIZE = 500; Compress(application)


@application.route('/')
@application.route('/s/', endpoint='s', methods=["POST", "GET"])
@application.route('/p/', endpoint='p', methods=["POST", "GET"])
def go():

    appname = 'Project K'
    burl = request.url_root
    burl = burl.replace('http://','https://')

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


    return c

if __name__ == '__main__':
    application.run()
