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
    box = '.box{padding:0px 0px;}'
    boxtop = '.box-top{padding-top:60px;}'
    boxsign = '.box-sign{padding-top:45px;}'
    boxuserheader = '.box-userheader{padding-top:45px; background: #343a40;}'
    boxpart = '.box-part{background:#FFF; border-radius:0; padding:10px 10px; margin:10px 0px; overflow-x: auto;}'
    signpart = '.sign-part{background:#151517; border-radius:0; margin:10px 0px;}'
    signrow = '.sign-row{background-color: #151517;}'
    text = '.text{margin:10px 0px;}'
    btn = '.btn {font-size:x-small;}'
    #Customized awesomplete
    awesomplete = '.awesomplete > ul {min-width: 200%;}'

    #Login Form
    form_signin = '.form-signin {width: 100%; max-width: 330px; padding: 15px; margin: 0 auto;}'
    form_signin_text_dark = '.form-signin-text-dark {color: white; text-align: center; }'
    form_signin_text_light = '.form-signin-text-light {text-align: center; }'
    form_signin_form_control = '.form-signin .form-control {position: relative; box-sizing: border-box; height: auto; padding: 10px; font-size: medium;}'
    form_signin_form_control_focus = '.form-signin .form-control:focus {z-index: 2;}'
    form_signin_input_email = '.form-signin input[type="email"] {margin-bottom: -1px; border-bottom-right-radius: 0; border-bottom-left-radius: 0;}'
    form_signin_input_password = '.form-signin input[type="password"] {margin-bottom: 10px; border-top-left-radius: 0; border-top-right-radius: 0;}'
    form_signin_btn = '.form-signin-btn {font-size: medium;}'

    #Specific settings
    sa_search_input = '#sa-search-input{width: 320px; font-size: 12px;}'
    sa_table_sm = '.sa-table-sm{font-size: 12px;}'
    sa_table_click_row = '.sa-table-click-row{cursor:pointer;}'
    sa_instr_n_portf_list = '.sa-instr-n-portf-list{margin-top: -10px;}'
    sa_box_h = '.sa-box-h{max-height: 400px;}'
    sa_signin_box = '.sa-signin-box{background-image:url('+ burl + 'static/sibg.gif); background-size:100% 100%; height: 300px; color: white; text-align: justify; padding: 20px; }'
    sa_descr_box_sm = '.sa-descr-box-sm{font-size: 13px;}'
    sa_chart_hw_90 = '.sa-chart-hw-90{height: 90%;}'
    sa_chart_hw_100 = '.sa-chart-hw-100{height: 350px;}'
    sa_chart_hw_300 = '.sa-chart-hw-290{height: 300px;}'
    sa_chart_hw_100_rsi = '.sa-chart-hw-100-rsi{height: 100px;}'
    sa_portf_alloc ='.sa-portf-alloc{height: 250px; overflow: auto;}'
    sa_portf_perf_portf_chart = '.sa-portf-perf-portf-chart{height: 380px; overflow: auto;}'
    sa_tab_sm = '#sa-tab-sm{font-size: 12px;}'
    sa_signal_ta_chart = '.sa-signal-ta-chart{height: 510px; overflow: auto;}'
    sa_signal_alt_ord_prf = '.sa-signal-alt-ord-prf{height: 250px; overflow: auto; font-size: 12px;}'
    sa_signal_recomm_trail_ret = '.sa-signal-recomm-trail-ret{height: 350px; overflow: auto; font-size: 12px;}'
    sa_center_content = '.sa-center-content{text-align:center;}'

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
    boxtop +\
    boxsign +\
    boxuserheader +\
    boxpart +\
    signpart +\
    signrow +\
    text +\
    btn +\
    awesomplete +\
    sa_table_sm +\
    sa_table_click_row +\
    sa_instr_n_portf_list +\
    sa_box_h +\
    sa_signin_box +\
    sa_search_input +\
    sa_descr_box_sm +\
    sa_chart_hw_90 +\
    sa_chart_hw_100 +\
    sa_chart_hw_100_rsi +\
    sa_chart_hw_300 +\
    sa_portf_alloc +\
    sa_portf_perf_portf_chart +\
    sa_tab_sm +\
    sa_signal_ta_chart +\
    sa_signal_alt_ord_prf +\
    sa_signal_recomm_trail_ret +\
    sa_center_content +\
    loading +\
    form_signin +\
    form_signin_text_dark +\
    form_signin_text_light +\
    form_signin_form_control +\
    form_signin_form_control_focus +\
    form_signin_input_email +\
    form_signin_input_password +\
    form_signin_btn +\
    '</style>'

    return r

def get_theme_color():

    theme_color = '#343a40'
    return theme_color
