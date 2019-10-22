# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *
from app_cookie import *
from purechat import *
from createuser_main import *
from sa_func import *

def get_package_price():
    r = ''
    try:
        r = '$29.00'
    except Exception as e: print(e)
    return r

def get_broker_signup_button(burl,lang,broker):
    r = ''
    try:
        l_button = 'Signup with '+ str(broker)
        button_signup = '<a href="'+burl+'join/?broker='+ str(broker) +'" class="btn btn-success" style="font-size:small;">'+ l_button +'</a>'
        r = button_signup
    except Exception as e: print(e)
    return r

def get_paypal_payment_button(burl,lang,is_soldout,size):
    r = ''
    try:
        l_price = get_package_price()
        l_button_trial = '1-month Free Trial<br />'
        l_button_soldout = '1-month trial<br />(SOLD OUT!)'
        l_then_recurring_monthly = 'Then '+ l_price +' for each month'
        l_secure_payment_with_paypal = 'Secure payment with PayPal'
        l_subscribe_payment_notice = ' Subscribe with confidence with PayPal Buyer Protection. You can cancel anytime. SmartAlpha is developed by Taatu Ltd. a U.K. Fintech company based in London.'
        paypal_form_action = 'https://www.paypal.com/cgi-bin/webscr'
        paypal_button_id = 'HS42U57YF4HKL'
        soldout_form_action = '#'

        class_btn = ''; style_btn = ''; paypal_notice = ''
        class_lg_btn = 'btn btn-lg btn-primary form-signin-btn'
        style_lg_btn = 'font-size:x-large; font-weight:bolder; width: 100%; max-width: 888px;'
        class_sm_btn = 'btn btn-primary'
        style_sm_btn = 'font-size:small;'

        if size == 'lg':
            class_btn = class_lg_btn
            style_btn = style_lg_btn
            paypal_notice = '<div style="margin-left: 8%; margin-right: 8%;"><strong>'+ l_then_recurring_monthly +' <i class="fas fa-lock"></i> ('+ l_secure_payment_with_paypal +') '+ l_subscribe_payment_notice +'</strong></div>'+\
                    '<div>'+ '' +'</div>'+\
                    '<div>&nbsp;</div>'+\
                    '<img alt="" src="'+ burl +'static/ccico.png" style="height: 30px;" />'
        if size == 'sm':
            class_btn = class_sm_btn
            style_btn = style_sm_btn
            paypal_notice = '&nbsp;'

        button_checkout = '<button type="submit" class="'+ class_btn +'" style="'+ style_btn +'">'+ l_button_trial +'</button>'
        button_soldout = '<button class="'+ class_btn +' disabled" style="'+ style_btn +'">'+ l_button_soldout + '</button>'

        if is_soldout:
            button_paypal = button_soldout
            form_action = soldout_form_action
        else:
            button_paypal = button_checkout
            form_action = paypal_form_action

        r = ' '+\
        '<!-- ------------------------------------------------------------------------------------------------------------------- -->'+\
        '<form action="'+ form_action +'" method="post" target="_top">'+\
        '<input type="hidden" name="cmd" value="_s-xclick">'+\
        '<input type="hidden" name="hosted_button_id" value="'+ paypal_button_id +'">'+\
        button_paypal +\
        '<img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" width="1" height="1">'+\
        '</form>'+\
        paypal_notice +\
        '<!-- ------------------------------------------------------------------------------------------------------------------- -->'
    except Exception as e: print(e)
    return r

def get_broker_url(broker,what,uid):
    r = ''
    try:
        if what == 'link':
            r = '<a '+ go_to_url(get_broker_affiliate_link(broker),'link',uid) +'" target="_blank">'+ broker +'</a>'
        if what == 'form':
            r = go_to_url(get_broker_affiliate_link(broker),'form',uid)
    except Exception as e: print(e)
    return r

