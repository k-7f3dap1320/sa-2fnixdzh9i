""" Strategy portfolio creation main module """
import datetime
import pymysql.cursors
from flask import make_response, request, redirect
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
from app_cookie import get_sa_theme
from sa_func import get_random_num
from googleanalytics import get_googleanalytics
from list_instr_n_portf import get_box_list_instr_n_portf
from portf_save import get_box_portf_save

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_selectportf_box(burl, step):
    """ Get portfolio selection box """
    box_content = ''
    min_sel = '5'
    progress_value = '0'

    if step == '1':
        l_desc_part_1 = "Select from list."
        progress_value = '20'
    if step == '2':
        l_desc_part_1 = str(step) +" of "+ str(min_sel)
        progress_value = '40'
    if step == '3':
        l_desc_part_1 = str(step) +" of "+ str(min_sel)
        progress_value = '60'
    if step == '4':
        l_desc_part_1 = str(step) +" of "+ str(min_sel)
        progress_value = '80'
    if step == '5':
        l_desc_part_1 = str(step) +" of "+ str(min_sel)
        progress_value = '95'
    if step == '6':
        l_desc_part_1 = "Save strategy"
        progress_value = '100'

    l_back_button = 'back'
    l_skip_process_button = 'done'

    button_back = '<span style="float:left;"><button type="button" '+\
    'style="font-size: medium;" class="btn btn-lg btn-secondary" '+\
    'onClick="javascript:history.back();"><i class="fas fa-caret-left">'+\
    '</i>&nbsp;'+ l_back_button +'</button></span>'

    if step != '1' and step != '2' and step != '6':
        button_process_skip = '<span style="float:right;"><a href="'+\
        burl + 'p/?ins=3' +\
        '" style="font-size: medium;" class="btn btn-lg btn-secondary">'+\
        l_skip_process_button +'&nbsp;<i class="fas fa-forward"></i></a></span>'
    else:
        button_process_skip = ''

    portf_selection = '<h6>'
    for i in range(5):
        select_instr = get_portf_select(i+1)
        if select_instr != '':
            portf_selection = portf_selection +\
            '<span class="badge badge-info"><i class="fas fa-chart-pie">&nbsp;</i>'+\
            select_instr +'</span>&nbsp;&nbsp;'

    portf_selection = portf_selection + '</h6>'

    if int(step) > 1 and int(step) < 6:
        portf_selection = 'your strategy selection: ' + portf_selection
    else:
        portf_selection = ''

    box_content = '<div class="box-top">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part sa-center-content rounded">'+\
    '                   <div class="alert" role="alert">' +\
    '                       <h5><i class="fas fa-list-ol"></i>&nbsp;'+\
    l_desc_part_1 +'</h5>'+\
    button_back + '&nbsp;&nbsp;&nbsp;&nbsp;' +\
    button_process_skip +\
    '                          <div>&nbsp;</div> '+\
    '                          <div class="progress">'+\
    '                               <div class="progress-bar progress-bar-striped bg-success" '+\
    'role="progressbar" style="width: '+\
    str(progress_value) +'%" aria-valuenow="'+\
    str(progress_value) +'" aria-valuemin="0" aria-valuemax="100"></div>'+\
    '                          </div>'+\
    '                   </div>'+\
    portf_selection +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content

def save_portf_select(burl, step, uid):
    """ Save strategy portfolio selection """
    next_step = int(step) +1
    if int(step) < 5:
        resp = make_response(redirect(burl+'p/?ins=1&step='+ str(next_step)))
        resp.set_cookie('portf_s_'+\
                        str(step), str(uid), expires=datetime.datetime.now() +\
                        datetime.timedelta(days=1))
    else:
        resp = make_response(redirect(burl+'p/?ins=3'))
        resp.set_cookie('portf_s_'+\
                        str(step), str(uid), expires=datetime.datetime.now() +\
                        datetime.timedelta(days=1))
    return resp

def get_portf_select(select):
    """ xxx """
    return_data = ''
    uid = request.cookies.get('portf_s_' + str(select))
    if not uid is None or uid == '':

        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.fullname FROM instruments "+\
        "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
        "WHERE symbol_list.uid=" + str(uid)
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            return_data = row[0]
        cursor.close()
    return return_data

def ini_portf_select(response):
    """ Initialize strategy portfolio selection """
    resp = make_response(response)
    conviction = 'neutral'
    for i in range(5):

        if get_random_num(3) == 1:
            conviction = 'neutral'
        if get_random_num(3) == 2:
            conviction = 'weak'
        if get_random_num(3) == 3:
            conviction = 'strong'

        resp.set_cookie('portf_s_' +\
                        str(i+1), '0', expires=datetime.datetime.now() +\
                        datetime.timedelta(days=1))
        resp.set_cookie('portf_s_' +\
                        str(i+1) +\
                        '_type', 'long/short', expires=datetime.datetime.now() +\
                        datetime.timedelta(days=1))
        resp.set_cookie('portf_s_' +\
                        str(i+1) + '_conv', conviction, expires=datetime.datetime.now() +\
                        datetime.timedelta(days=1))
    return resp

def gen_selectportf_page(appname, burl, step, terminal):
    """ xxx """
    return_data = ''
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl, terminal, None) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() + get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_selectportf_box(burl, step) +\
             get_box_list_instr_n_portf(burl, 'portf_select', 'instr', step, 10000, ''))
    return_data = set_page(return_data)
    if step == '1':
        return_data = ini_portf_select(return_data)
    return return_data

def custom_save_portf_page(appname, burl, terminal):
    """ xxx """
    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl, terminal, None) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbar(burl, 0, terminal) +\
             get_selectportf_box(burl, '6') +\
             get_box_portf_save(burl))
    return_data = set_page(return_data)
    return return_data
