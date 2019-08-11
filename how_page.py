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

    numslide = 15

    s01 = imgsrc + '01.png'
    s01title = 'SmartAlpha Dashboard'
    s01descr = 'Slide 1 detailed Description'
    s02 = imgsrc + '02.png'
    s02title = 'Your portfolio(s)'
    s02descr = 'Slide 2 detailed Description'
    s03 = imgsrc + '03.png'
    s03title = 'Tradebook'
    s03descr = 'Slide 3 detailed Description'
    s04 = imgsrc + '04.png'
    s04title = 'Control Center'
    s04descr = 'Slide 4 detailed Description'
    s05 = imgsrc + '05.png'
    s05title = 'Trading Signals and orders'
    s05descr = 'Slide 5 detailed Description'
    s06 = imgsrc + '06.png'
    s06title = 'Your aggregated signals portfolio(s) performance'
    s06descr = 'Slide 6 detailed Description'
    s07 = imgsrc + '07.png'
    s07title = 'Create portfolio'
    s07descr = 'Slide 7 detailed Description'
    s08 = imgsrc + '08.png'
    s08title = 'Select stocks, fx pairs, crypto, commodities etc...'
    s08descr = 'Slide 8 detailed Description'
    s09 = imgsrc + '09.png'
    s09title = 'View portfolio(s) details or remove a portfolio'
    s09descr = 'Slide 9 detailed Description'
    s10 = imgsrc + '10.png'
    s10title = 'Portfolio information'
    s10descr = 'Slide 10 detailed Description'
    s11 = imgsrc + '11.png'
    s11title = 'Search for signals and trading instruments'
    s11descr = 'Slide 11 detailed Description'
    s12 = imgsrc + '12.png'
    s12title = 'Trading Recommendations'
    s12descr = 'Slide 12 detailed Description'
    s13 = imgsrc + '13.png'
    s13title = 'Technical recommendations'
    s13descr = 'Slide 13 detailed Description'
    s14 = imgsrc + '14.png'
    s14title = 'Precise entry on lower timeframe based on technical analysis'
    s14descr = 'Slide 14 detailed Description'
    s15 = imgsrc + '15.png'
    s15title = 'Current active trade(s) and closed trades'
    s15descr = 'Slide 15 detailed Description'

    try:

        i = 1
        simg = ''; stitle = ''; sdescr = ''
        slideblock = ''
        lineblock = ''
        slideInterval = 9000
        while i <= numslide:
            if i == 1: sactive = 'active'; simg = s01; stitle = s01title; sdescr = s01descr
            if i == 2: sactive = ''; simg = s02; stitle = s02title; sdescr = s02descr
            if i == 3: sactive = ''; simg = s03; stitle = s03title; sdescr = s03descr
            if i == 4: sactive = ''; simg = s04; stitle = s04title; sdescr = s04descr
            if i == 5: sactive = ''; simg = s05; stitle = s05title; sdescr = s05descr
            if i == 6: sactive = ''; simg = s06; stitle = s06title; sdescr = s06descr
            if i == 7: sactive = ''; simg = s07; stitle = s07title; sdescr = s07descr
            if i == 8: sactive = ''; simg = s08; stitle = s08title; sdescr = s08descr
            if i == 9: sactive = ''; simg = s09; stitle = s09title; sdescr = s09descr
            if i == 10: sactive = ''; simg = s10; stitle = s10title; sdescr = s10descr
            if i == 11: sactive = ''; simg = s11; stitle = s11title; sdescr = s11descr
            if i == 12: sactive = ''; simg = s12; stitle = s12title; sdescr = s12descr
            if i == 13: sactive = ''; simg = s13; stitle = s13title; sdescr = s13descr
            if i == 14: sactive = ''; simg = s14; stitle = s14title; sdescr = s14descr
            if i == 15: sactive = ''; simg = s15; stitle = s15title; sdescr = s15descr

            slideblock = slideblock +\
             '    <div class="carousel-item '+ sactive +'">'+\
             '      <img class="d-block w-100" src="'+ simg +'" alt="'+ stitle  +'">'+\
             '      <div class="carousel-caption d-none d-md-block" style="background-color: black; opacity:0.5;">'+\
             '       <h5 style="color: white;">'+ stitle+'</h5>'+\
             '       <p style="color: white;">'+ sdescr +'</p>'+\
             '      </div>'+\
             '    </div>'

            if i == 1:
                lineClass = 'class="active"'
            else:
                lineClass = ''
            lineblock = lineblock +\
            '    <li data-target="#carouselIndicators" data-slide-to="'+ str(i-1) +'" '+ lineClass +'></li>'
            i += 1


        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content">'+\
        '<div id="carouselIndicators" class="carousel slide" data-interval="'+ str(slideInterval) +'" style="margin-left:auto; margin-right:auto; width:80%">'+\
        '  <ol class="carousel-indicators">'+\
        lineblock +\
        '  </ol>'+\
        '  <div class="carousel-inner">'+\
        slideblock +\
        '  </div>'+\
        '  <a class="carousel-control-prev" href="#carouselIndicators" role="button" data-slide="prev">'+\
        '    <span class="carousel-control-prev-icon" aria-hidden="true"></span>'+\
        '    <span class="sr-only">Previous</span>'+\
        '  </a>'+\
        '  <a class="carousel-control-next" href="#carouselIndicators" role="button" data-slide="next">'+\
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
