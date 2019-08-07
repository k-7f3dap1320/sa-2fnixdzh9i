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

    imgsrc = burl + 'static/help/'
    sactive = ''

    numslide = 10

    s01 = imgsrc + '01.png'
    s01title = 'Slide 1 title'
    s01descr = 'Slide 1 detailed Description'
    s02 = imgsrc + '02.png'
    s02title = 'Slide 2 title'
    s02descr = 'Slide 2 detailed Description'
    s03 = imgsrc + '03.png'
    s03title = 'Slide 3 title'
    s03descr = 'Slide 3 detailed Description'
    s04 = imgsrc + '04.png'
    s04title = 'Slide 4 title'
    s04descr = 'Slide 4 detailed Description'
    s05 = imgsrc + '05.png'
    s05title = 'Slide 5 title'
    s05descr = 'Slide 5 detailed Description'
    s06 = imgsrc + '06.png'
    s06title = 'Slide 6 title'
    s06descr = 'Slide 6 detailed Description'
    s07 = imgsrc + '07.png'
    s07title = 'Slide 7 title'
    s07descr = 'Slide 7 detailed Description'
    s08 = imgsrc + '08.png'
    s08title = 'Slide 8 title'
    s08descr = 'Slide 8 detailed Description'
    s09 = imgsrc + '09.png'
    s09title = 'Slide 9 title'
    s09descr = 'Slide 9 detailed Description'
    s10 = imgsrc + '10.png'
    s10title = 'Slide 10 title'
    s10descr = 'Slide 10 detailed Description'

    try:

        i = 1
        simg = ''; stitle = ''; sdescr = ''
        slideblock = ''
        while i <= numslide:
            if i == 1: sactive = 'Active'; simg = s01; stitle = s01title; sdescr = s01descr
            if i == 2: sactive = ''; simg = s02; stitle = s02title; sdescr = s02descr
            if i == 3: sactive = ''; simg = s03; stitle = s03title; sdescr = s03descr
            if i == 3: sactive = ''; simg = s04; stitle = s04title; sdescr = s04descr
            if i == 3: sactive = ''; simg = s05; stitle = s05title; sdescr = s05descr
            if i == 3: sactive = ''; simg = s06; stitle = s06title; sdescr = s06descr
            if i == 3: sactive = ''; simg = s07; stitle = s07title; sdescr = s07descr
            if i == 3: sactive = ''; simg = s08; stitle = s08title; sdescr = s08descr
            if i == 3: sactive = ''; simg = s09; stitle = s09title; sdescr = s09descr
            if i == 10: sactive = ''; simg = s10; stitle = s10title; sdescr = s10descr

            slideblock = slideblock +\
             '    <div class="carousel-item '+ sactive +'">'+\
             '      <img class="d-block w-100" src="'+ simg +'" alt="'+ stitle  +'">'+\
             '      <div class="carousel-caption d-none d-md-block">'+\
             '       <h5>'+ stitle+'</h5>'+\
             '       <p>'+ sdescr +'</p>'+\
             '      </div>'+\
             '    </div>'


        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content">'+\
        '<div id="carouselExampleIndicators" class="carousel slide">'+\
        '  <ol class="carousel-indicators">'+\
        '    <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>'+\
        '    <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>'+\
        '    <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>'+\
        '  </ol>'+\
        '  <div class="carousel-inner">'+\
        slideblock +\
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
