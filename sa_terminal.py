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
from sa_func import redirect_if_not_logged_in
from print_google_ads import print_google_ads

def get_terminal_desc(burl):
    """ xxx """
    ret = ''
    title = '<h3 style="'+ theme_return_this('','color:white;') +'text-align: left;">Smartalpha Terminal</h3>'
    description = '<div style:"text-align:left;">Add panels, charts and functions with &lt;search&gt; on the top-left corner. '+\
    'Type &lt;HELP&gt; &lt;GO&gt; for Help. To run terminal, do no operate the browser in fullscreen mode.</div><div>&nbsp;</div>'
    launch_btn ='<button type="button" class="btn btn-primary btn-lg" style="font-size: large;">Launch Terminal</button>'
    btn_space = '<div>&nbsp;</div>'

    ret = title +\
    description +\
    launch_btn +\
    btn_space
    return ret

def get_sa_terminal_content(burl):
    """ Content of the page """

    box_content = ''+\
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
    ''+\
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
    print_google_ads('billboard', 'center')
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
