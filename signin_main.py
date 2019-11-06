
from app_head import *
from app_body import *
from app_page import *
from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *
from app_metatags import *
from bootstrap import *
from font_awesome import *
from app_navbar import *
from googleanalytics import *
from app_cookie import *
from purechat import *

def get_login_form(burl,theme,redirect):
    return_data = ''
    l_register_link = 'Register'
    l_forgot_password = 'Forgot password'
    if theme == 'dark':
        sign_in_class = 'form-signin-text-dark'
        logo = 'logo.png'
    else:
        sign_in_class = 'form-signin-text-light'
        logo = 'logo_light.png'
    return_data = '' +\
    '<div class="'+ sign_in_class +'"><img alt="" src="'+ burl +'static/'+ logo +'" height="30">&nbsp;Sign In</div>'+\
    '    <form class="form-signin" method="POST" action="'+ burl+'login/?redirect='+ redirect +'">'+\
    '      <label for="user" class="sr-only">Email address</label>'+\
    '      <input type="email" id="user" name="user" class="form-control btn-outline-info" placeholder="Email address" required autofocus>'+\
    '      <label for="password" class="sr-only">Password</label>'+\
    '      <input type="password" id="password" name="password" class="form-control btn-outline-info" placeholder="Password" required>'+\
    '      <button class="btn btn-lg btn-info btn-block form-signin-btn" type="submit">Login</button>'+\
    '<div>&nbsp;</div>'+\
    '<div><span style="float: left;"><a href="'+ burl +'pricing/" class="text-info">'+ l_register_link +'</a></span><span style="float: right;"><a href="'+ burl +'reset/?password" class="text-info">'+ l_forgot_password +'</a></span></div>'+\
    '    </form>'
    return return_data

def popup_login(err,burl):
    return_data = ''
    l_error_title = '<i class="fas fa-exclamation-circle"></i>&nbsp;Email and password you entered did not match our records'
    l_error_descr = 'Please double-check and try again. If you have any issue connecting to your account, please do not hesitate to contact us: <a href="mailto:info@taatu.co">info@taatu.co</a>'
    l_error_class = 'alert alert-danger'
    l_title = '<i class="fas fa-lock"></i>&nbsp;Restricted access to members only'
    l_join_now_button = 'Join now'
    l_descr = 'Provide your email and password to access to content. Signup below if you do not have an account.  '+\
    '<div>&nbsp;</div>' +\
    '<div><a href="'+ burl +'pricing" class="btn btn-sm btn-info form-signin-btn">'+ l_join_now_button +'</a></div>'
    l_class = 'alert alert-warning'

    if err == '1':
        l_title = l_error_title
        l_descr = l_error_descr
        l_class = l_error_class

    return_data = ''+\
    '<div class="'+ l_class +'" role="alert">' +\
    '  <strong>'+ l_title +'</strong><br>'+ l_descr +\
    '</div><div>&nbsp;</div>'
    return return_data

def get_signin_content(burl,theme,err,redirect):
    box_content = ''
    box_content = '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded">'+\
    popup_login(err,burl) +\
    get_login_form(burl,theme,redirect) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content

def get_signin_page(appname,burl,err,redirect):
    return_data = ''
    return_data = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_font_awesome() + get_stylesheet(burl) )
    return_data = return_data + get_body( get_loading_body(), navbar(burl,0) + get_signin_content(burl,'light',err,redirect) + get_page_footer(burl) + get_purechat(1) )
    return_data = set_page(return_data)
    return return_data
