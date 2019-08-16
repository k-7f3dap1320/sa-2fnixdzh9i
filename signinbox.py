# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *
from signin_main import *
from app_cookie import *

def get_signin_box(burl):

    box_content = ''

    try:

        if user_is_login() == 0:

            l_app_header_title = 'Artificial Intelligence Trading Signal Insights'
            l_app_header_desc = 'Access 1,000+ Tradable Financial Instruments Including Stocks, Foreign Exchange Pairs (Forex), Commodities, Exchange Traded Funds (ETFs), Cryptocurrencies (Cryptos), Bonds, Binary Options; optimized using AI. Join Now to Create Your Trading Portfolio Signals by Just a Few Clicks.'
            l_app_call_to_action_link = 'Join now.'

            box_content = '<div class="box-sign"><div class="row">' +\
            '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
            '            <div class="sign-part">'+\
            '               <div class="row sign-row">'+\
            '                <div class="col-lg-6 col-md-6 col-sm-23 col-xs-12 sa-signin-box">'+\
            '                   <div>&nbsp;</div>'+\
            '                   <h1 style="text-align: left; font-size:x-large; font-weight:bolder;">'+ l_app_header_title +'</h1>   '+\
            '                   <div>'+ l_app_header_desc +'&nbsp;<a href="'+ burl +'pricing" class="text-info">'+ l_app_call_to_action_link +'</a></div>'+\
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
