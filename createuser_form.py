# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *
from sa_db import *
access_obj = sa_db_access()

def get_user_creation_form(burl):

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '     <form method="POST" action="'+ burl +'n/?uid=xxx" style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
        '         <div>'+\
        '            <div>'+\
        '<div style="text-align: center;"><img src="'+ burl +'static/logo_light.png?'+ get_random_str(9) +'" height="88"></div>'+\
        '                <hr>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '                <div class="form-group">'+\
        '                    <div class="input-group mb-2 mr-sm-2 mb-sm-0">'+\
        '                        <div class="input-group-addon" style="width: 2.6rem"><i class="fa fa-user"></i></div>'+\
        '                        <input type="text" name="name" class="form-control btn-outline-info" id="name" placeholder="Your name" required autofocus>'+\
        '                    </div>'+\
        '                </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '                <div class="form-group">'+\
        '                    <div class="input-group mb-2 mr-sm-2 mb-sm-0">'+\
        '                        <div class="input-group-addon" style="width: 2.6rem"><i class="fa fa-at"></i></div>'+\
        '                        <input type="email" name="email" class="form-control btn-outline-info" id="email" placeholder="Your email: you@example.com" required autofocus>'+\
        '                    </div>'+\
        '                </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '                <div class="form-group has-danger">'+\
        '                    <div class="input-group mb-2 mr-sm-2 mb-sm-0">'+\
        '                        <div class="input-group-addon" style="width: 2.6rem"><i class="fa fa-key"></i></div>'+\
        '                        <input type="password" name="password" class="form-control btn-outline-info" id="password" placeholder="Password" required>'+\
        '                    </div>'+\
        '                </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '                <button type="submit" class="btn btn-info btn-lg btn-block form-signin-btn"><i class="fa fa-user-plus"></i> Sign up</button>'+\
        '            </div>'+\
        '        </div>'+\
        '<div class="expl" style="text-align: center;">*We respect your privacy and will never share your email address with any person or organization.</div>'+\
        '    </form>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


        box_content = box_content + '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '               <div>&nbsp;</div>'+\
        '               <h5>Taatu Ltd.</h5>'+\
        '               <div>27 Old Gloucester Street</div>'+\
        '               <div>London</div>'+\
        '               <div>WC1N 3AX</div>'+\
        '               <div>United Kingdom</div>'+\
        '               <div>&nbsp;</div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '               <div>&nbsp;</div>'+\
        '               <h5>Contact Us, we love feedback</h5>'+\
        '               <div>e: <a href="mailto:info@taatu.co">info@taatu.co</a></div>'+\
        '               <div>w: <a href="http://taatu.co">www.taatu.co</a></div>'+\
        '               <div>&nbsp;</div>'+\
        '               <div>Do you have any problem to log in? Drop us an <a href="mailto:info@taatu.co">email</a> or talk with us on <a href="https://www.facebook.com/messages/t/taatuco" target="_blank">messenger</a>.</div>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content
