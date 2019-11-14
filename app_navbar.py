""" App Navigation bar """
from app_cookie import user_is_login
from sa_func import get_broker_affiliate_link, get_random_str
from user_dashboard_count import get_num_orders

def get_how_menu(burl):
    """ xxx """
    return_data = ''
    l_helptooltip = 'Quick Help over there...'
    if user_is_login() == 1:
        l_howitworks = '<i class="far fa-question-circle" style="font-size: x-large;"></i>'
    else:
        l_howitworks = ''

    l_how_menu = '<li class="nav-item d-none d-sm-block">'+\
    '<a class="nav-link sa-navbar-text" href="'+\
    burl +'h/" data-toggle="tooltip" data-placement="bottom" data-original-title="'+\
    l_helptooltip +'">'+ l_howitworks +'</a></li>'

    return_data = l_how_menu
    return return_data

def get_dashboard_menu(burl):
    """ xxx """
    return_data = ''
    l_dashboard = 'Dashboard'
    num_dashboard_badge = (get_num_orders('open') +
                           get_num_orders('close') +
                           get_num_orders('pending'))
    l_dashboard_menu = '<li class="nav-item d-none d-sm-block">'+\
    '<a class="nav-link sa-navbar-text" href="'+\
    burl +'?dashboard=1" data-toggle="tooltip" data-placement="bottom" data-original-title="'+\
    l_dashboard +'" ><strong>'+\
    '<i class="fas fa-tachometer-alt" style="font-size: x-large;"></i>' +\
    '</strong><sup><span class="badge badge-pill badge-danger">'+\
    str(num_dashboard_badge) +'</span></sup></a></li>'
    return_data = l_dashboard_menu
    return return_data

def get_portfolio_button(burl):
    """ xxx """
    return_data = ''

    l_create_portfolio = 'Create a new trading strategy'
    portfolio_button = '<div class="d-none d-sm-block"><a href="'+\
    burl+'p/?ins=1&step=1&button=1" class="btn btn-lg btn-primary d-block d-md-inline-block" '+\
    'style="font-size:large;" data-toggle="tooltip" data-placement="bottom" '+\
    'title="" data-original-title="'+\
    l_create_portfolio +'"><i class="fas fa-edit"></i></a></div>'

    return_data = portfolio_button
    return return_data

def get_pricing_menu(burl):
    """ xxx """
    return_data = ''
    link = burl + 'pricing'
    l_title = 'Pricing'

    return_data = '<li>&nbsp;&nbsp;</li><li class="nav-item d-none d-sm-block">'+\
    '<a style="font-size: medium;" class="btn btn-sm btn-outline-info" href="'+\
    link +'">'+ l_title +'</a></li>'

    return return_data

def get_about_menu():
    """ xxx """
    return_data = ''
    link = get_broker_affiliate_link('googleSiteSmartAlpha', 'affiliate')
    l_title = 'What is SmartAlpha?'

    return_data = '<li>&nbsp;&nbsp;</li><li class="nav-item d-none d-sm-block">'+\
    '<a style="font-size: medium;" class="btn btn-sm btn-outline-info" href="'+\
    link +'">'+ l_title +'</a></li>'

    return return_data

def navbar(burl, disable_search):
    """ xxx """
    search_placeholder = '<search> function, ticker...'
    sid = get_random_str(9)
    l_join_now_btn = 'Join now'
    l_themeswitch = 'Theme: Light/Dark'
    l_settings = 'Settings'
    l_logout = 'Logout'

    search_box = ''
    if disable_search != 1:
        search_box = ' '+\
        '<img alt="" src="'+ burl+'static/cursor.gif'+'" height="15" class="d-none d-sm-block">'+\
        '    <input id="sa-search-input" onclick="location.href = \''+ burl + 'search/' +'\';"' +\
        '       type="text" name="'+ str(sid) +'" placeholder="'+\
        search_placeholder +'" aria-label="Search" class="d-none d-sm-block" >'

    if user_is_login() == 1:
        leftsidemenu = ''

        rightsidemenu = '' +\
        get_dashboard_menu(burl) +\
        get_how_menu(burl) +\
        '    <li class="nav-item dropdown">'+\
        '      <a class="nav-link dropdown-toggle" href="#" id="userDropdown" '+\
        'role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'+\
        '<i class="fas fa-user-circle" style="font-size: x-large;"></i>' +'</a>'+\
        '      <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">'+\
        '        <a class="dropdown-item sa-navbar-text" href="'+\
        burl + 'theme/"><i class="fas fa-toggle-on"></i> '+\
        l_themeswitch +'</a>'+\
        '        <a class="dropdown-item sa-navbar-text" href="'+\
        burl + 'settings/"><i class="fas fa-cog"></i> '+\
        l_settings +'</a>'+\
        '        <div class="dropdown-divider"></div>'+\
        '        <a class="dropdown-item sa-navbar-text" href="'+\
        burl + 'logout/"><i class="fas fa-sign-out-alt"></i> '+\
        l_logout +'</a>'+\
        '      </div>'+\
        '    </li>'+\
        '<li class="nav-item">'+\
        get_portfolio_button(burl)+\
        '</li>'
    else:
        leftsidemenu = ''+\
        get_pricing_menu(burl)+\
        get_about_menu()

        rightsidemenu = '<strong>'+\
        get_how_menu(burl) +\
        '</strong>' +'<li class="nav-item"><a href="'+\
        burl+'pricing/" class="btn btn-sm btn-danger btn-block form-signin-btn">'+\
        '<i class="fas fa-sign-in-alt"></i>&nbsp;'+\
        l_join_now_btn +'</a></li>'


    return_data = ''+\
    '<nav class="navbar fixed-top navbar-expand-sm navbar-dark bg-dark">'+\
    '<a class="navbar-brand" href="'+\
    burl +'"><img src="'+\
    burl+'static/logo.png' +'?'+\
    get_random_str(9) +'" height="30" alt="logo"></a>'+\
    '<button class="navbar-toggler" type="button" data-toggle="collapse" '+\
    'data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" '+\
    'aria-expanded="false" aria-label="Toggle navigation">'+\
    '  <span class="navbar-toggler-icon"></span>'+\
    '</button>'+\
    '<div class="collapse navbar-collapse" id="navbarSupportedContent">'+\
    search_box +\
    '  <ul class="navbar-nav mr-auto">'+\
    leftsidemenu +\
    '  </ul>'+\
    ' '+\
    '  <ul class="navbar-nav ml-auto">'+\
    rightsidemenu +\
    ' '+\
    '  </ul>'+\
    '</div>'+\
    '</nav>'
    return return_data
