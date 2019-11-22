""" Signin header in the main page when user not logged in """
from signin_main import get_login_form
from app_cookie import user_is_login
from sa_func import get_broker_affiliate_link, go_to_url

def get_signin_box(burl):
    """ xxx """
    box_content = ''
    if user_is_login() == 0:
        l_app_header_title = 'Create unlimited optimized trading portfolios'

        l_app_header_desc = 'Chart patterns, price movements, '+\
        'and news analysed using quantitative methods '+\
        'with the power of artificial intelligence to generate trading signals. '+\
        'Generate more profitable trades by using SmartAlpha as your trading assistant.'

        l_app_call_to_action_link = 'Join now.'
        etoro_logo_form = go_to_url(get_broker_affiliate_link('eToro', 'affiliate'),
                                    'form',
                                    'eToro')
        etoro_logo_link = go_to_url(get_broker_affiliate_link('eToro', 'affiliate'),
                                    'link',
                                    'eToro')

        box_content = etoro_logo_form +\
        '<div class="box-sign"><div class="row">' +\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="sign-part">'+\
        '               <div class="row sign-row">'+\
        '                <div class="col-lg-6 col-md-6 col-sm-23 col-xs-12 sa-signin-box">'+\
        '                   <div>&nbsp;</div>'+\
        '                   <h1 style="text-align: left; font-size:x-large; font-weight:bolder;">'+\
        l_app_header_title +'</h1>   '+\
        '                   <div>'+\
        l_app_header_desc +'&nbsp;<a href="'+\
        burl +'pricing/" class="text-info">'+\
        l_app_call_to_action_link +'</a></div>'+\
        '                   <div class="row d-none d-sm-block style="margin: 20px;">'+\
        '                       <a '+\
        etoro_logo_link +'" target="_blank"><img src="'+\
        burl +'static/etoro-logo.png" height="50px" style="margin:20px;" /></a>'+\
        '                       <a href="#" target=""><img src="'+\
        burl +'static/tradingview-logo.png" height="50px" style="margin:20px;" /></a>'+\
        '                       <a href="#" target=""><img src="'+\
        burl +'static/aws-logo.png" height="50px" style="margin:20px;" /></a>'+\
        '                   </div>'+\
        '                </div>'+\
        '                <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12" '+\
        'style="padding: 50px;">'+\
        get_login_form(burl, 'dark', '') +\
        '                </div>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'+\
        '</div></div>'
    return box_content
