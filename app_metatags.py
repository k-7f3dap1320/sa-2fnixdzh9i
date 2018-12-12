# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_stylesheet import *

def get_metatags():
    theme_color = '<meta name="theme-color" content="'+ get_theme_color() +'" />'

    return theme_color
