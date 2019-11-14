""" App Search functionalities """
import pymysql.cursors
from app_head import get_head
from app_body import get_body
from app_page import set_page
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
from sa_func import get_random_str
from app_cookie import theme_return_this, get_sa_theme

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_search_table_content(burl, nonavbar):
    """ xxx """
    return_data = ''
    nonavbarparam = '&nonavbar=1'
    if nonavbar is None:
        nonavbarparam = ''

    return_data = ' '+\
    '<script>$(document).ready(function($) {'+\
    '$(".sa-table-click-row").click(function() {'+\
    'window.document.location = $(this).data("href");'+\
    '});'+\
    '});</script>'

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT feed.search, feed.content, markets.market_label, feed.url, '+\
    'feed.type FROM feed LEFT JOIN markets ON markets.market_id = feed.market '+\
    'WHERE (feed.type<>9 AND feed.type<>3) ORDER BY feed.symbol'
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        search_text = row[0]
        content_details = row[1]
        scope_text = row[2]
        url = row[3].replace('{burl}', burl) + nonavbarparam
        feed_type = row[4]

        textcolor = ''
        if feed_type == 2:
            textcolor = theme_return_this('blue', '#5bc0de')

        return_data = return_data +\
        '<tr class="sa-table-click-row" data-href="'+ str(url) +'">'+\
        '    <td style="text-align: left; color:' +\
        textcolor + ';" scope="row"><strong>'+ str(search_text) +'</strong></td>'+\
        '    <td style="text-align: left; color:' +\
        textcolor + ';">'+ str(content_details) +'</td>'+\
        '    <td style="text-align: left; color:' +\
        textcolor + ';">'+ str(scope_text) +'</td>'+\
        '</tr>'
    cursor.close()
    connection.close()
    return return_data

def gen_search_table(burl, nonavbar):
    """ xxx """
    return_data = ''
    return_data = '' +\
    '<table id="table_search" class="table table-hover table-sm">'+\
    '  <thead>'+\
    '    <tr>'+\
    '       <th scope="col" style="text-align: left">Instruments / Functions</th>'+\
    '       <th scope="col" style="text-align: left"></th>'+\
    '       <th scope="col" style="text-align: left"></th>'+\
    '    </tr>'+\
    ' </thead>'+\
    '  <tbody>'+\
    get_search_table_content(burl, nonavbar) +\
    '  </tbody>'+\
    '</table>'
    return return_data

def get_box_search(burl, nonavbar):
    """ xxx """
    box_content = ''
    col_id = 0
    sid = get_random_str(9)

    l_placeholder = "Enter function, ticker or search. Hit <enter> to go."

    search_box = ' '+\
    '  <form class="" action="'+ burl +'" method="get" id="searchForm" name="searhcForm" >'+\
    '       <div class="input-group input-group-lg">'+\
    '       <div class="input-group-prepend"><span class="input-group-text" '+\
    'id="inputGroup-sizing-lg"><i class="fas fa-search" '+\
    'style="font-size: xx-large;"></i></span></div>'+\
    '<input type="search" id="filterInput" name="'+\
    str(sid) +'" onkeyup="filterTable(); this.value = this.value.toUpperCase();" '+\
    'class="form-control" aria-label="Large" '+\
    'aria-describedby="inputGroup-sizing-sm" placeholder="'+\
    l_placeholder +'" autofocus></div><div>&nbsp;'+\
    '       </div>'+\
    '     <input type="hidden" name="sid" value="'+ str(sid) +'">'+\
    '  </form>'

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
    gen_search_table(burl, nonavbar)
    return box_content

def get_search_result(query):
    """ xxx """
    feed_type_filter_out = 3

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT url FROM feed WHERE search LIKE '%"+\
    str(query) +"%' and type<>"+ str(feed_type_filter_out)
    cursor.execute(sql)
    res = cursor.fetchall()
    url = ''
    return_data = ''

    for row in res:
        url = row[0].replace('{burl}', '')
        return_data = set_page(get_head('<meta http-equiv="refresh" content="0;URL=' +\
                                         str(url) + '" />') + get_body('', ''))

    if return_data == '':
        return_data = set_page(get_head('<meta http-equiv="refresh" content="0;URL=/?s=0" />') +\
                               get_body('', ''))

    cursor.close()
    connection.close()
    return return_data

def get_search_page_content(burl, nonavbar):
    """ xxx """
    box_content = ''
    box_class = 'box'
    if nonavbar is None:
        box_class = 'box-top'

    box_content = ' ' +\
    '<div class="'+ box_class +'">' +\
    '   <div class="row">'+\
    '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
    '            <div class="box-part rounded sa-center-content" style="'+\
    theme_return_this('', 'border-style:solid; border-width:thin; border-color:#343a40;') +'">'+\
    get_box_search(burl, nonavbar) +\
    '            </div>'+\
    '        </div>'+\
    '   </div>'+\
    '</div>'
    return box_content

def get_search_page(appname, burl, nonavbar):
    """ xxx """
    return_data = ''
    navbarcontent = ''
    if nonavbar is None:
        navbarcontent = navbar(burl, 1)

    return_data = get_head(get_loading_head() +\
                           get_googleanalytics() +\
                           get_title(appname) +\
                           get_metatags(burl) +\
                           set_ogp(burl, 1, '', '') +\
                           get_bootstrap(get_sa_theme(), burl) +\
                           get_font_awesome() +\
                           get_stylesheet(burl))
    return_data = return_data +\
    get_body(get_loading_body(), navbarcontent +\
             get_search_page_content(burl, nonavbar) +\
             get_page_footer(burl))
    return_data = set_page(return_data)
    return return_data
