# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from search import *
from sa_func import *
from app_cookie import *

def navbar(burl):

    search_placeholder = 'Enter function, ticker or search. Hit <enter> to go.'
    sid = get_random_str(9)
    l_join_now_btn = 'Join now'

    if not user_is_login():
        rightsidemenu = '<a href="'+burl+'n/?uid=0" class="btn btn-sm btn-danger btn-block form-signin-btn">'+ l_join_now_btn +'</a>'
    else:
        rightsidemenu = '<a href="'+burl+'logout" class="btn btn-sm btn-primary btn-block form-signin-btn">'+ 'logout:'+ user_get_uid() +'</a>'

    r = ''+\
    '<nav class="navbar fixed-top navbar-expand-sm navbar-dark bg-dark">'+\
    '<a class="navbar-brand" href="'+ burl +'"><img src="'+ burl+'static/logo.png' +'?'+ get_random_str(9) +'" height="30"></a>'+\
    '<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">'+\
    '  <span class="navbar-toggler-icon"></span>'+\
    '</button>'+\
    '<div class="collapse navbar-collapse" id="navbarSupportedContent">'+\
    '  <form class="form-inline my-2 my-lg-0" action="'+ burl +'" method="get" >'+\
    '    <input id="sa-search-input" class="form-control mr-lg-4 btn-outline-info awesomplete"' +\
    '       type="search" name="'+ str(sid) +'" placeholder="'+ search_placeholder +'" aria-label="Search" id="navBarSearchForm" data-list="'+ get_search_suggestions() +'" >'+\
    '     <input type="hidden" name="sid" value="'+ str(sid) +'">'+\
    '  </form>'+\
    '  <ul class="navbar-nav mr-auto">'+\
    '    <li class="nav-item dropdown">'+\
    '      <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Select Market</a>'+\
    '      <div class="dropdown-menu" aria-labelledby="navbarDropdown">'+\
    '        <a class="dropdown-item" href="'+ burl + '?x=">Top of everything</a>'+\
    '        <a class="dropdown-item" href="'+ burl + '?x=EQ:">All Stocks</a>'+\
    '        <a class="dropdown-item" href="'+ burl + '?x=FX:">Forex</a>'+\
    '        <a class="dropdown-item" href="'+ burl + '?x=CR:">Cryptocurrency</a>'+\
    '        <div class="dropdown-divider"></div>'+\
    '        <a class="dropdown-item" href="'+ burl + '?x=US>">U.S. Market</a>'+\
    '      </div>'+\
    '    </li>'+\
    '  </ul>'+\
    '  <ul class="navbar-nav ml-auto">'+\
    '      <li class="nav-item">'+\
    rightsidemenu +\
    '      </li>'+\
    '  </ul>'+\
    '</div>'+\
    '</nav>'

    return r
