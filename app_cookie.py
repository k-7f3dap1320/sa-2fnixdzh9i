""" Manage cookies """
import datetime
from flask import make_response, request

def get_lang():
    """ xxx """
    return request.cookies.get('lang')

def set_sa_lang(lang, val):
    """ xxx """
    resp = make_response(val)
    if lang is None:
        lang = 'en'
    resp.set_cookie('lang', str(lang),
                    expires=datetime.datetime.now() + datetime.timedelta(days=500))
    return resp

def get_default_theme():
    """ xxx """
    return 'dark'

def set_sa_theme(theme, val):
    """ xxx """
    resp = make_response(val)
    if theme is None:
        theme = get_default_theme()
    resp.set_cookie('theme', str(theme),
                    expires=datetime.datetime.now() + datetime.timedelta(days=500))
    return resp

def get_sa_theme():
    """ xxx """
    default_theme = get_default_theme()
    selected_theme = ''
    selected_theme = request.cookies.get('theme')
    if selected_theme is None or selected_theme == '':
        selected_theme = default_theme
    return selected_theme

def theme_return_this(for_light, for_dark):
    """ xxx """
    return_data = ''
    if get_sa_theme() == 'light':
        return_data = for_light
    else:
        return_data = for_dark
    return return_data

def set_sa_ref_code(ref, content):
    """ xxx """
    resp = make_response(content)
    if ref is None:
        ref = ''
    ref_str = ref
    if len(ref_str) > 1:
        ref_str = str(ref)
    resp.set_cookie('ref_by', str(ref_str),
                    expires=datetime.datetime.now() + datetime.timedelta(days=500))
    return resp

def set_sa_cookie(uid, val):
    """ xxx """
    resp = make_response(val)
    user_uid = '0'
    if len(uid) > 1:
        user_uid = str(uid)
    resp.set_cookie('user', str(user_uid),
                    expires=datetime.datetime.now() + datetime.timedelta(days=20))
    return resp

def user_get_uid():
    """ xxx """
    return_data = request.cookies.get('user')
    if return_data is None:
        return_data = 0
    return return_data

def user_is_login():
    """ xxx """
    user_id = '0'
    return_data = 0
    user_id = request.cookies.get('user')
    if user_id is None:
        user_id = ''
    if len(user_id) > 1:
        return_data = 1
    return return_data

def get_refer_by_code():
    """ xxx """
    refer_by_code = ''
    refer_by_code = request.cookies.get('ref_by')
    return refer_by_code
