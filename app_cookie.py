
from flask import Flask, make_response, request, redirect
from app_page import *
from app_head import *
from app_body import *
import datetime
import time
from datetime import timedelta

def get_lang():
    return request.cookies.get('lang')

def set_sa_lang(lang,c):
    resp = make_response( c )
    if lang is None: lang = 'en'
    resp.set_cookie('lang', str(lang), expires=datetime.datetime.now() + datetime.timedelta(days=500) )
    return resp

def set_sa_theme(theme,c):
    resp = make_response( c )
    if theme is None: theme = default_theme
    resp.set_cookie('theme', str(theme), expires=datetime.datetime.now() + datetime.timedelta(days=500))
    return resp

def get_sa_theme():
    default_theme = 'dark'
    selected_theme = ''
    selected_theme = request.cookies.get('theme')
    if selected_theme is None or selected_theme =='': selected_theme = default_theme
    return selected_theme

def theme_return_this(for_light,for_dark):
    return_data = ''
    if get_sa_theme() == 'light':
        return_data = for_light
    else:
        return_data = for_dark
    return return_data

def set_sa_ref_code(ref,c):
    resp = make_response( c )
    ref_str = ref
    if len(ref_str) > 1: ref_str = str(ref)
    resp.set_cookie('ref_by', str(ref_str), expires=datetime.datetime.now() + datetime.timedelta(days=500) )
    return resp

def set_sa_cookie(uid,c):
    resp = make_response( c )
    user_uid = '0';
    if len(uid) > 1: user_uid = str(uid)
    resp.set_cookie('user', str(user_uid), expires=datetime.datetime.now() + datetime.timedelta(days=20) )
    return resp

def user_get_uid():
    return_data = request.cookies.get('user')
    if return_data is None: return_data = 0
    return return_data

def user_is_login():
    user_id = '0'
    return_data = 0
    user_id = request.cookies.get('user')
    if len(user_id) > 1 : return_data = 1
    return return_data

def get_refer_by_code():
    refer_by_code = ''
    refer_by_code = request.cookies.get('ref_by')
    return refer_by_code
