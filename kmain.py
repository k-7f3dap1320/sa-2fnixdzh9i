# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from kfunc import *
aps = app_settings()

from page import *
from head import *
from metatags import *
from title import *
from body import *
from bootstrap import *
from google_chart import *
from kloading import *
from kstylesheet import *
from awesomplete import *
from knavbar import *
from kcard import *

def gen_main_page(x):

    r = get_head( get_loading_head() + get_title( aps.get_app_name() +' - Market intelligence') + get_metatags() + get_bootstrap() + get_awesomplete() + get_google_chart_script() + get_stylesheet() )
    r = r + get_body( get_loading_body(), navbar() + get_card(x,9) + get_card(x,1) )
    r = set_page(r)

    return r
