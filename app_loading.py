# Copyright (c) 2018-present, Project K
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *


def get_loading_body():

    r = '<div id="load"></div>'
    return r

def get_loading_head():

    loading_script = '<script>'+\
    'document.onreadystatechange = function () {'+\
    '   var state = document.readyState;'+\
    '   if (state == "interactive") {'+\
    '        document.getElementById("content").style.visibility="hidden";'+\
    '   } else if (state == "complete") {'+\
    '   setTimeout(function(){'+\
    '       document.getElementById("interactive");'+\
    '       document.getElementById("load").style.visibility="hidden";'+\
    '       document.getElementById("content").style.visibility="visible";'+\
    '    },10);}}'+\
    '</script>'

    return loading_script
