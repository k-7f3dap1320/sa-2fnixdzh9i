# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *

def get_help_content(burl):

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content">'+\
        '<div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">'+\
        '  <ol class="carousel-indicators">'+\
        '    <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>'+\
        '    <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>'+\
        '    <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>'+\
        '  </ol>'+\
        '  <div class="carousel-inner">'+\
        '    <div class="carousel-item active">'+\
        '      <img class="d-block w-100" src=".../800x400?auto=yes&bg=777&fg=555&text=First slide" alt="First slide">'+\
        '      <div class="carousel-caption d-none d-md-block">'+\
        '       <h5>Title slide 1</h5>'+\
        '       <p>Description for slide 1</p>'+\
        '      </div>'+\
        '    </div>'+\
        '    <div class="carousel-item">'+\
        '      <img class="d-block w-100" src=".../800x400?auto=yes&bg=666&fg=444&text=Second slide" alt="Second slide">'+\
        '      <div class="carousel-caption d-none d-md-block">'+\
        '       <h5>Title slide 2</h5>'+\
        '       <p>Description for slide 2</p>'+\
        '      </div>'+\
        '    </div>'+\
        '    <div class="carousel-item">'+\
        '      <img class="d-block w-100" src=".../800x400?auto=yes&bg=555&fg=333&text=Third slide" alt="Third slide">'+\
        '      <div class="carousel-caption d-none d-md-block">'+\
        '       <h5>Title slide 3</h5>'+\
        '       <p>Description slide 3</p>'+\
        '      </div>'+\
        '    </div>'+\
        '  </div>'+\
        '  <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">'+\
        '    <span class="carousel-control-prev-icon" aria-hidden="true"></span>'+\
        '    <span class="sr-only">Previous</span>'+\
        '  </a>'+\
        '  <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">'+\
        '    <span class="carousel-control-next-icon" aria-hidden="true"></span>'+\
        '    <span class="sr-only">Next</span>'+\
        '  </a>'+\
        '</div>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def get_help_page(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_help_content(burl) + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
