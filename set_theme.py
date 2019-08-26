# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *
from sa_func import *
from app_cookie import *



def theme_redirect(burl):
    c = ''
    try:
        c = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl +'" />') + get_body('','') )
    except Exception as e: print(e)
    return c
