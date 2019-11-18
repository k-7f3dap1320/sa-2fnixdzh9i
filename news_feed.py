""" News feed  """
import pymysql.cursors
from app_cookie import theme_return_this
from sa_func import get_user_default_profile, get_user, get_random_str
from sa_func import go_to_url, get_elapsed_time, get_uid_from_symbol, get_uid
from tradingview_single_ticker import get_tradingview_single_ticker
from signal_details import get_signal_details
from sa_db import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_newsfeed(burl, sel, suid, numline, show_chart):
    """ xxx """
    ### ------------------------------------------------------------------------
    # sel == 0 : world top news
    # sel == 1 : news based on users default market, asset_class selection
    # sel == 2 : news based on users portfolio selection
    # suid == []: news from selected uid of the symbol
    # numline == []: number of line of news to return
    #show_chart == 1: show relevant chart or sentiment bar if sel == 0
    ### ------------------------------------------------------------------------
    return_data = ''
    l_view_article = 'more >'
    l_newsfeed_title = 'Newsfeed'
    lang = 'en'
    feed_type = 3
    ranking_filter = 9
    bsclass_left = 'col-lg-12 col-md-12 col-sm-12'
    bsclass_right = 'col-lg-12 col-md-12 col-sm-12'
    wrapstyle = 'style="white-space: nowrap;"'
    filter_no_symbol = 'symbol <>"" AND'
    rightcol_line_sep = ''


    if sel == 0 and suid == 0:
        l_newsfeed_title = 'World News and Top Stories'
    if sel == 1 and suid == 0:
        l_newsfeed_title = 'Featured Articles'
    if sel == 1 and suid == 0 and show_chart == 0:
        l_newsfeed_title = 'Latest Articles and Analysis'
    if sel == 2 and suid == 0:
        l_newsfeed_title = 'News Top Selection'

    if show_chart == 1:
        if sel == 0:
            bsclass_left = 'col-lg-10 col-md-10 col-sm-10'
            bsclass_right = 'col-lg-2 col-md-2 col-sm-2'
        if sel == 1:
            bsclass_left = 'col-lg-8 col-md-7 col-sm-7'
            bsclass_right = 'col-lg-4 col-md-5 col-sm-5'
        if sel == 2:
            bsclass_left = 'col-lg-10 col-md-10 col-sm-10'
            bsclass_right = 'col-lg-2 col-md-2 col-sm-2'

    if show_chart == 0:
        if sel == 1:
            bsclass_left = 'col-lg-10 col-md-10 col-sm-10'
            bsclass_right = 'col-lg-2 col-md-2 col-sm-2'
            filter_no_symbol = ''

    query = ' '+\
    'SELECT DISTINCT short_title, '+\
    'short_description, '+\
    'url, badge, '+\
    'ranking, '+\
    '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time, symbol '+\
    'FROM feed '+\
    'WHERE '+\
    'type=3 '+\
    'AND '+\
    'symbol LIKE "%%" '+\
    'AND '+\
    'asset_class LIKE "%%" '+\
    'AND '+\
    'lang LIKE "%'+ str(lang) +'%" '+\
    'AND ranking < '+ str(ranking_filter) + ' ' +\
    'ORDER BY date DESC LIMIT '+ str(numline)

    if sel == 0:
        query = 'SELECT DISTINCT short_title, short_description, url, badge, ranking, '+\
        '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time, symbol '+\
        'FROM feed '+\
        'WHERE asset_class="" AND market="" AND lang LIKE "%'+ str(lang) +'%" '+\
        'AND ranking < '+ str(ranking_filter) +' AND type='+ str(feed_type) + ' ' +\
        'ORDER BY date DESC LIMIT '+ str(numline)

    if sel == 1:
        query = 'SELECT DISTINCT short_title, short_description, url, badge, ranking, '+\
        '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time, symbol '+\
        'FROM feed '+\
        'WHERE '+\
        str(filter_no_symbol) +' (asset_class LIKE "%'+\
        str(get_user_default_profile()) +'%" OR market LIKE "%'+\
        str(get_user_default_profile()) +'%") AND lang LIKE "%'+\
        str(lang) +'%" '+\
        'AND ranking <'+ str(ranking_filter) +' AND type='+ str(feed_type) + ' ' +\
        'ORDER BY date DESC LIMIT '+ str(numline)
        wrapstyle = 'style="font-size: 20px;" '
        if show_chart == 1:
            rightcol_line_sep = 'border-top:0.5px; border-top-style: dotted; '

    if sel == 2:
        query = ' '+\
        'SELECT DISTINCT short_title, short_description, url, badge, ranking, '+\
        '(SELECT ROUND((UNIX_TIMESTAMP() - UNIX_TIMESTAMP(date)) / 60) ) AS elapsed_time, symbol '+\
        'FROM feed '+\
        'WHERE symbol IN(SELECT DISTINCT portfolios.symbol FROM instruments '+\
        'JOIN portfolios ON instruments.symbol = portfolios.portf_symbol '+\
        'WHERE instruments.owner = (SELECT users.id FROM users WHERE uid = "'+\
        str(get_user()) +'") ) AND ranking < '+\
        str(ranking_filter) +' AND type='+\
        str(feed_type) + ' '+\
        'ORDER BY date DESC LIMIT '+ str(numline) +';'

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = query
    cursor.execute(sql)
    res = cursor.fetchall()
    newsrow = '<span class="sectiont"><i class="far fa-newspaper"></i>&nbsp;'+\
    l_newsfeed_title +'</span>'

    newnewscss = ''+\
    '<style>'+\
    '.blinkin {'+\
    ' -webkit-animation: inrow 2s 10; /* Safari 4+ */'+\
    '  -moz-animation:   inrow 2s 10; /* Fx 5+ */'+\
    '  -o-animation:     inrow 2s 10; /* Opera 12+ */'+\
    '  animation:        inrow 2s 10; /* IE 10+, Fx 29+ */'+\
    '}'+\
    '@-webkit-keyframes inrow {'+\
    '  0%, 49% {'+\
    '      background-color: darkblue;'+\
    '      color: white;'+\
    '  }'+\
    '}'+\
    '</style>'

    i = 1
    newsrow = newnewscss + newsrow + '<div class="row">'
    for row in res:
        unistr = 'x'+ str(get_random_str(10)) + 'x'

        url_href = go_to_url(str(row[2]), 'link', unistr)
        url_form = go_to_url(str(row[2]), 'form', unistr)

        news_title = str(row[0]) +' '+ str(row[3])
        news_ranking = row[4]
        news_date = get_elapsed_time(row[5])
        news_minutes = int(row[5])
        symbol = str(row[6])
        contextstyle = ''
        newnewsclass = ''
        if news_minutes <= 10:
            newnewsclass = 'blinkin'

        if news_ranking <= -0.8:
            contextstyle = theme_return_this('color: white; background-color: red;',
                                             'color: white; background-color: red;')
        if news_ranking > 0 and news_ranking <= 0.5:
            contextstyle = theme_return_this('color: black;', 'color: white;')

        news_content = str(row[1].replace('http://', 'https://')) +\
        ' <br /><br />'+ '<a '+ url_href  +' >'+ l_view_article +'</a>'

        if symbol != '':
            news_content = news_content +\
            '<br /><br /><div style="width: 100%; overflow-x: auto;">'+\
            get_signal_details(get_uid_from_symbol(symbol), burl, 'newsfeed') +\
            '</div>'

        newsrow = newsrow + url_form +\
        '    <div class="'+ bsclass_left +\
        ' col-xs-12" style="border-top:0.5px; border-top-style: dotted; "> '+\
        '       <div class="d-none d-sm-block" '+ wrapstyle +'>'+\
        '           <a '+ url_href +' style="'+\
        theme_return_this('color:black;', 'color:white;') +'" >'+\
        '<i class="fas fa-external-link-alt"></i></a>'+\
        '           <strong><a data-toggle="collapse" href="#'+\
        str(unistr)+'"  style="'+\
        contextstyle +'" class="'+\
        newnewsclass +'" >'+ '&nbsp;<span style="'+\
        theme_return_this('color:black;', 'color:#00ffff;') +' ">'+\
            str(news_date) +'</span>&nbsp;' +\
            news_title  + '</a></strong>&nbsp;'+\
        '       </div>'+\
        '       <div class="d-sm-none" >'+\
        '           <a '+ url_href +' style="'+\
        theme_return_this('color:black;', 'color:white;') +\
        '" ><i class="fas fa-external-link-alt"></i></a>'+\
        '           <strong><a data-toggle="collapse" href="#'+\
        str(unistr)+'"  style="'+\
        contextstyle +'" class="'+\
        newnewsclass +'" >'+ '&nbsp;<span style="'+\
        theme_return_this('color:black;', 'color:#00ffff;') +' ">'+\
            str(news_date) +'</span>&nbsp;' +\
            news_title  + '</a></strong>&nbsp;'+\
        '       </div>'+\
        '       <div class="collapse" id="'+ str(unistr) +'">'+ news_content +'<br /><br /></div>'+\
        '    </div>'+\
        '    <div class="'+ bsclass_right +\
        ' col-xs-1 d-none d-sm-block" style="'+\
        theme_return_this('background-color:white;',
                          'background-color:black;') + ' ' + rightcol_line_sep +'" >'+\
        draw_feed_chart(sel, show_chart, news_ranking, symbol) +\
        '    </div>'
        i += 1
    newsrow = newsrow + '</div>'
    cursor.close()
    connection.close()

    return_data = newsrow
    return return_data

