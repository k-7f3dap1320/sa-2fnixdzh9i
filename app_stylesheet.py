""" App stylesheet """
from sa_func import get_random_str

def get_stylesheet(burl):
    """ xxx """

    #Page main components
    body = 'body{font-family:monospace,sans-serif; overflow-x:hidden;}'
    footer = '.footer{}'
    scrollbar = '::-webkit-scrollbar {'+\
                'width: 5px;'+\
                '}'+\
                '::-webkit-scrollbar-track {'+\
                '  background: #363535; '+\
                '}'+\
                '::-webkit-scrollbar-thumb {'+\
                '  background: #888;'+\
                '}'+\
                '::-webkit-scrollbar-thumb:hover {'+\
                '  background: #555;'+\
                '}'
    desc = '.desc{font-size:small;}'
    expl = '.expl{font-size:x-small;}'
    box = '.box{padding:0px 0px; max-width:1500px}'
    boxtop = '.box-top{padding-top:60px; max-width:1500px}'
    boxsign = '.box-sign{padding-top:45px;}'
    boxuhead = '.box-uhead{padding-top:45px;}'
    boxpart = '.box-part{border-radius:0; padding:10px 10px; margin:10px 0px; overflow-x: auto;}'
    signpart = '.sign-part{background:#141415; border-radius:0; margin:10px 0px;}'
    signrow = '.sign-row{background-color: #151517;}'
    text = '.text{margin:10px 0px;}'
    btn = '.btn {font-size:x-small;}'
    section_title = '.sectiont {font-weight: lighter; font-size: medium; line-height: 50px;}'

    #Login Form
    form_signin = '.form-signin {width: 100%; max-width: 330px; padding: 15px; margin: 0 auto;}'
    form_signin_text_dark = '.form-signin-text-dark {color: white; text-align: center; }'
    form_signin_text_light = '.form-signin-text-light {text-align: center; }'

    form_signin_form_control = '.form-signin '+\
    '.form-control {position: relative; box-sizing: border-box; '+\
    'height: auto; padding: 10px; font-size: medium;}'

    form_signin_form_control_focus = '.form-signin .form-control:focus {z-index: 2;}'

    form_signin_input_email = '.form-signin input[type="email"] {margin-bottom: -1px; '+\
    'border-bottom-right-radius: 0; border-bottom-left-radius: 0;}'

    form_signin_input_password = '.form-signin input[type="password"] {margin-bottom: 10px; '+\
    'border-top-left-radius: 0; border-top-right-radius: 0;}'

    form_signin_btn = '.form-signin-btn {font-size: medium;}'

    #Specific settings
    sa_search_input = '#sa-search-input{width: 250px; font-size: '+\
    'small;background: transparent; border-top: none; border-left: none; '+\
    'border-right: none; border-bottom: solid; border-color: #00ffff; border-width: thin;}'

    sa_table_sm = '.sa-table-sm{font-size: small;}'
    sa_table_click_row = '.sa-table-click-row{cursor:pointer;}'
    sa_instr_n_portf_list = '.sa-instr-n-portf-list{margin-top: -10px;}'

    sa_signin_box = '.sa-signin-box{background-image:url('+\
    burl + 'static/sibg.gif); background-size:100% 100%; height: 300px; '+\
        'color: white; text-align: justify; padding: 20px; }'

    sa_user_header = '.sa-uhead-box{color: white; text-align: left;}'
    sa_descr_box_sm = '.sa-descr-box-sm{font-size: small;}'
    sa_chart_hw_90 = '.sa-chart-hw-90{height: 83%;}'
    sa_chart_hw_100 = '.sa-chart-hw-100{height: 400px;}'
    sa_chart_hw_300 = '.sa-chart-hw-290{height: 300px;}'
    sa_chart_hw_100_rsi = '.sa-chart-hw-100-rsi{height: 100px;}'
    sa_portf_alloc = '.sa-portf-alloc{height: 250px; overflow: auto;}'
    sa_portf_perf_portf_chart = '.sa-portf-perf-portf-chart{height: 380px; overflow: auto;}'
    sa_tab_sm = '#sa-tab-sm{font-size: x-small;}'
    sa_signal_ta_chart = '.sa-signal-ta-chart{height: 580px; overflow: hidden;}'

    sa_signal_alt_ord_prf = '.sa-signal-alt-ord-prf{height: 250px; '+\
    'overflow: auto; font-size: small;}'

    sa_signal_indic = '.sa-signal-indic{padding: 0px;}'

    sa_signal_recomm_trail_ret = '.sa-signal-recomm-trail-ret{height: 350px; '+\
    'overflow: auto; font-size: small;}'

    sa_center_content = '.sa-center-content{text-align:center;}'
    sa_navbar_text = '.sa-navbar-text{font-size: small;}'

    sa_cursor = '.sa-cursor { position: relative;}'+\
    '.sa-cursor	i { position: absolute; width: 10px; height: 80%; background-color: #00ffff;'+\
    'left: 5px; top: 10%; animation-name: blink; animation-duration: 1000ms;'+\
    'animation-iteration-count: infinite; opacity: 1;}'+\
    '.sa-cursor input:focus + i {display: none;}'+\
    '@keyframes blink {from { opacity: 1; } to { opacity: 0; }}'

    #Page loading gif display
    loading = ''+\
    '#load{'+\
    'width:100%;'+\
    'height:100%;'+\
    'position:fixed;'+\
    'z-index:1000;'+\
    'background:url("'+\
    burl + 'static/loader.gif' +\
    '?'+ get_random_str(9) +'") no-repeat center center rgba(52, 58, 64, 1)}'

    return_data = '<style>'+\
    body +\
    footer +\
    scrollbar +\
    desc +\
    expl +\
    box +\
    boxtop +\
    boxsign +\
    boxuhead +\
    boxpart +\
    signpart +\
    signrow +\
    text +\
    btn +\
    section_title +\
    sa_table_sm +\
    sa_table_click_row +\
    sa_instr_n_portf_list +\
    sa_signin_box +\
    sa_user_header +\
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
    sa_signal_indic +\
    sa_signal_recomm_trail_ret +\
    sa_center_content +\
    sa_navbar_text +\
    sa_cursor +\
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
    return return_data

def get_theme_color():
    """ xxx """
    theme_color = '#343a40'
    return theme_color
