""" Market selection module """
import pymysql.cursors
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_ogp import set_ogp
from app_metatags import get_metatags
from app_title import get_title
from bootstrap import get_bootstrap
from app_loading import get_loading_head, get_loading_body
from app_stylesheet import get_stylesheet
from app_navbar import navbar
from font_awesome import get_font_awesome
from app_cookie import get_sa_theme, user_get_uid
from googleanalytics import get_googleanalytics
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def save_selectmarket(burl, sel):
    """ xxx """
    return_data = set_page(get_head('<meta http-equiv="refresh" content="0;URL=' +\
                                    burl + 'genportf/?acm='+\
                                    str(sel) +'&step=1&notstart=0" />') + get_body('', ''))
    user_id = user_get_uid()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "UPDATE users SET default_profile='"+ str(sel) +"' WHERE uid='" + str(user_id) +"'"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    return return_data

def get_market_list(burl):
    """ xxx """
    return_data = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT asset_class_id, asset_class_name FROM asset_class ORDER BY asset_class_id"
    cursor.execute(sql)
    res = cursor.fetchall()
    label = 'x'
    return_data = '<div class="list-group">'
    for row in res:
        asset_class_id = row[0]
        asset_class_name = row[1]
        label = asset_class_name
        #handle particularities
        if asset_class_id == 'EQ:':
            label = 'All stocks'
        if asset_class_id == 'BD:':
            label = 'x'
        if asset_class_id == 'MA:':
            label = 'x'
        if asset_class_id == 'CO:':
            label = 'x'
        if asset_class_id == 'PRF:':
            label = 'x'
        if not label == 'x':
            return_data = return_data +\
            ' <a href="'+\
            burl +'n/?step=d&x='+\
            asset_class_id +\
            '" class="list-group-item list-group-item-action">'+\
            label +'</a>'

    sql = "SELECT market_id, market_label FROM markets order by market_label"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        market_id = row[0]
        market_label = row[1]
        label = market_label + ' Market'
        if not label == 'x':
            return_data = return_data +\
            ' <a href="'+\
            burl +\
            'n/?step=d&x='+\
            market_id +\
            '" class="list-group-item list-group-item-action">'+\
            label +'</a>'

    return_data = return_data + '</div>'
    cursor.close()
    connection.close()

    return return_data

def get_selectmarket_box(burl, mode):
    """ xxx """
    box_content = ''
    if mode == 'portf':
        l_desc_part_1 = "Select a market for your portfolio"
        l_desc_part_2 = "Pick from the list below..."
    else:
        l_desc_part_1 = "What do you most frequently trade?"
        l_desc_part_2 = "Pick a Market from the list below..."

    box_content = '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content">'+\
    '                   <div class="alert alert-success" role="alert">' +\
    '                       <h5><i class="fas fa-chart-line"></i>&nbsp;'+\
    l_desc_part_1 +'</h5>'+\
    l_desc_part_2 +\
    '                   </div><div>&nbsp;</div>'+\
    get_market_list(burl) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content

def gen_selectmarket_page(appname, burl, mode, terminal):
    """ xxx """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data + get_body(get_loading_body(), navbar(burl, 0, terminal) +\
                                         get_selectmarket_box(burl, mode))
    return_data = set_page(return_data)
    return return_data
