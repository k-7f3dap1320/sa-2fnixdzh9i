# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def get_page_footer(burl):

    box_content = ''

    try:

        box_content = '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '               <br /><br /><br /><strong>'+\
        '               <span><a href="'+ burl +'static/taatu/index.html" target="_blank">About Us</a></span>' +\
        '               <br /><br /><br /><br /></strong>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '               <br /><br /><br /><strong>'+\
        '               <span><a href="'+ burl +'static/taatu/index.html#contact" target="_blank">Contact Us</a></span>' +\
        '               <br /><br /><br /><br /></strong>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '               <br /><br /><br /><strong>'+\
        '               <span><a href="'+ burl +'static/taatu/index.html#contact" target="_blank">SmartAlpha for Business</a></span>' +\
        '               <br /><br /><br /><br /></strong>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '               <br /><br /><br /><strong>'+\
        '               <span><a href="'+ burl +'static/taatu/index.html#tc" target="_blank">Terms and Conditions</a></span>' +\
        '               <br /><br /><br /><br /></strong>'+\
        '            </div>'+\
        '        </div>'+\
        '   <div class="row">'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


    except Exception as e: print(e)

    return box_content
