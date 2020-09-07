""" Document / article page """
import pymysql.cursors
from app_head import get_head
from app_body import get_body
from app_page import set_page
from sa_func import get_random_num
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
from document_menu import get_doc_menu
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

class doc_data:
    """ xxx """
    title = ''
    content = ''
    category = ''

    def __init__(self, uid):
        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT title, content, category FROM documents WHERE uid='+ str(uid)
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            self.title = row[0]
            self.content = row[1]
            self.category = row[2]
        cursor.close()
        connection.close()

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content
    
    def get_category(self):
        return self.category

def get_doc_illustration(burl):
    ret = ''
    img_filename = str(get_random_num(9)) + 'a.png'
    file_location = burl + 'static/img/' + img_filename
    ret = '<img src="'+ str(file_location) +'" width="100%" alt="article image">'
    return ret

def get_doc_content(burl, title, content, category, terminal):
    """ Content of the page """
    content_height = ''
    iframe_margin = ''
    iframe_content = ''
    gsheet_content_height = '100vh'
    gsheet_iframe_margin ='-40px'
    gdoc_content_height = '102vh'
    gdoc_iframe_margin = '-72px'
    toolbar_height = '30px'
    toolbar_padding = '0px'
    content_no_doc_found = '<i class="fas fa-exclamation-circle"></i>&nbsp;'+\
    '<strong>The function or content is not available at the moment.</strong><br />'+\
    'Please try again later. For support and assistance type:&nbsp;'+\
    '<a href="' + burl + 'h/?" '+\
    'style="text-decoration: none; font-weight: bolder;">&lt;HELP&gt;&nbsp;&lt;GO&gt;</a>.'
    
    if content.find('google.com/spreadsheets') > 0:
        content_height = gsheet_content_height
        iframe_margin = gsheet_iframe_margin
    if content.find('google.com/document') > 0:
        content_height = gdoc_content_height
        iframe_margin = gdoc_iframe_margin
        
    if content == '':
        iframe_content = content_no_doc_found
    else:
        iframe_content = ''+\
        '<iframe src="'+ str(content)+'" frameborder="0" '+\
        'style="overflow:hidden;height:100%;width:100%; margin-top:'+ iframe_margin +'" '+\
        'height="100%" width="100%">'+\
        '</iframe>'

    box_content = ''+\
    '<div class="box-top" style="max-width: 100%">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded" '+\
    '            style="height:'+ toolbar_height +'; padding:'+ toolbar_padding +';">'+\
    get_doc_menu(burl, category)+\
    '            </div>'+\
    '            <div class="box-part rounded" style="height:'+ content_height +';'+\
    '            overflow: hidden;">'+\
    iframe_content +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content


def get_doc_page(appname, burl, uid, terminal):
    """ Return the content of the entire page """
    return_data = ''

    document = doc_data(uid)
    title = document.get_title()
    content = document.get_content()
    category = document.get_category()
    page_url = burl+'doc/?uid=' + str(uid)

    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           set_ogp(burl, 2, title, page_url) +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_doc_content(burl, title, content, category, terminal) +\
             get_page_footer(burl, False),'overflow: hidden;')
    return_data = set_page(return_data)
    return return_data
