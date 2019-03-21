# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *

def set_ogp(burl,type):
    try:

        r = '' +\
        '<meta property="og:title" content="A.I. Powered Trading Insights">'+\
        '<meta property="og:site_name" content="SmartAlpha Trade">'+\
        '<meta property="og:url" content="http://smartalphatrade.com">'+\
        '<meta property="og:description" content="SmartAlpha will help you to turn any trading portfolio into a profitable one.">'+\
        '<meta property="og:type" content="article">'+\
        '<meta property="og:image" content="'+ burl +'static/ogp.png?'+ get_random_num(9) +'">'

    except Exception as e: print(e)
    return r
