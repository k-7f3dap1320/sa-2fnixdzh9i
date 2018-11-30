# Copyright (c) 2018-present, Kahroo LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
@app.route('/i/', endpoint='i', methods=["POST", "GET"])
@app.route('/p/', endpoint='p', methods=["POST", "GET"])
def go():
    if request.endpoint == 'i':
        msg = 'View function go() called from "i" route'
    elif request.endpoint == 'p':
        msg = 'View function go() called from "p" route'
    else:
        msg = 'View function go() from any other route'

    return msg

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
