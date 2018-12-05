# Copyright (c) 2018-present, Kahroo LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from page import *
from head import *
from title import *
from body import *
from bootstrap import *
from google_chart import *
from kstylesheet import *
from awesomplete import *
from knavbar import *
from kcard import *

def gen_main_page(x):

    r = get_head( get_title('Kahroo - Market intelligence') + get_bootstrap() + get_awesomplete() + get_google_chart_script() + get_stylesheet() )
    r = r + get_body( navbar() + get_card(x,9) + get_card(x,1) )
    r = set_page(r)

    return r
