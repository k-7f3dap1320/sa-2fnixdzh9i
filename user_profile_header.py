""" Header with the moving tickers """
from app_cookie import user_is_login, user_get_uid
from tradingview_ticker import get_tradingview_ticker

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_box_user_profile_header():
    """ Get the moving tickers header """
    box_content = ''
    if user_is_login() == 1:
        uid = user_get_uid()

        box_content = '<div class="box-uhead sa-uhead-box">' +\
        '   <div class="row sa-uhead-box bg-dark">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content sa-uhead-box" '+\
        'style="height: 95px;">'+\
        get_tradingview_ticker(uid) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    return box_content
