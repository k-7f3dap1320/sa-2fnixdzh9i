# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *

def get_stylesheet(burl):

    #Page main components
    body = 'body{background: #eee;}'
    desc = '.desc{font-size:14px;}'
    expl = '.expl{font-size:10px;}'
    box = '.box{padding:60px 0px;}'
    boxpart = '.box-part{background:#FFF; border-radius:0; padding:10px 10px; margin:10px 0px;}'
    text = '.text{margin:10px 0px;}'
    btn = '.btn {font-size:x-small;}'

    sa_table_sm = '.sa-table-sm{font-size: 12px;}'
    sa_portf_alloc ='.sa-portf-alloc{height: 250px; overflow: auto;}'
    sa_portf_perf_portf_chart = '.sa-portf-perf-portf-chart{height: 500px; overflow: auto;}'

    #Page loading gif display
    loading = ''+\
    '#load{'+\
    'width:100%;'+\
    'height:100%;'+\
    'position:fixed;'+\
    'z-index:1000;'+\
    'background:url("'+ burl + 'static/loader.gif' +'?'+ get_random_str(9) +'") no-repeat center center rgba(242,241,246,1)}'

    r = '<style>'+ body + desc + expl + box + boxpart + text + btn + sa_table_sm + sa_portf_alloc + sa_portf_perf_portf_chart + loading + '</style>'


    return r

def get_theme_color():

    theme_color = '#343a40'
    return theme_color
