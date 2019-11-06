
from sa_db import sa_db_access
access_obj = sa_db_access()
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_box_content(uid):
    box_content = ''
    return box_content
