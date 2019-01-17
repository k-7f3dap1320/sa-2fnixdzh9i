# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from signinbox import *



def get_signin_page(burl):

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        get_login_form(burl) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content
