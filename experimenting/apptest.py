# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask, request
from app_page import *

app = Flask(__name__)

@app.route('/')
@app.route('/s/', endpoint='s', methods=["POST", "GET"])
@app.route('/p/', endpoint='p', methods=["POST", "GET"])
def go():
    if request.endpoint == 'i':
        uid = request.args.get('uid')
        msg = 'View function go() called from "i" route and uid='+ str(uid)
    elif request.endpoint == 'p':
        uid = request.args.get('uid')
        msg = 'View function go() called from "p" route and uid='+ str(uid)
    else:
        header = '<head>'+\
                    '<title>This is a test page</title>'+\
                '</head>'
        body = '<body>'+\
                    '<a href="#">Hello World!</a>'+\
                '</body>'
        msg = '<html>'+header+body+'</html>'

    return msg

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
