# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_page import set_page
from app_head import get_head
from app_ogp import set_ogp
from app_footer import get_page_footer
from app_metatags import get_metatags
from app_title import get_title
from app_body import get_body
from bootstrap import get_bootstrap
from google_chart import get_google_chart_script
from app_loading import get_loading_body, get_loading_head
from app_stylesheet import get_stylesheet
from app_navbar import navbar
from details_header import get_details_header
from portf_alloc import get_portf_alloc
from portf_perf_desc import get_portf_perf_desc
from portf_risk_trail_returns import get_portf_risk_trail_returns
from trades_tab import get_trades_box
from font_awesome import get_font_awesome
from googleanalytics import get_googleanalytics
from error_page import get_error_page
from sa_func import redirect_if_not_logged_in
from app_cookie import get_sa_theme

from sa_db import sa_db_access
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def gen_portf_popup(uid,pop):
    return_data = ''
    label_header = 'Trading strategy created!'
    label_content = 'Your trading strategy has been generated.'
    label_button = 'Take me to my strategy...'

    if pop == '1':
        return_data = '' +\
        '  <script type="text/javascript">'+\
        '  $(window).on(\'load\',function(){'+\
        '    $(\'#portf_popup\').modal(\'show\');'+\
        '  });'+\
        '  </script>'+\
        ' <div class="modal" id="portf_popup">'+\
        '    <div class="modal-dialog modal-lg">'+\
        '      <div class="modal-content">'+\
        '        <div class="modal-header">'+\
        '          <h4 class="modal-title">'+ label_header +'</h4>'+\
        '          <button type="button" class="close" data-dismiss="modal">&times;</button>'+\
        '        </div>'+\
        '        <div class="modal-body">'+\
        label_content +\
        '        </div>'+\
        '        <!-- Modal footer -->'+\
        '        <div class="modal-footer">'+\
        '          <button type="button" class="btn btn-info form-signin-btn" data-dismiss="modal">'+ label_button +'</button>'+\
        '        </div>'+\
        '      </div>'+\
        '    </div>'+\
        ' </div>'
    return return_data

def gen_portf_page(uid,appname,burl,pop):

    return_data = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.fullname FROM `symbol_list` JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
            "WHERE symbol_list.uid = " + str(uid)

        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            instfullname = row[0]

        return_data = get_head(  get_loading_head() + get_googleanalytics() + get_title( appname +' - ' + instfullname ) + get_metatags(burl) + redirect_if_not_logged_in(burl,'') + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_font_awesome() + get_google_chart_script() + get_stylesheet(burl) )
        return_data = return_data + get_body(  get_loading_body(), gen_portf_popup(uid,pop) + navbar(burl,0) + '<div class="box-top"><div class="row">' + get_details_header(uid,burl) + get_portf_alloc(uid,burl) + get_portf_perf_desc(uid) + get_portf_risk_trail_returns(uid) + get_trades_box(uid,burl,None) + '</div></div>' +  get_page_footer(burl)  )
        return_data = set_page(return_data)

        cr.close()
        connection.close()
    except Exception as e:
        print(e)
        get_error_page(appname,burl)

    return return_data
