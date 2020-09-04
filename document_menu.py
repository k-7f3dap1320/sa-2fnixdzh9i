""" document toolbar, top menu """
import pymysql.cursors
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_doc_menu(burl, category):
    """
    Return default menu unless:
    category is: 
        [...]
    """
    ret = default_menu(burl)
    return ret

def default_menu(burl):
    """ xxx """
    ret = ''
    sql = ''
    menu_label = ''
    color = ''
    # Top Analysis (color: primary)
    sql = "SELECT uid, title FROM documents WHERE "+\
    "category LIKE '%perma%' ORDER BY title"
    color = "primary"
    menu_label = "Top Analysis"
    ret = ret + default_menu_content(sql, color, burl, menu_label)
    
    # By Asset Class (color: info)
    sql = "SELECT uid, title FROM documents WHERE "+\
    "category LIKE '%assetclass%' ORDER BY title"
    color = "info"
    menu_label = "By Asset Class"
    ret = ret + default_menu_content(sql, color, burl, menu_label)
    
    # By Sectors (color: warning)
    sql = "SELECT uid, title FROM documents WHERE "+\
    "category LIKE '%sector%' ORDER BY title"
    color = "warning"
    menu_label = "By Sectors"
    ret = ret + default_menu_content(sql, color, burl, menu_label)
    
    # Latest Analysis (color: danger)
    sql = "SELECT uid, title FROM documents WHERE "+\
    "category LIKE %article% ORDER BY date DESC"
    color = "danger"
    menu_label = "Latest"
    ret = ret + default_menu_content(sql, color, burl, menu_label)
    
    return ret

def default_menu_content(sql, color, burl, menu_label):
    ret = ''

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    res = cursor.fetchall()
    ret = ''+\
    '<div class="btn-group">'+\
    '  <button type="button" class="btn btn-'+ str(color) +' dropdown-toggle" '+\
    'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+\
    menu_label+\
    '  </button>'+\
    '  <div class="dropdown-menu">'

    for row in res:
        uid = row[0]
        title = row[1]
        '<a class="dropdown-item" href="'+ burl + 'doc/?uid='+ str(uid) +'">'+ str(title) +'</a>'
    ret = ret +\
    '  </div>'+\
    '</div>'
    return ret