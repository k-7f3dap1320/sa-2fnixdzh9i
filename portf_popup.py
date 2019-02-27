# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_db import *

access_obj = sa_db_access()
import pymysql.cursors

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def gen_portf_popup(uid,pop):
    r = ''
    try:
        label_header = 'Portfolio created!'
        label_content = 'Wow! Your newly created portfolio: {portf_fullname} looks great. Actually it is expected that your portfolio will return {portf_forecast} with a {portf_account_reference} {portf_unit} invested.'
        label_button = 'View details'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.fullname, instruments.w_forecast_display_info, instruments.account_reference, instruments.unit "+\
        "FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
        "WHERE symbol_list.uid = " + str(uid)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            portf_fullname = row[0]
            portf_forecast = row[1]
            portf_account_reference = row[2]
            portf_unit = row[3]
        cr.close()
        connection.close()

        label_content = label_content.replace('{portf_fullname}',portf_fullname)
        label_content = label_content.replace('{portf_forecast}',portf_forecast)
        label_content = label_content.replace('{portf_account_reference}',str(portf_account_reference))
        label_content = label_content.replace('{portf_unit}',portf_unit)

        if pop == '1':
            r = '' +\
            '  <script type="text/javascript">'+\
            '  $(window).on(\'load\',function(){'+\
            '    $(\'#portf_popup\').modal(\'show\');'+\
            '  });'+\
            '  </script>'+\
            ' <div class="modal" id="portf_popup">'+\
            '    <div class="modal-dialog">'+\
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
            '          <button type="button" class="btn btn-info" data-dismiss="modal">'+ label_button +'</button>'+\
            '        </div>'+\
            '      </div>'+\
            '    </div>'+\
            ' </div>'

    except Exception as e: print(e)
    return r
