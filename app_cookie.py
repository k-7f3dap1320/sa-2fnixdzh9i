# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import Flask, make_response, request, redirect
from app_page import *
from app_head import *
from app_body import *

def set_sa_ref_code(ref,c):
    try:
        resp = make_response( c )
        ref_str = ref
        if len(ref_str) > 1: ref_str = str(ref)
        resp.set_cookie('ref_by', str(ref_str) )
    except Exception as e: print(e)
    return resp

def set_sa_cookie(usr,ref):
    try:
        resp = make_response( redirect("/") )
        user_uid = '0'; ref_str = '0'
        if len(usr) > 1: user_uid = str(usr)
        if len(ref_str) > 1: ref_str = str(ref)
        resp.set_cookie('user', str(user_uid) )
        resp.set_cookie('ref_by', str(ref_str) )
        print('user_id=' + user_uid )
    except Exception as e: print(e)
    return resp

def user_get_uid():
    return request.cookies.get('user')

def user_is_login():

    user_id = '0'
    r = 0
    try:
        user_id = request.cookies.get('user')
        print('THIS IS USER_ID = ' + str(user_id) )
        if len(user_id) > 1 : r = 1
    except Exception as e: print(e)
    print('user is logged in: '+ str(r) )

    return r

def user_logout(burl):

    resp = ''
    try:
        resp = make_response( redirect("/") )
        resp.set_cookie('user', '0')
    except Exception as e: print(e)

    return resp

def get_refer_by_code():

    refer_by_code = ''
    try:
        refer_by_code = request.cookies.get('ref_by')
    except Exception as e: print(e)

    return refer_by_code
