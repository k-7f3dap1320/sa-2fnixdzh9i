# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from flask import Flask, make_response, request
from app_page import *
from app_head import *
from app_body import *


def set_sa_cookie(usr,ref):
    r = False
    try:
        resp = make_response(None)
        user_uid = '0'; ref_str = '0'
        if len(usr) > 1: user_uid = str(usr)
        if len(ref_str) > 1: ref_str = str(ref)
        resp.set_cookie('user', str(user_uid) )
        resp.set_cookie('ref_by', str(ref_str) )
        r = True
    except Exception as e: print(e)

    return r

def user_get_uid():
    return = request.cookies.get('user')
    
def user_is_login():

    user_id = None
    r = False
    try:
        user_id = request.cookies.get('user')
    except Exception as e: print(e)

    if not user_id == None or not user_id == '0' : r = True
    return r

def user_logout(burl):

    resp = ''
    try:
        resp = make_response( set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + str(burl) + '" />') + get_body('','') ) )
        resp.set_cookie('user', '0')
    except Exception as e: print(e)

    return resp

def get_refer_by_code():

    refer_by_code = ''
    try:
        refer_by_code = request.cookies.get('ref_by')
    except Exception as e: print(e)

    return refer_by_code
