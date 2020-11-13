""" App payment page """
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_loading import get_loading_head, get_loading_body
from app_footer import get_page_footer
from app_ogp import set_ogp
from app_title import get_title
from app_metatags import get_metatags
from bootstrap import get_bootstrap
from font_awesome import get_font_awesome
from app_navbar import navbar
from app_stylesheet import get_stylesheet
from googleanalytics import get_googleanalytics
from purechat import get_purechat
from sa_func import go_to_url, get_broker_affiliate_link

def get_package_price(what):
    """ xxx """
    if what == 'broker':
        return_data = '$1.00'
    else:
        return_data = '$5.00'
    return return_data

def get_broker_signup_button(burl, broker):
    """ xxx """
    return_data = ''
    l_button = 'Signup with '+ str(broker)

    button_signup = '<a href="'+\
    burl+'join/?broker='+\
    str(broker) +'" class="btn btn-success" style="font-size:small;">'+\
    l_button +'</a>'

    return_data = button_signup
    return return_data

def get_paypal_payment_notice(burl):
    l_secure_payment_with_paypal = 'Secure payment with PayPal'
    l_subscribe_payment_notice = ' Subscribe with confidence with PayPal Buyer Protection. '+\
    'You can cancel anytime. SmartAlpha is developed by Taatu Ltd. a U.K. '+\
    'Fintech company based in London.'
    paypal_notice = '<div style="margin-left: 8%; margin-right: 8%;"><strong>'+\
    ' <i class="fas fa-lock"></i> ('+\
    l_secure_payment_with_paypal +') '+\
    l_subscribe_payment_notice +'</strong>'+\
            '<div>'+ '' +'</div>'+\
            '<div><img alt="" src="'+\
            burl +'static/ccico.png" style="height: 30px;" /></div></div>'
    return paypal_notice

def get_paypal_payment_button(burl, is_soldout, size, what):
    """ xxx """
    return_data = ''
    if what == 'broker':
        l_button_signup = 'Signup with eToro<br />'
    else:
        l_button_signup = 'Signup<br />'

    l_button_soldout = 'Signup<br />(SOLD OUT!)'

    paypal_form_action = 'https://www.paypal.com/cgi-bin/webscr'
    if what != 'broker':
        paypal_button_id = 'HS42U57YF4HKL'
    else:
        paypal_button_id = 'L3FX73NUJVF64'
    soldout_form_action = '#'

    class_btn = ''
    style_btn = ''
    class_lg_btn = 'btn btn-lg btn-primary form-signin-btn'
    style_lg_btn = 'font-size:x-large; font-weight:bolder; width: 100%; max-width: 888px;'
    if what == 'broker':
        class_sm_btn = 'btn btn-success'
    else:
        class_sm_btn = 'btn btn-primary'
    style_sm_btn = 'font-size:small;'

    if size == 'lg':
        class_btn = class_lg_btn
        style_btn = style_lg_btn

    if size == 'sm':
        class_btn = class_sm_btn
        style_btn = style_sm_btn

    button_checkout = '<button type="submit" class="'+\
    class_btn +'" style="'+\
    style_btn +'">'+\
    l_button_signup +'</button>'

    button_soldout = '<button class="'+\
    class_btn +' disabled" style="'+\
    style_btn +'">'+\
    l_button_soldout + '</button>'

    if is_soldout:
        button_paypal = button_soldout
        form_action = soldout_form_action
    else:
        button_paypal = button_checkout
        form_action = paypal_form_action

    return_data = ' '+\
    '<!-- ----------------------------------------------------------------->'+\
    '<form action="'+ form_action +'" method="post" target="_top">'+\
    '<input type="hidden" name="cmd" value="_s-xclick">'+\
    '<input type="hidden" name="hosted_button_id" value="'+ paypal_button_id +'">'+\
    button_paypal +\
    '<img alt="" border="0" src="https://www.paypalobjects.com/en_US/i/scr/pixel.gif" '+\
    'width="1" height="1">'+\
    '</form>'+\
    '<!-- ----------------------------------------------------------------->'
    return return_data

def get_broker_url(broker, what, uid):
    """ xxx """
    return_data = ''
    if what == 'link':
        return_data = '<a '+\
        go_to_url(get_broker_affiliate_link(broker, 'affiliate'), 'link', uid) +\
        '" target="_blank">'+ broker +'</a>'

    if what == 'form':
        return_data = go_to_url(get_broker_affiliate_link(broker, 'affiliate'), 'form', uid)
    return return_data

