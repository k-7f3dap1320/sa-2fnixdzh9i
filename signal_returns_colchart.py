""" Signal returns column chart section """
import pymysql.cursors
from app_cookie import theme_return_this
from gcharts_columnchart import get_gcharts_column

from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def get_signal_return_colchart(uid):
    """ xxx """
    return_data = ''
    chart_id = 'chart_signal_returns_col'
    title = 'Signal Performance'
    legend_position = 'none'
    width = '90%'
    height = '100px'
    color_neg = theme_return_this('red', '#d9534f')
    color_pos = theme_return_this('green', 'lime')
    data = []
    data_label = []
    data_color = []
    data_annotation = []
    l_y1 = '1-year'
    l_m6 = '6-month'
    l_m3 = '3-month'
    l_m1 = '1-month'
    factor = 1
    sep = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = 'SELECT instruments.y1_signal,instruments.m6_signal,'+\
    'instruments.m3_signal,instruments.m1_signal,instruments.w1_signal, instruments.unit '+\
    'FROM instruments JOIN symbol_list '+\
    'ON symbol_list.symbol = instruments.symbol WHERE symbol_list.uid = '+\
    str(uid)

    cursor.execute(sql)
    res = cursor.fetchall()

    for row in res:
        y_1 = row[0]
        m_6 = row[1]
        m_3 = row[2]
        m_1 = row[3]
        unit = row[5]

    if unit == '%':
        factor = 100
        sep = ''
    else:
        factor = 1
        sep = ' '

    data.append(round(y_1*factor, 1))
    data_label.append(l_y1)
    if y_1 < 0:
        data_color.append(color_neg)
    else:
        data_color.append(color_pos)
    data_annotation.append(str(round(y_1*factor, 1)) + sep + unit)

    data.append(round(m_6*factor, 1))
    data_label.append(l_m6)
    if m_6 < 0:
        data_color.append(color_neg)
    else:
        data_color.append(color_pos)
    data_annotation.append(str(round(m_6*factor, 1)) + sep + unit)

    data.append(round(m_3*factor, 1))
    data_label.append(l_m3)
    if m_3 < 0:
        data_color.append(color_neg)
    else:
        data_color.append(color_pos)
    data_annotation.append(str(round(m_3*factor, 1)) + sep + unit)

    data.append(round(m_1*factor, 1))
    data_label.append(l_m1)
    if m_1 < 0:
        data_color.append(color_neg)
    else:
        data_color.append(color_pos)
    data_annotation.append(str(round(m_1*factor, 1)) + sep + unit)

    return_data = get_gcharts_column(chart_id,
                                     data,
                                     data_label,
                                     data_color,
                                     data_annotation,
                                     title,
                                     legend_position,
                                     width,
                                     height)
    cursor.close()
    connection.close()

    return return_data
