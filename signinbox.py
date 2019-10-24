# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *
from signin_main import *
from app_cookie import *
from createuser_main import *

def get_signin_box(burl):

    box_content = ''

    try:

        if user_is_login() == 0:

            l_app_header_title = 'Create unlimited optimized trading portfolios'
            l_app_header_desc = 'Chart patterns, price movements, and news analysed using quantitative methods with the power of artificial intelligence to generate trading signals. SmartAlpha is your trading assistant to generate more profitable trades.'
            l_app_call_to_action_link = 'Join now.'
            etoro_logo_form = broker_link_form = go_to_url(get_broker_affiliate_link('eToro'),'form','eToro')
            etoro_logo_link = broker_link_form = go_to_url(get_broker_affiliate_link('eToro'),'link','eToro')

            box_content = etoro_logo_form +\
            '<div class="box-sign"><div class="row">' +\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="sign-part">'+\
            '               <div class="row sign-row">'+\
            '                <div class="col-lg-6 col-md-6 col-sm-23 col-xs-12 sa-signin-box">'+\
            '                   <div>&nbsp;</div>'+\
            '                   <h1 style="text-align: left; font-size:x-large; font-weight:bolder;">'+ l_app_header_title +'</h1>   '+\
            '                   <div>'+ l_app_header_desc +'&nbsp;<a href="'+ burl +'pricing/" class="text-info">'+ l_app_call_to_action_link +'</a></div>'+\
            '                   <div class="row d-none d-sm-block style="margin: 20px;">'+\
            '                       <a '+ etoro_logo_link +'" target="_blank"><img src="'+ burl +'static/etoro-logo.png" height="50px" style="margin:20px;" /></a>'+\
            '                       <a href="#" target=""><img src="'+ burl +'static/tradingview-logo.png" height="50px" style="margin:20px;" /></a>'+\
            '                       <a href="#" target=""><img src="'+ burl +'static/aws-logo.png" height="50px" style="margin:20px;" /></a>'+\
            '                   </div>'+\
            '                </div>'+\
            '                <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12" style="padding: 50px;">'+\
            get_login_form(burl,'dark','') +\
            '                </div>'+\
            '               </div>'+\
            '            </div>'+\
            '        </div>'+\
            '</div></div>'

            cr.close()
            connection.close()

    except Exception as e: print(e)

    return box_content