def get_box_plan_selection(burl):
    """ xxx """
    box_content = ''
    broker = 'eToro'
    l_price = get_package_price('')
    l_price_broker = get_package_price('broker')
    broker_link_form = get_broker_url(broker, 'form', 1)

    l_feature_01 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    'Create and track your financial portfolio’s performance.</div>'+\
    'Create unlimited trading strategies.'

    l_feature_02 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    'Get clear trading instructions with entries and exits</div>'+\
    '(Take profit, Stop loss) on stocks, forex, commodities, ETF and crypto.'

    l_feature_03 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    'Trade the news with our in-build sentiment analysis.</div>'+\
    'Gauge the impact of ongoing news, and apply this information in your trading '+\
    'for high probability trading setup.'

    l_feature_04 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    'Analysed charts</div>Our technical analysis generated by '+\
    'our algorithms are designed to provide key levels for support and resistance, '+\
    'plus define current short and long term trends.'

    l_feature_05 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    'Market Intelligence</div>Get a “straight to the point” '+\
    'snapshot of what’s happening in the global financial market.'

    l_feature_06 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    '1000+ trading instruments</div>U.S. Stocks / U.K. Stocks / Germany Stocks '+\
    '/ World Indices / Major,cross Forex pairs / Commodities / '+\
    'Major Cryptocurrencies, Cross Cryptocurrencies '+\
    '/  Commodities / Bonds... '+\
    '<a href="'+ burl +\
    'ls/?w=instr" target="_blank">(List of available instruments)</a>'

    l_feature_07 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    'Place your trades and orders from SmartAlpha directly.</div>Trade with '+\
    get_broker_url(broker, 'link', 1) +\
    ' directly from SmartAlpha with just one click.'

    l_feature_08 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    'Auto-Trade on '+\
    get_broker_url(broker, 'link', 1) +\
    ' with our proprietary SmartAlpha allocation</div>Copy our winning strategy on '+\
    get_broker_url(broker, 'link', 1) +' and profit without the hassle.'

    l_feature_09 = '<div style="font-weight: bold; text-decoration: underline;">'+\
    'SmartAlpha Trading Intelligence is forever FREE for '+\
    get_broker_url(broker, 'link', 1) +' users</div>Terms & Conditions: Signup to '+\
    get_broker_url(broker, 'link', 1) +' from SmartAlpha or copy our Portfolio on '+\
    get_broker_url(broker, 'link', 1) +' if you are already a client at '+\
    get_broker_url(broker, 'link', 1) +'.'

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
    '      <th scope="col" style="vertical-align: top; text-align: left;">'+\
    '&nbsp;</th>'+\
    '      <th scope="col" style="vertical-align: top;">'+\
    '<strong>SmartAlpha Trading Intelligence + Trade with eToro</strong></th>'+\
    '      <th scope="col" style="vertical-align: top;">'+\
    '<strong>SmartAlpha Trading Intelligence</strong></th>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <th scope="col" style="vertical-align: top; text-align: left;">'+\
    '<div class="d-none d-sm-block">&nbsp;</div></th>'+\
    '      <th scope="col" style="vertical-align: top;">'+\
    '<h3>MONTHLY</h3><div style:"font-size: xx-large;">'+\
    l_price_broker +'</div></th>'+\
    '      <th scope="col" style="vertical-align: top;">'+\
    '<h3>MONTHLY</h3><div style:"font-size: xx-large;">'+\
    l_price +'</div></th>'+\
    '    </tr>'+\
    '  </thead>'+\
    '  <tbody>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >&nbsp;</td>'+\
    '      <td style="vertical-align: top;">'+\
    get_paypal_payment_button(burl, False, 'sm', 'broker') +'</td>'+\
    '      <td style="vertical-align: top;">'+\
    get_paypal_payment_button(burl, False, 'sm', '') +'</td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_01 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_02 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_03 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_04 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_05 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_06 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="fas fa-check-circle"></i></h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_07 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="far fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success"><div class="d-none d-sm-block">&nbsp;</h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_08 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="far fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success"><div class="d-none d-sm-block">&nbsp;</h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">'+\
    l_feature_09 +'</div></td>'+\
    '      <td><h2 class="text-success">'+\
    '<div class="d-none d-sm-block">'+\
    '<i class="far fa-check-circle"></i></h2></div></td>'+\
    '      <td><h2 class="text-success"><div class="d-none d-sm-block">&nbsp;</h2></div></td>'+\
    '    </tr>'+\
    '    <tr>'+\
    '      <td scope="row" style=" text-align: left;" >'+\
    '<div class="d-none d-sm-block">&nbsp;</div></td>'+\
    '      <td style="vertical-align: top;">'+\
    '<div class="d-none d-sm-block">'+\
    get_paypal_payment_button(burl, False, 'sm', 'broker') +'</div></td>'+\
    '      <td style="vertical-align: top;">'+\
    '<div class="d-none d-sm-block">'+\
    get_paypal_payment_button(burl, False, 'sm', '') +'</div></td>'+\
    '    </tr>'+\
    '  </tbody>'+\
    '</table>'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'+\
    get_paypal_payment_notice(burl)
    return box_content

def get_plan_selection_page(appname, burl, terminal):
    """ xxx """
    return_data = ''
    theme = 'light'
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(theme, burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_box_plan_selection(burl) +\
             get_page_footer(burl, False) +\
             get_purechat(1),'')
    return_data = set_page(return_data)
    return return_data
