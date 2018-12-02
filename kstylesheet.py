# Copyright (c) 2018-present, Kahroo LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


def get_stylesheet():


    body = 'body{background: #eee;}'
    desc = '.desc{font-size:19px;}'
    expl = '.expl{font-size:10px;}'
    box = '.box{padding:60px 0px;}'
    boxpart = '.box-part{background:#FFF; border-radius:0; padding:60px 10px; margin:30px 0px;}'
    text = '.text{margin:20px 0px;}'


    r = '<style>'+ body + desc + expl + box + boxpart + text + '</style>'


    return r
