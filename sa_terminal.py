""" A template page """
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
from googleanalytics import get_googleanalytics
from app_stylesheet import get_stylesheet
from app_cookie import theme_return_this, get_sa_theme
from sa_func import redirect_if_not_logged_in, get_random_str
from print_google_ads import print_google_ads
from app_popup_modal import open_window_args
from user_profile_header import get_box_user_profile_header

def get_terminal_button_func(burl, func_name):
    """ xxx """
    ret = ''
    jsc = '' +\
    '<script>'+\
    'function '+ func_name +'{'+\
    'if((screen.availHeight || screen.height-30) > window.innerHeight) {'+\
    'var screen_y = (screen.height-50);'+\
    'var screen_x = (screen.width-55);'+\
    'var screen_y_half = screen_y/2;'+\
    'var screen_x_half = screen_x/2;'+\
    'var screen_x_quart = screen_x/4;'+\
    'var screen_x_right = screen_x_half + screen_x_quart;'+\
    'var common_args = \'location=no, menubar=no, status=no,toolbar=no\';'+\
    'var newsfeed_args = '+\
    '\'width=\'+ screen_x_half +\', height=\'+ screen_y +\', left=0, top=0,\'+ common_args;'+\
    open_window_args(burl+'?terminal', 'newsfeed_args')+\
    'var topright_one_args = '+\
    '\'width=\'+ screen_x_quart +\', height=\'+ screen_y_half +\', left=\'+ screen_x_half +\', top=0,\'+ common_args;'+\
    open_window_args(burl+'w/?funcname=get_tradingview_ecocal(0,0)&refreshw=1800&nonavbar', 'topright_one_args')+\
    'var topright_two_args = '+\
    '\'width=\'+ screen_x_quart +\', height=\'+ screen_y_half +\', left=\'+ screen_x_right +\', top=0,\'+ common_args;'+\
    open_window_args(burl+'w/?funcname=get_tradingview_watchlist(0,0)&nonavbar', 'topright_two_args')+\
    'var bottomright_one_args = '+\
    '\'width=\'+ screen_x_half +\', height=\'+ screen_y_half +\', left=\'+ screen_x_half +\', top=\'+ screen_y_half +\',\'+ common_args;'+\
    open_window_args(burl+'w/?funcname=get_tradingview_chart(566,0,0)&nonavbar', 'bottomright_one_args')+\
    '}'+\
    '}'+\
    '</script>'
    ret = jsc
    return ret

def get_terminal_desc(burl):
    """ xxx """
    ret = ''
    func_name = 'launchTerminal()'

    title = '<h3 style="'+ theme_return_this('', 'color:white;') +\
    'text-align: left;">Smartalpha Terminal</h3>'

    description = '<div style:"text-align:left;">Add panels, charts and functions with '+\
    '<a href="'+\
    burl +'search'+'"><strong>&lt;search&gt;</strong></a> on the top-left corner. '+\
    'Type <a href="'+\
    burl +'h"><strong>&lt;HELP&gt;</strong> <strong>&lt;GO&gt;</strong></a> for Help. '+\
    'To run terminal, do no operate the browser in fullscreen mode. <strong>ALLOW popup and redirects.</strong>'+\
    '</div><div>&nbsp;</div>'

    launch_btn = '<a href="javascript:'+\
    func_name +\
    ';" type="button" class="btn btn-primary btn-lg" style="font-size: large;">Launch Terminal</a>'

    btn_space = '<div>&nbsp;</div>'

    ret = ''+\
    get_terminal_button_func(burl, func_name)+\
    title +\
    description +\
    launch_btn +\
    btn_space
    return ret

def get_settings_note(burl):
    """ xxx """
    ret = ''
    description = 'To customize your newsfeed and select your default '+\
    'market and asset class type <a href="'+\
    burl +'settings'+'"><strong>&lt;SET&gt; &lt;GO&gt;</strong></a>'

    ret = description
    return ret

def get_sa_terminal_content(burl):
    """ Content of the page """
    box_content = get_box_user_profile_header()
    box_content = box_content +\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:orange;') +'">'+\
    get_terminal_desc(burl) +\
    '            </div>'+\
    '        </div>'+\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:black;') +'">'+\
    '<img src="'+ burl+ 'static/saterminal.png?'+ get_random_str(9) +'" height="200" />'+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'

    box_content = box_content +\
   '<div class="box">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    get_settings_note(burl) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'

    box_content = box_content +\
   '<div class="box">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:black;') +'">'+\
    print_google_ads('billboard', 'center')+\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'

    return box_content

def get_sa_terminal_page(appname, burl):
    """ Return the content of the entire page """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           redirect_if_not_logged_in(burl, burl + 'terminal') +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0) +\
             get_sa_terminal_content(burl) +\
             get_page_footer(burl))
    return_data = set_page(return_data)
    return return_data
