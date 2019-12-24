""" Application main module """
DEV_MODE = False

from flask import Flask, request, redirect
from flask_compress import Compress
from app_main import gen_main_page
from app_login import user_login
from portf_main import gen_portf_page
from signal_main import gen_sign_page
from app_widget import get_widget_page
from createuser_main import gen_createuser_page
from select_market import gen_selectmarket_page, save_selectmarket
from createportf_main import gen_selectportf_page, save_portf_select, custom_save_portf_page
from portf_delete import del_portf
from portf_save import portf_save_conviction, portf_save
from app_head import get_head
from app_body import get_body
from app_page import set_page
from app_cookie import get_sa_theme, set_sa_lang
from app_cookie import set_sa_ref_code, set_sa_theme, user_logout
from sa_func import get_user_default_profile
from signin_main import get_signin_page
from view_list_instr_n_portf import gen_view_list_instr_n_portf
from payment_page import get_plan_selection_page
from error_page import get_error_page
from portf_gen_user_example import gen_portf_user_example, gen_portf_validate_content
from help_page import get_help_page
from intel_report import get_intel_page
from sa_terminal import get_sa_terminal_page
from sa_terminal_help import get_sa_terminal_help_page
from set_theme import theme_redirect
from app_settings import save_settings, get_settings_page
from app_search import get_search_page, get_search_result
from reset_password import get_resetpassword_page
from app_loading import get_loading_head, get_loading_body

application = Flask(__name__)

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6; COMPRESS_MIN_SIZE = 500; Compress(application)

@application.route('/')
@application.route('/s/', endpoint='s', methods=["POST", "GET"])
@application.route('/p/', endpoint='p', methods=["POST", "GET"])
@application.route('/ls/', endpoint='ls', methods=["POST", "GET"])
@application.route('/n/', endpoint='n', methods=["POST", "GET"])
@application.route('/join/', endpoint='join', methods=["POST", "GET"])
@application.route('/h/', endpoint='h', methods=["POST","GET"])
@application.route('/w/', endpoint='w', methods=["POST","GET"])
@application.route('/intelligence/', endpoint='intelligence', methods=["POST","GET"])
@application.route('/terminal/', endpoint='terminal', methods=["POST","GET"])
@application.route('/terminalhelp/', endpoint='terminalhelp', methods=["POST","GET"])
@application.route('/theme/', endpoint='theme', methods=["POST","GET"])
@application.route('/login/', endpoint='login', methods=["POST", "GET"])
@application.route('/logout/', endpoint='logout', methods=["POST", "GET"])
@application.route('/signin/', endpoint='signin', methods=["POST", "GET"])
@application.route('/genportf/', endpoint='genportf', methods=["POST","GET"])
@application.route('/pricing/', endpoint='pricing', methods=["POST","GET"])
@application.route('/settings/', endpoint='settings', methods=["POST","GET"])
@application.route('/reset/', endpoint='reset', methods=["POST","GET"])
@application.route('/search/', endpoint='search', methods=["POST","GET"])
@application.route('/error/', endpoint='error', methods=["POST","GET"])
@application.route('/url/', endpoint='url', methods=["POST","GET"])
@application.route('/w/url/', endpoint='url', methods=["POST","GET"])
@application.route('/join/url/', endpoint='url', methods=["POST","GET"])
@application.route('/pricing/url/', endpoint='url', methods=["POST","GET"])


