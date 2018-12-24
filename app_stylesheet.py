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

    #Customized awesomplete
    awesomplete = '.awesomplete > ul {min-width: 200%;}'

    #Specific settings
    sa_search_input = '#sa-search-input{width: 320px; font-size: 13px;}'
    sa_table_sm = '.sa-table-sm{font-size: 12px;}'
    sa_descr_box_sm = '.sa-descr-box-sm{font-size: 13px;}'
    sa_chart_hw_100 = '.sa-chart-hw-100{height: 90%;}'
    sa_portf_alloc ='.sa-portf-alloc{height: 250px; overflow: auto;}'
    sa_portf_perf_portf_chart = '.sa-portf-perf-portf-chart{height: 380px; overflow: auto;}'
    sa_tab_sm = '#sa-tab-sm{font-size: 12px;}'
    sa_signal_ta_chart = '.sa-signal-ta-chart{height: 510px; overflow: auto;}'
    sa_signal_alt_ord_prf = '.sa-signal-alt-ord-prf{height: 250px; overflow: auto; font-size: 12px;}'

    #Page loading gif display
    loading = ''+\
    '#load{'+\
    'width:100%;'+\
    'height:100%;'+\
    'position:fixed;'+\
    'z-index:1000;'+\
    'background:url("'+ burl + 'static/loader.gif' +'?'+ get_random_str(9) +'") no-repeat center center rgba(242,241,246,1)}'

    r = '<style>'+\
    body +\
    desc +\
    expl +\
    box +\
    boxpart +\
    text +\
    btn +\
    awesomplete +\
    sa_table_sm +\
    sa_search_input +\
    sa_descr_box_sm +\
    sa_chart_hw_100 +\
    sa_portf_alloc +\
    sa_portf_perf_portf_chart +\
    sa_tab_sm +\
    sa_signal_ta_chart +\
    sa_signal_alt_ord_prf +\
    loading +\
    '</style>'


    return r

def get_theme_color():

    theme_color = '#343a40'
    return theme_color
