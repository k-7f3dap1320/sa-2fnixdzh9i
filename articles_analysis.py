""" Articles and Analysis section """
import pymysql.cursors
from app_cookie import theme_return_this
from sa_func import get_elapsed_time

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_list_articles(burl, max_list):
    """ xxx """
    ret = ''
    doc_cat = 'article'
    title = ''
    uid = 0
    l_latest_articles = 'Latest analysis'
    
    ret = '<span class="sectiont"><i class="fas fa-file-alt"></i>&nbsp;'+\
    l_latest_articles +'</span>'
    
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT uid, title, '+\
    '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time '+\
    'FROM documents WHERE category LIKE "%'+ str(doc_cat) +'%" '+\
    'ORDER BY date DESC LIMIT ' + str(max_list)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        uid = row[0]
        title = row[1]
        article_date = get_elapsed_time(row[2])
        ret = ret +\
        '<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12" '+\
        'style="border-top:0.5px; border-top-style: dotted; text-align: left;">'+\
        '<i class="fas fa-file-alt"></i> '+\
        '&nbsp;'+\
        '<strong>'+\
        '<a href="'+ str(burl) +'doc/?uid='+ str(uid) +'" target="_blank">'+\
        '<span style="'+\
        theme_return_this('color:black;', 'color:#00ffff;') +' ">'+\
        str(article_date) +'</span>&nbsp;'+\
        str(title) +'</a>'+\
        '</strong>'+\
        '</div>'
    cursor.close()
    connection.close()
    return ret