def draw_feed_chart(sel, show_chart, score, symbol):
    """ xxx """
    return_data = ''
    if show_chart == 1:
        if sel == 0:
            return_data = get_sentiment_progressbar(score)
        if sel == 1:
            return_data = get_tradingview_single_ticker(get_uid(str(symbol)))
        if sel == 2:
            return_data = get_sentiment_progressbar(score)
    if show_chart == 0:
        if sel == 1:
            return_data = get_sentiment_progressbar(score)
    return return_data

def get_sentiment_progressbar(score):
    """ xxx """
    return_data = ''
    pos = 0
    neg = 0
    if score < 0:
        pos = 1+score
        neg = abs(score)
    if score > 0:
        pos = score
        neg = 1-score
    pos = pos *100
    neg = neg *100

    content = ' '+\
    '<div class="progress" style="width: 100%;">'+\
    '  <div class="progress-bar bg-success progress-bar-striped" '+\
    'role="progressbar" style="width: '+\
    str(pos) +'%" aria-valuenow="'+\
    str(pos) +'" aria-valuemin="0" aria-valuemax="100"></div>'+\
    '  <div class="progress-bar bg-danger progress-bar-striped" '+\
    'role="progressbar" style="width: '+\
    str(neg) +'%" aria-valuenow="'+\
    str(neg) +'" aria-valuemin="0" aria-valuemax="100"></div>'+\
    '</div>'
    return_data = content
    return return_data
