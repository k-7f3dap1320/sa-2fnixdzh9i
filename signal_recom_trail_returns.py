""" Signal recommendations and trail returns section """
import pymysql.cursors
from app_cookie import theme_return_this
from trail_returns_chart import get_trailing_returns


from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def get_recomm(uid):
    """ xxx """
    recomm_box = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT instruments.recommendation FROM instruments "+\
    "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid=" +\
    str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        recommendation = row[0]
    recomm_box = recommendation
    cursor.close()
    connection.close()
    return recomm_box

def get_recomm_layout(uid):
    """ xxx """
    return_data = ''
    l_title = 'Technical Recommendation'
    return_data = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-signal-recomm-trail-ret" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    '               <div>'+ get_recomm(uid) +'</div>'+\
    '            </div>'+\
    '        </div>'
    return return_data

def get_chart_box(uid):
    """ xxx """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "SELECT instruments.fullname FROM instruments "+\
    "JOIN symbol_list ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.uid="+\
    str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        fullname = row[0].replace("'", "")
    cursor.close()
    connection.close()
    l_title = fullname + ' trailing returns'
    return_data = '' +\
    '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-signal-recomm-trail-ret" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    '               <div><h6>'+ l_title +'</h6></div>'+\
    get_trailing_returns(uid) +\
    '            </div>'+\
    '        </div>'
    return return_data

def get_sign_recommend_trail_returns(uid):
    """ xxx """
    return_data = ''
    return_data = get_recomm_layout(uid) + get_chart_box(uid)
    return return_data
