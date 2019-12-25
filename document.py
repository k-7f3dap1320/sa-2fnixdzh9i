""" Document / article page """
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
from app_cookie import get_sa_theme
from print_google_ads import print_google_ads
from help_page import get_list_articles
from card import get_card
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_doc_content(burl, uid, terminal):
    """ Content of the page """
    more_articles = 'More posts and articles'
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT title, content FROM documents WHERE uid='+ str(uid)
    cursor.execute(sql)
    res = cursor.fetchall()
    doc_title = ''
    doc_content = ''
    for row in res:
        doc_title = row[0]
        doc_content = row[1]

    box_content = ''+\
    '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content">'+\
    print_google_ads('leaderboard', 'center') +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded" style="text-align: justify; margin: 5%;">'+\
    '<h1>' + str(doc_title) + '</h1>' +\
    str(doc_content) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content">'+\
    print_google_ads('leaderboard', 'center') +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded">'+\
    '<h10><strong>'+ str(more_articles) +'</strong></h10>'+\
    get_list_articles(burl, 10) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded">'+\
    '<h10><strong>'+ str(more_articles) +'</strong></h10>'+\
    get_card('', 9, burl, terminal) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content


def get_doc_page(appname, burl, uid, terminal):
    """ Return the content of the entire page """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_doc_content(burl, uid, terminal) +\
             get_page_footer(burl, False))
    return_data = set_page(return_data)
    return return_data
