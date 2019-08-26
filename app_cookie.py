# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import Flask, make_response, request, redirect
from app_page import *
from app_head import *
from app_body import *
import datetime
import time
from datetime import timedelta

def set_sa_lang(lang,c):
    try:
        resp = make_response( c )
        if lang is None: lang = 'en'
        resp.set_cookie('lang', str(lang), expires=datetime.datetime.now() + datetime.timedelta(days=500) )
    except Exception as e: print(e)
    return resp

def set_sa_theme(theme,c):
    try:
        default_theme = 'dark'
        resp = make_response( c )
        if theme is None: theme = default_theme
        resp.set_cookie('theme', str(theme), expires=datetime.datetime.now() + datetime.timedelta(days=500))
    except Exception as e: print(e)
    return resp

def get_sa_theme():
    selected_theme = ''
    try:
        selected_theme = request.cookies.get('theme')
    except Exception as e: print(e)
    return selected_theme

def set_sa_ref_code(ref,c):
    try:
        resp = make_response( c )
        ref_str = ref
        if len(ref_str) > 1: ref_str = str(ref)
        resp.set_cookie('ref_by', str(ref_str), expires=datetime.datetime.now() + datetime.timedelta(days=500) )
    except Exception as e: print(e)
    return resp

def set_sa_cookie(uid,c):
    try:
        resp = make_response( c )
        user_uid = '0';
        if len(uid) > 1: user_uid = str(uid)
        resp.set_cookie('user', str(user_uid), expires=datetime.datetime.now() + datetime.timedelta(days=500) )
    except Exception as e: print(e)
    return resp

def user_get_uid():
    return request.cookies.get('user')

def user_is_login():
    user_id = '0'
    r = 0
    try:
        user_id = request.cookies.get('user')
        if len(user_id) > 1 : r = 1
    except Exception as e: print(e)
    return r

def get_refer_by_code():
    refer_by_code = ''
    try:
        refer_by_code = request.cookies.get('ref_by')
    except Exception as e: print(e)
    return refer_by_code
