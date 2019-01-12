# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *

def get_signin_box(burl):

    box_content = ''

    try:

        box_content = '' +\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part sa-signin-box">'+\
        '                <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '                   <h1>A.I. Powered Trading Intelligence</h1>   '+\
        '                   <div>Your personal trading assistant</div>'+\
        '                </div>'+\
        '                <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '                </div>'+\
        '            </div>'+\
        '        </div>'


        cr.close()
        connection.close()

    except Exception as e: print(e)

    return box_content
