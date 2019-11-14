""" Help page: This module will be dismantled soon """
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_loading import get_loading_head, get_loading_body
from app_footer import get_page_footer
from app_ogp import set_ogp
from app_title import get_title
from app_metatags import get_metatags
from app_stylesheet import get_stylesheet
from bootstrap import get_bootstrap
from font_awesome import get_font_awesome
from app_navbar import navbar
from googleanalytics import get_googleanalytics
from app_cookie import theme_return_this, get_sa_theme
from purechat import *

def get_help_content(burl):
    """ xxx """
    box_content = ''
    imgsrc = burl + 'static/help/'
    sactive = ''
    numslide = 15

    s01 = imgsrc + '01.png'
    s01title = 'SmartAlpha Dashboard'
    s01descr = 'Click on "Dashboard" on the upper-right corner to access to your daily trading report all in one-place.'
    s02 = imgsrc + '02.png'
    s02title = 'Your portfolio(s)'
    s02descr = 'In the Dashboard, you can have an overview and control over all your trading activities and relevant trading signals. Portfolios contains up to 5 instruments or combined trading signals. You can create an ulimited number of portfolios.'
    s03 = imgsrc + '03.png'
    s03title = 'Tradebook'
    s03descr = 'Tradebook summarize all the trading signals you need to pay attention to according to your portfolio(s) selection.'
    s04 = imgsrc + '04.png'
    s04title = 'Control Center'
    s04descr = 'In just a quick glance, "Control Center" gives you what actions you have to take today such as which trades you might have to close or open. Note that the color code of the tag relates to the tradebook tag for you to recognize actions to take easily.'
    s05 = imgsrc + '05.png'
    s05title = 'Trading Signals and orders'
    s05descr = 'Actually, from the "Tradebook" you can switch between the list of current active trades (signals) and closed trades.'
    s06 = imgsrc + '06.png'
    s06title = 'Your aggregated signals portfolio(s) performance'
    s06descr = '"Performance" represents your equity curve for a one year of all your aggregated portfolios.'
    s07 = imgsrc + '07.png'
    s07title = 'Create portfolio'
    s07descr = 'Click on the upper-right corner on the navigation bar button to create a portfolio and select trading signals. You can select up to 5 instruments per portfolio, However, you can create an unlimited number of portfolios.'
    s08 = imgsrc + '08.png'
    s08title = 'Select stocks, fx pairs, crypto, commodities etc...'
    s08descr = 'Click from the list to select an instruments. Search for an instrument by using the search box. On the other hand, you can let SmartAlpha to choose instruments and do the process of selection for you using an optimum risk management.'
    s09 = imgsrc + '09.png'
    s09title = 'View portfolio(s) details or remove a portfolio'
    s09descr = 'Once your portfolio is created, you will see it appear in your "Dashboard". You can view, or delete it with the respective buttons.'
    s10 = imgsrc + '10.png'
    s10title = 'Portfolio information'
    s10descr = 'From the portfolio page, you can view all information related to the portfolio such as active/closed trades, performance, description and recommendations.'
    s11 = imgsrc + '11.png'
    s11title = 'Search for signals and trading instruments'
    s11descr = 'On the upper-left corner of the navigation bar, type the name or symbol/ticker to access quickly to signals or information you need.'
    s12 = imgsrc + '12.png'
    s12title = 'Trading Recommendations'
    s12descr = 'From the instrument page, you can access to various related information such as trading recommendation: Buy/Sell, Target Price, Stop Loss, and optimum entry point.'
    s13 = imgsrc + '13.png'
    s13title = 'Technical recommendations'
    s13descr = 'You also get a technical recommendation to assist you in your trading decisions.'
    s14 = imgsrc + '14.png'
    s14title = 'Precise entry on lower timeframe based on technical analysis'
    s14descr = 'Technical Analysis is an aggregated score of different indicators at different timeframe (moving average and oscillators) which provide you assistance for a precise timed entry.'
    s15 = imgsrc + '15.png'
    s15title = 'Current active trade(s) and closed trades'
    s15descr = 'All trades and signals are transparently available. Signals get improved over-time with SmartAlpha proprietary algorithm based on machine learning.'

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

    return box_content


def get_help_page(appname,burl):
    """ xxx """
    return_data = ''
    return_data = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap( get_sa_theme(),burl ) + get_font_awesome() + get_stylesheet(burl) )
    return_data = return_data + get_body( get_loading_body(), navbar(burl,0) + get_help_content(burl) + get_page_footer(burl) + get_purechat(1) )
    return_data = set_page(return_data)
    return return_data
