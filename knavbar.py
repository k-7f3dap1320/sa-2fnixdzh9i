# Copyright (c) 2018-present, Kahroo LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from search import *
from kfunc import *
aps = app_settings()

def navbar():

    sid = get_random_str(9)
    r = ''+\
    '<div id="navbar"><nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">'+\
    '<a class="navbar-brand" href="'+ aps.get_homepage() +'"><img src="'+ aps.get_navbar_logo() +'?'+ get_random_str(9) +'" height="30"></a>'+\
    '<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">'+\
    '  <span class="navbar-toggler-icon"></span>'+\
    '</button>'+\
    '<div class="collapse navbar-collapse" id="navbarSupportedContent">'+\
    '  <form class="form-inline my-2 my-lg-0">'+\
    '    <input class="form-control mr-lg-4 btn-outline-info awesomplete"' +\
    '       type="search" name="'+ str(sid) +'" placeholder="Search" aria-label="Search" id="navBarSearchForm" data-list="'+ get_search_suggestions() +'" >'+\
    '     <input type="hidden" name="sid" value="'+ str(sid) +'">'+\
    '  </form>'+\
    '  <ul class="navbar-nav mr-auto">'+\
    '    <li class="nav-item dropdown">'+\
    '      <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Select Market</a>'+\
    '      <div class="dropdown-menu" aria-labelledby="navbarDropdown">'+\
    '        <a class="dropdown-item" href="?x=">Top of everything</a>'+\
    '        <a class="dropdown-item" href="?x=EQ:">All Stocks</a>'+\
    '        <a class="dropdown-item" href="?x=FX:">Forex</a>'+\
    '        <a class="dropdown-item" href="?x=CR:">Cryptocurrency</a>'+\
    '        <div class="dropdown-divider"></div>'+\
    '        <a class="dropdown-item" href="?x=US>">U.S. Market</a>'+\
    '        <a class="dropdown-item disabled" href="#>">Thai Market</a>'+\
    '      </div>'+\
    '    </li>'+\
    ' </ul>'+\
    '</div>'+\
    '</nav></div>'

    return r
