# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *

def get_login_form(burl):

    r = ''
    try:
        r = '' +\
        '<div class="form-signin-text"><img src="'+ burl +'static/logo.png" height="30">&nbsp;Sign In</div>'+\
        '    <form class="form-signin" method="post" action="'+ burl+'login' +'">'+\
        '      <label for="inputEmail" class="sr-only">Email address</label>'+\
        '      <input type="email" id="user" name="user" class="form-control btn-outline-info" placeholder="Email address" required autofocus>'+\
        '      <label for="inputPassword" class="sr-only">Password</label>'+\
        '      <input type="password" id="password" name="password" class="form-control btn-outline-info" placeholder="Password" required>'+\
        '      <button class="btn btn-lg btn-info btn-block form-signin-btn" type="submit">Login</button>'+\
        '    </form>'
    except Exception as e: print(e)
    return r

def get_signin_box(burl):

    box_content = ''

    try:

        box_content = '<div class="box-sign"><div class="row">' +\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="sign-part">'+\
        '               <div class="row sign-row">'+\
        '                <div class="col-lg-6 col-md-6 col-sm-23 col-xs-12 sa-signin-box">'+\
        '                   <div>&nbsp;</div>'+\
        '                   <h1 style="text-align: left;">A.I. powered Trading Insights</h1>   '+\
        '                   <div>Your personal trading assistant. Access to more than 1,000 financial instruments, stocks, forex, commodities & cryptos. Get daily signals powered by Artificial intelligence.</div>'+\
        '                </div>'+\
        '                <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12" style="padding: 50px;">'+\
        get_login_form(burl) +\
        '                </div>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'+\
        '</div></div>'

        cr.close()
        connection.close()

    except Exception as e: print(e)

    return box_content