def get_box_plan_selection(burl):

    box_content = ''
    try:
        broker = 'eToro'

        l_price = get_package_price()
        broker_link_form = get_broker_url(broker,'form',1)
        l_feature_01 = '<strong>Create and track your financial portfolio’s performance.</strong><br />Create unlimited trading strategies.'
        l_feature_02 = '<strong>Get clear trading instructions with entries and exits</strong><br />(Take profit, Stop loss) on stocks, forex, commodities, ETF and crypto.'
        l_feature_03 = '<strong>Trade the news with our in-build sentiment analysis.</strong><br />Gauge the impact of ongoing news, and apply this information in your trading for high probability trading setup.'
        l_feature_04 = '<strong>Analysed charts</strong><br />Our technical analysis generated by our algorithms are designed to provide key levels for support and resistance, plus define current short and long term trends.'
        l_feature_05 = '<strong>Market Intelligence</strong><br />Get a “straight to the point” snapshot of what’s happening in the global financial market.'
        l_feature_06 = '<strong>1000+ trading instruments</strong><br />U.S. Stocks / U.K. Stocks / Germany Stocks / World Indices / Major,cross Forex pairs / Commodities / Major Cryptocurrencies, Cross Cryptocurrencies /  Commodities / Bonds... '+\
                        '<a href="'+ burl +'ls/?w=instr" target="_blank">(List of available instruments)</a>'
        l_feature_07 = '<strong>Place your trades and orders from SmartAlpha directly.</strong><br />Trade with '+ get_broker_url(broker,'link',1) +' directly from SmartAlpha with just one click.'
        l_feature_08 = '<strong>Auto-Trade on '+ get_broker_url(broker,'link',1) +' with our proprietary SmartAlpha allocation</strong><br />Copy our winning strategy on '+ get_broker_url(broker,'link',1) +' and profit without the hassle.'
        l_feature_09 = '<strong>SmartAlpha Trading Intelligence is forever FREE for '+ get_broker_url(broker,'link',1) +' users</strong><br />Terms & Conditions: Signup to '+ get_broker_url(broker,'link',1) +' from SmartAlpha or copy our Portfolio on '+ get_broker_url(broker,'link',1) +' if you are already a client at '+ get_broker_url(broker,'link',1) +'.'

        box_content = broker_link_form +\
        '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content">'+\
        '<div>&nbsp;</div>'+\
        '<div>&nbsp;</div>'+\
        '<table class="table-hover table-sm" style="font-size: smaller;">'+\
        '  <thead>'+\
        '    <tr>'+\
        '      <th scope="col" style="vertical-align: top; text-align: left;">&nbsp;</th>'+\
        '      <th scope="col" style="vertical-align: top;"><strong>SmartAlpha Trading Intelligence + Trade with eToro</strong></th>'+\
        '      <th scope="col" style="vertical-align: top;"><strong>SmartAlpha Trading Intelligence</strong></th>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <th scope="col" style="vertical-align: top; text-align: left;"><div class="d-none d-sm-block">Features</div></th>'+\
        '      <th scope="col" style="vertical-align: top;"><h3>FREE</h3></th>'+\
        '      <th scope="col" style="vertical-align: top;"><h3>MONTHLY</h3><div>'+ l_price +'</div></th>'+\
        '    </tr>'+\
        '  </thead>'+\
        '  <tbody>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >&nbsp;</td>'+\
        '      <td style="vertical-align: top;">'+ get_broker_signup_button(burl,'en',broker) +'</td>'+\
        '      <td style="vertical-align: top;">'+ get_paypal_payment_button(burl,'en', False, 'sm') +'</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_01 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_02 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_03 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_04 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_05 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_06 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="fas fa-check-circle"></i></h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_07 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="far fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block">&nbsp;</h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_08 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="far fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block">&nbsp;</h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">'+ l_feature_09 +'</div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block"><i class="far fa-check-circle"></i></h2></div></td>'+\
        '      <td><h2 class="text-success"><div class="d-none d-sm-block">&nbsp;</h2></div></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><div class="d-none d-sm-block">&nbsp;</div></td>'+\
        '      <td><div class="d-none d-sm-block" style="vertical-align: top;">'+ get_broker_signup_button(burl,'en',broker) +'</div></td>'+\
        '      <td><div class="d-none d-sm-block" style="vertical-align: top;">'+ get_paypal_payment_button(burl,'en', False, 'sm') +'</div></td>'+\
        '    </tr>'+\
        '  </tbody>'+\
        '</table>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def get_plan_selection_page(appname,burl):
    r = ''
    theme = 'light'
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( theme ,burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl,0) + get_box_plan_selection(burl) + get_page_footer(burl) + get_purechat(1) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
