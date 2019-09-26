# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *
from app_stylesheet import *
from sa_db import *
from sa_func import *
from app_cookie import *
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_search_table_content(burl,nonavbar):
    r = ''
    nonavbarparam = '&nonavbar=1'
    try:
        if nonavbar is None: nonavbarparam = ''

        r = ' '

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT feed.search, feed.content, markets.market_label, feed.url, feed.type FROM feed LEFT JOIN markets ON markets.market_id = feed.market WHERE (feed.type<>9 AND feed.type<>3) ORDER BY feed.symbol'
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            search_text = row[0]
            content_details = row[1]
            scope_text = row[2]
            url = row[3].replace('{burl}',burl) + nonavbarparam
            feed_type = row[4]

            textcolor = ''
            if feed_type == 2: textcolor = theme_return_this('blue','#5bc0de');

            r = r +\
            '<tr class="sa-table-click-row" data-href="'+ str(url) +'">'+\
            '    <td style="text-align: left; color:' + textcolor + ';" scope="row"><strong>'+ str(search_text) +'</strong></td>'+\
            '    <td style="text-align: left; color:' + textcolor + ';">'+ str(content_details) +'</td>'+\
            '    <td style="text-align: left; color:' + textcolor + ';">'+ str(scope_text) +'</td>'+\
            '</tr>'
        cr.close()
        connection.close()

    except Exception as e: print(e)
    return r

def gen_search_table(burl,nonavbar):

    r = ''
    try:
        r =  ' ' +\
        '<table id="table_search" class="table table-hover table-sm">'+\
        '  <thead>'+\
        '    <tr>'+\
        '       <th scope="col" style="text-align: left">Instruments / Functions</th>'+\
        '       <th scope="col" style="text-align: left"></th>'+\
        '       <th scope="col" style="text-align: left"></th>'+\
        '    </tr>'+\
        ' </thead>'+\
        '  <tbody>'+\
        get_search_table_content(burl,nonavbar) +\
        '  </tbody>'+\
        '</table>'

    except Exception as e:
        print(e)
    return r

def get_box_search(burl,nonavbar):

    box_content = ''

    try:
        col_id = 0
        sid = get_random_str(9)

        l_placeholder = "Enter function, ticker or search. Hit <enter> to go."
        list_class = 'sa-center-content sa-list-select-100pct sa-instr-n-portf-list'
        search_box = ' '+\
        '  <form class="" action="'+ burl +'" method="get" id="searchForm" name="searhcForm" >'+\
        '       <div class="input-group input-group-lg">'+\
        '       <div class="input-group-prepend"><span class="input-group-text" id="inputGroup-sizing-lg"><i class="fas fa-search" style="font-size: xx-large;"></i></span></div><input type="search" id="filterInput" name="'+ str(sid) +'" onkeyup="filterTable(); this.value = this.value.toUpperCase();" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="'+ l_placeholder +'" autofocus></div><div>&nbsp;'+\
        '       </div>'+\
        '     <input type="hidden" name="sid" value="'+ str(sid) +'">'+\
        '  </form>'+\
        '  <script>'+\
        '   window.onload = function() {'+\
        '       document.getElementById("filterInput").focus();'+\
        '   }'+\
        '  </script>'

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

        box_content = box_content +\
        search_box +\
        gen_search_table(burl,nonavbar)

    except Exception as e: print(e)
    return box_content

def get_search_result(q):

    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT url FROM feed WHERE search LIKE '%"+ str(q) +"%'"
        cr.execute(sql)
        rs = cr.fetchall()
        url = ''
        c = ''

        for row in rs:
            url = row[0].replace('{burl}','')
            c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + str(url) + '" />') + get_body('','') )

        if c == '':
            c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=/?s=0" />') + get_body('','') )

        cr.close()
        connection.close()
    except Exception as e: print(e)
    return c

def get_search_page_content(burl,nonavbar):
    box_content = ''
    try:
        sid = get_random_str(9)

        box_class = 'box'
        if nonavbar is None:
            box_class = 'box-top'

        box_content = ' ' +\
        '<div class="'+ box_class +'">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content" style="'+ theme_return_this('','border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
        get_box_search(burl,nonavbar) +\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)
    return box_content

def get_search_page(appname,burl,nonavbar):
    r = ''
    try:
        navbarcontent = ''
        if nonavbar is None: navbarcontent = navbar(burl,1)

        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbarcontent + get_search_page_content(burl,nonavbar) + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)
    return r
