""" Signal recommendations and trail returns section """
from app_cookie import *
from sa_db import *
access_obj = sa_db_access()
import pymysql.cursors
from trail_returns_chart import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_recomm(uid):
    """ xxx """
    recomm_box = ''
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.recommendation FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid=" + str(uid)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        recommendation = row[0]
    recomm_box = recommendation
    cr.close()
    connection.close()
    return recomm_box

def get_recomm_layout(uid):
    """ xxx """
    return_data = ''
    l_title = 'Technical Recommendation'
    return_data = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-signal-recomm-trail-ret" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    '               <div>'+ get_recomm(uid) +'</div>'+\
    '            </div>'+\
    '        </div>'
    return return_data

def get_chart_box(uid):
    """ xxx """
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.fullname FROM instruments JOIN symbol_list ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid="+ str(uid)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        fullname = row[0].replace("'","")
    cr.close()
    connection.close()
    l_title = fullname + ' trailing returns'
    return_data = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-signal-recomm-trail-ret" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    get_trailing_returns(uid) +\
    '            </div>'+\
    '        </div>'
    return return_data

def get_sign_recommend_trail_returns(uid):
    """ xxx """
    return_data =''
    return_data = get_recomm_layout(uid) + get_chart_box(uid)
    return return_data
