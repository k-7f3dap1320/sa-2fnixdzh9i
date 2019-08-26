# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *

def get_bootstrap(theme,burl):

    bootcss_url = 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'
    bootcss_integrity = 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO'
    bootcss_dark_url =burl + 'static/bootstrap_custom_dark.css?' + get_random_str(10)
    selected_bootcss = ''

    if theme == 'dark':
        selected_bootcss = bootcss_dark_url
        bootcss_integrity = ''
    else:
        selected_bootcss = bootcss_url
    
    jquery = '<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>'
    popper = '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>'
    bootcss = '<link rel="stylesheet" href="'+ selected_bootcss +'" integrity="" crossorigin="anonymous">'
    bootsmin = '<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="'+ bootcss_integrity +'" crossorigin="anonymous"></script>'
    tooltip ="<script>$(function () {$('[data-toggle=\"tooltip\"]').tooltip()})</script>"

    r = jquery + popper + bootcss + bootsmin + tooltip

    return r
