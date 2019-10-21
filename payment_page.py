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

def get_paypal_payment_button(burl,lang,is_soldout):
    r = ''
    try:
        l_price = 'USD 29.00'
        l_button_trial = 'Try 1-month for free<br />'
        l_button_soldout = '1-month trial. USD 5.00<br />(SOLD OUT!)'
        l_then_recurring_monthly = 'Then '+ l_price +' for each month'
        l_secure_payment_with_paypal = 'Secure payment with PayPal'
        l_subscribe_payment_notice = ' Subscribe with confidence with PayPal Buyer Protection. You can cancel anytime. SmartAlpha is developed by Taatu Ltd. a U.K. Fintech company based in London.'
        button_checkout = '<button type="submit" class="btn btn-lg btn-primary form-signin-btn" style="font-size:x-large; font-weight:bolder; width: 100%; max-width: 888px;">'+ l_button_trial +'</button>'
        button_soldout = '<button class="btn btn-lg btn-primary form-signin-btn disabled" style="font-size:x-large; font-weight:bolder; width: 100%; max-width: 888px;">'+ l_button_soldout + '</button>'
        paypal_form_action = 'https://www.paypal.com/cgi-bin/webscr'
        paypal_button_id = 'HS42U57YF4HKL'
        soldout_form_action = '#'

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
        '<div style="margin-left: 8%; margin-right: 8%;"><strong>'+ l_then_recurring_monthly +' <i class="fas fa-lock"></i> ('+ l_secure_payment_with_paypal +') '+ l_subscribe_payment_notice +'</strong></div>'+\
        '<div>'+ '' +'</div>'+\
        '<div>&nbsp;</div>'+\
        '<img alt="" src="'+ burl +'static/ccico.png" style="height: 30px;" />'+\
        '<!-- ------------------------------------------------------------------------------------------------------------------- -->'
    except Exception as e: print(e)
    return r

def get_box_plan_selection(burl):

    box_content = ''
    try:
        l_price = 'USD 29.00'
        l_less_than_price_coffee_day = '*For less than $1 a day.'
        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content">'+\
        '<div>&nbsp;</div>'+\
        '<div>&nbsp;</div>'+\
        '<div>&nbsp;</div>'+\
        get_paypal_payment_button(burl,'en', False) +\
        '<div>&nbsp;</div>'+\
        '<div>&nbsp;</div>'+\
        '<table class="table table-hover table-sm">'+\
        '  <thead>'+\
        '    <tr>'+\
        '      <th scope="col" style="vertical-align: top; text-align: left;">&nbsp;</th>'+\
        '      <th scope="col" style="vertical-align: top; text-align: left;"><strong>SmartAlpha Trading Intelligence</strong></th>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <th scope="col" style="vertical-align: top; text-align: left;">Features</th>'+\
        '      <th scope="col" style="vertical-align: top; text-align: left;"><h2>'+ l_price +'<sup>/month</sup></h2><span style="font-size:small;" class="text-danger">'+ l_less_than_price_coffee_day +'</span></th>'+\
        '    </tr>'+\
        '  </thead>'+\
        '  <tbody>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><strong>Turn any trading portfolio into a profitable one with SmartAlpha proprietary system.</strong></td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" ><strong>Stop wasting time researching, SmartAlpha does it for you and provide you clear trading instructions.</strong></td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >User friendly dashboard with all your trading information.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Exclusive SmartAlpha portfolio pre-generated by artificial intelligence personalized for you.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Create unlimited number of portfolios.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Check out top traders and follow their trades.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Ability to monitor top trading signals.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Access to all trading signals with instant email notifications.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Backtest and simulate performance of portfolios.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
            '    <tr>'+\
            '      <td scope="row" style=" text-align: left;" >Technical Analysis and chart patterns for all available assets.</td>'+\
            '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
            '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Clear entries and exits points defined.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Portfolio allocation automatically generated by algorithms for optimum performance.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Risk exposure and expected return of the asset/portfolio.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Transparent historical orders and performance.</td>'+\
        '      <td><h2 class="text-success"><i class="fas fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Dedicated account manager to support your trading desk.</td>'+\
        '      <td><h2 class="text-success"><i class="far fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Daily personalized trading intelligence report delivered to your inbox. (coming soon)</td>'+\
        '      <td><h2 class="text-success"><i class="far fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row" style=" text-align: left;" >Concrete and precise trading instruction report. (coming soon)</td>'+\
        '      <td><h2 class="text-success"><i class="far fa-check-circle"></i></h2></td>'+\
        '    </tr>'+\
        '  </tbody>'+\
        '</table>'+\
        '<div>&nbsp;</div>'+\
        get_paypal_payment_button(burl,'en', False) +\
        '<div>&nbsp;</div>'+\
        '<div>&nbsp;</div>'+\
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
