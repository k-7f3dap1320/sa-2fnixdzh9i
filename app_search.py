# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_cookie import *
from sa_db import *
from sa_func import *
from app_cookie import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()



def gen_search_table(burl):

    r = ''
    try:
        r =  ' ' +\
        '<table id="table_search" class="table table-hover">'+\
        '  <thead>'+\
        '    <tr>'+\
        '       <th scope="col" style="text-align: left"></th>'
        '    </tr>'+\
        ' </thead>'+\
        '  <tbody>'+\
        get_table_content_list_instr_n_portf(burl,mode,what,step,portf,maxrow,x) +\
        '  </tbody>'+\
        '</table>'

    except Exception as e:
        print(e)
    return r

def get_box_search(burl):

    box_content = ''

    try:
        col_id = 0

        box_content = '' +\
        '<script>'+\
        'function filterTable() {'+\
        '  var input, filter, table, tr, td, i, txtValue;'+\
        '  input = document.getElementById("filterInput");'+\
        '  filter = input.value.toUpperCase();'+\
        '  table = document.getElementById("table_search");'+\
        '  tr = table.getElementsByTagName("tr");'+\
        '  for (i = 0; i < tr.length; i++) {'+\
        '    td = tr[i].getElementsByTagName("td")['+ str(col_id) +'];'+\
        '    if (td) {'+\
        '      txtValue = td.textContent || td.innerText;'+\
        '      if (txtValue.toUpperCase().indexOf(filter) > -1) {'+\
        '        tr[i].style.display = "";'+\
        '      } else {'+\
        '        tr[i].style.display = "none";'+\
        '      }'+\
        '    }'+\
        '  }'+\
        '}'+\
        '</script>'


        l_placeholder = "Enter function, ticker or search. Hit <enter> to go."
        list_class = 'sa-center-content sa-list-select-100pct sa-instr-n-portf-list'
        search_box = '<div class="input-group input-group-lg"><div class="input-group-prepend"><span class="input-group-text" id="inputGroup-sizing-lg"><i class="fas fa-search" style="font-size: xx-large;"></i></span></div><input type="text" id="filterInput" name="filterInput" onkeyup="filterTable()" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_placeholder +'" autofocus></div><div>&nbsp;</div>'

        box_content = box_content +\
        '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 d-none d-md-block">'+\
        '            <div class="box-part rounded '+ list_class +'" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        search_box +\
        gen_search_table(burl) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


    except Exception as e: print(e)

    return box_content