def go():
    """ xxx """
    appname = 'SmartAlpha | Trading Intelligence'
    c = ''
    burl = request.url_root;
    if not DEV_MODE: 
        burl = burl.replace('http://','https://')

    uid = request.args.get('uid')
    ref = request.args.get('ref')
    lang = request.args.get('lang')
    nonavbar = request.values.get('nonavbar')
    terminal = request.args.get('terminal')
    x = request.args.get('x');


    err = request.args.get('err')

    ############################################################################
    if request.endpoint == 's':
        tvws = request.args.get('tvwidgetsymbol')
        c = gen_sign_page(uid, tvws, appname, burl, terminal)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'p':
        ins = request.values.get('ins')
        step = request.values.get('step')
        mode = request.values.get('mode')
        pop = request.values.get('pop')
        delete = request.values.get('delete')
        dashboard = request.values.get('dashboard')
        if ins != '' or ins != None:
            if x == '' or x == None : 
                x = get_user_default_profile()
        if ins == '1': 
            c = gen_selectportf_page(appname, burl, step, terminal)
        if ins == '2': 
            c = save_portf_select(burl, step, uid)
        if ins == '3': 
            c = custom_save_portf_page(appname, burl, terminal)
        if ins == '4': 
            c = portf_save_conviction(burl,mode,x)
        if ins == '5': 
            c = portf_save(burl)
        if ins is None: 
            c = gen_portf_page(uid,appname,burl,pop, terminal)
        if delete is not None: 
            c = del_portf(delete,burl,x,dashboard)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'ls':
        what = request.values.get('w')
        c = gen_view_list_instr_n_portf(appname, burl, what, x, terminal)

    elif request.endpoint == 'n':
        name = request.values.get('name')
        username = request.values.get('email')
        password = request.values.get('password')
        from_ip = request.values.get('from_ip')
        nickname = request.values.get('nickname')
        step = request.args.get('step')
        broker = request.args.get('broker')
        if broker is None: 
            broker = request.values.get('broker')
        broker_username = request.values.get('username_broker')
        mode = request.values.get('mode')
        if step == 'c': 
            c = gen_selectmarket_page(appname, burl, mode, terminal)
        elif step == 'd': 
            c= save_selectmarket(burl, x)
        else: 
            c = gen_createuser_page(uid,
                                    appname,
                                    burl,
                                    name,
                                    username,
                                    password,
                                    from_ip,broker,
                                    broker_username,
                                    terminal)

    elif request.endpoint == 'join':
        broker = request.args.get('broker')
        if broker is None: 
            broker = 'not-specified'
        c = gen_createuser_page('0',appname,burl,'','','','',broker,'', terminal)

    elif request.endpoint == 'h':
        c = get_help_page(appname, burl, terminal)

    elif request.endpoint == 'w':
        funcname = request.values.get('funcname')
        refreshw = request.values.get('refreshw')
        noflexheight = request.values.get('noflexheight')
        c = get_widget_page(appname,
                            burl,
                            nonavbar,
                            funcname,
                            refreshw,
                            noflexheight,
                            terminal)

    elif request.endpoint == 'intelligence':
        c = get_intel_page(appname, burl, terminal)

    elif request.endpoint == 'terminal':
        c = get_sa_terminal_page(appname,burl, terminal)

    elif request.endpoint == 'terminalhelp':
        c = get_sa_terminal_help_page(appname,burl, terminal)

    elif request.endpoint == 'theme':
        switch_to = ''
        if get_sa_theme() == 'dark':
            switch_to = 'light'
        else:
            switch_to = 'dark'
        c = theme_redirect(burl, terminal)
        c = set_sa_theme(switch_to, c )

    elif request.endpoint == 'login':
        user = request.values.get('user')
        password = request.values.get('password')
        redirect_to = request.values.get('redirect')
        c = user_login(user,password, burl, redirect_to)

    elif request.endpoint == 'logout':
        c = user_logout(burl)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'signin':
        redirect_to = request.values.get('redirect')
        c = get_signin_page(appname, burl, err, redirect_to, terminal)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'pricing':
        c = get_plan_selection_page(appname, burl, terminal)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'settings':
        step = request.args.get('step')
        name = request.values.get('name')
        nickname = request.values.get('nickname')
        username = request.values.get('username')
        default_profile = request.values.get('default_profile')
        email_subscription = request.values.get('email_subscription')
        message = save_settings(name,nickname,username,default_profile,email_subscription)
        c = get_settings_page(appname, burl, step, message, terminal)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'reset':
        step = request.args.get('step')
        data = request.values.get('data')
        data2 = request.values.get('data2')
        c = get_resetpassword_page(appname,
                                   burl,
                                   step,
                                   data,
                                   data2,
                                   terminal)

    elif request.endpoint == 'search':
        nonavbar = request.args.get('nonavbar')
        c = get_search_page(appname,burl,nonavbar, terminal)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'genportf':
        acm = request.args.get('acm')
        step = request.args.get('step')
        notstart = request.args.get('notstart')
        if step == '1': 
            c = gen_portf_user_example(burl,acm,notstart)
        if step == '2': 
            c = gen_portf_validate_content(burl,notstart)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'error':
        c = get_error_page(appname, burl, terminal)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)

    elif request.endpoint == 'url':
        url_q = request.values.get('q')
        c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + str(url_q) + '" />') + get_body('','') )
    else:
        if x == '' or x == None : x = get_user_default_profile()
        dashboard = request.args.get('dashboard')
        tour = request.args.get('tour')
        c = gen_main_page(x,appname,burl,dashboard,tour,nonavbar, terminal)
        c = set_sa_lang(lang,c)
        c = set_sa_ref_code(ref,c)
    ############################################################################

    sid = request.args.get('sid')
    if sid is None: sid = ''
    q = request.args.get(sid)
    if len(sid)>5:
        c = get_search_result(q, burl, nonavbar)


    if not DEV_MODE:
        if burl.find('https://app.') == -1:
            if burl.find('https://www.') > -1:
                burl = burl.replace('https://www.','https://app.')
            else:
                burl = burl.replace('https://','https://app.')
            c = set_page( get_head(get_loading_head() + '<script>window.location = "'+ burl +'";</script>' ) + get_body( get_loading_body() , '' ) )

    return c

#@application.errorhandler(500)
#def error_handler(error):
    #return redirect(request.url_root + 'error', code=302)
#    return 'error'

if __name__ == '__main__':
    #For dev_mode and testing --> application.run(host='0.0.0.0', port=80, threaded=True)
    #For AWS Beanstalk --> application.run()
    if not DEV_MODE:
        application.run()
    else:
        application.run(host='0.0.0.0', port=80, threaded=True)
