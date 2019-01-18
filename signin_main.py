# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *

def get_login_form(burl,theme):

    r = ''
    try:

        if theme == 'dark':
            sign_in_class = 'form-signin-text-dark'
            logo = 'logo.png'
        else:
            sign_in_class = 'form-signin-text-light'
            logo = 'logo_light.png'
        r = '' +\
        '<div class="'+ sign_in_class +'"><img src="'+ burl +'static/'+ logo +'" height="30">&nbsp;Sign In</div>'+\
        '    <form class="form-signin" method="POST" action="'+ burl+'login/' +'">'+\
        '      <label for="user" class="sr-only">Email address</label>'+\
        '      <input type="email" id="user" name="user" class="form-control btn-outline-info" placeholder="Email address" required autofocus>'+\
        '      <label for="password" class="sr-only">Password</label>'+\
        '      <input type="password" id="password" name="password" class="form-control btn-outline-info" placeholder="Password" required>'+\
        '      <button class="btn btn-lg btn-info btn-block form-signin-btn" type="submit">Login</button>'+\
        '    </form>'
    except Exception as e: print(e)
    return r

def get_signin_content(burl):

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        get_login_form(burl,'light') +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def get_signin_page(appname,burl,err):
    r = ''
    try:
        r = get_head( get_loading_head() + get_title( appname ) + get_metatags(burl) + get_bootstrap() + get_awesomplete() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_signin_content(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
