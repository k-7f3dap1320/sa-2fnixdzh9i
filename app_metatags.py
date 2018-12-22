# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_stylesheet import *
from sa_func import *

def get_metatags(burl):
    theme_color = '<meta name="theme-color" content="'+ get_theme_color() +'" />'
    favicon = '<link rel="icon" href="static/favicon.ico?r='+ get_random_str(9) +'">'

    r = theme_color +\
        favicon

    return r
