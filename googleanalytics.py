# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def get_googleanalytics():

    ga = '<!-- Global site tag (gtag.js) - Google Analytics -->'+\
                '<script async src="https://www.googletagmanager.com/gtag/js?id=UA-100755106-1"></script>'+\
                '<script>'+\
                '   window.dataLayer = window.dataLayer || [];'+\
                '   function gtag(){dataLayer.push(arguments);}'+\
                '       gtag("js", new Date());'+\
                '       gtag("config", "UA-100755106-1");'+\
                '</script>'
    r = ga

    return r
