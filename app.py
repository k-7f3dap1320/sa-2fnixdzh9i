# Copyright (c) 2018-present, Kahroo LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask, request
from kmain import *

app = Flask(__name__)

@app.route('/')
@app.route('/s/', endpoint='s', methods=["POST", "GET"])
@app.route('/p/', endpoint='p', methods=["POST", "GET"])
def go():
    if request.endpoint == 's':
        pass

    elif request.endpoint == 'p':
        pass

    else:
        x = request.args.get('x')
        c = gen_main_page(x)

    return c

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
