""" A template page """
import pymysql.cursors
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

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_list_video_tutorials():
    ret = ''
    list_row = ''
    doc_cat_1 = 'intro'
    doc_cat_2 = 'help'
    title = ''
    content = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT title, content FROM documents WHERE category LIKE "%'+ str(doc_cat_1) +'%"'

    header = ''+\
    '   <div class="row">'

    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        title = row[0]
        content = row[1]
        list_row = list_row +\
        '<div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        str(content) +\
        '<br />'+\
        str(title)+\
        '</div>'
    sql = 'SELECT title, content FROM documents WHERE category LIKE "%'+ str(doc_cat_2) +'%"'
    footer = ''+\
    '   </div>'
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        title = row[0]
        content = row[1]
        list_row = list_row +\
        '<div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        str(content) +\
        '<br />'+\
        str(title)+\
        '</div>'
    cursor.close()
    connection.close()

    ret = header + list_row + footer
    return ret

def get_list_articles(burl):
    ret = ''+\
    '<table>'+\
    '  <tr>'+\
    '    <td></td>'+\
    '  </tr>'+\
    '</table>'

    return ret

def get_contact_tab(burl):
    ret = ''
    ret = ret + get_page_footer(burl, True)
    return ret

def get_help_tabs(burl):
    ret = '' +\
    '<ul class="nav nav-tabs" id="helpTab" role="tablist">'+\
    '  <li class="nav-item">'+\
    '    <a class="nav-link active" id="helptab" data-toggle="tab" '+\
    'href="#help" role="tab" aria-controls="help" aria-selected="true">Help</a>'+\
    '  </li>'+\
    '  <li class="nav-item">'+\
    '    <a class="nav-link" id="articlestab" data-toggle="tab" '+\
    'href="#articles" role="tab" aria-controls="articles" aria-selected="false">More articles</a>'+\
    '  </li>'+\
    '  <li class="nav-item">'+\
    '    <a class="nav-link" id="contacttab" data-toggle="tab" '+\
    'href="#contact" role="tab" aria-controls="contact" aria-selected="false">Contact</a>'+\
    '  </li>'+\
    '</ul>'+\
    '<div class="tab-content" id="myTabContent">'+\
    '  <div class="tab-pane fade show active" id="help" role="tabpanel" '+\
    'aria-labelledby="help">'+ get_list_video_tutorials() +'</div>'+\
    '  <div class="tab-pane fade" id="articles" role="tabpanel" '+\
    'aria-labelledby="articles">'+ get_list_articles(burl) +'</div>'+\
    '  <div class="tab-pane fade" style="overflow: hidden;" id="contact" role="tabpanel" '+\
    'aria-labelledby="contact">'+ get_contact_tab(burl) +'</div>'+\
    '</div>'
    return ret

def get_help_content(burl):
    """ Content of the page """

    box_content = ''+\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    get_help_tabs(burl) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content


def get_help_page(appname, burl, terminal):
    """ Return the content of the entire page """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           redirect_if_not_logged_in(burl, '') +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_help_content(burl) +\
             get_page_footer(burl, False))
    return_data = set_page(return_data)
    return return_data
