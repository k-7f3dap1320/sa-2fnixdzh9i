# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def get_page_footer(burl):

    box_content = ''

    try:

        box_content = '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="sa-center-content footer">'+\
        '               <span><a href="'+ burl +'static/taatu/index.html" target="_blank">About Us</a></span>&nbsp;&nbsp;&nbsp;&nbsp;' +\
        '               <span><a href="'+ burl +'static/taatu/index.html#contact" target="_blank">Contact Us</a></span>&nbsp;&nbsp;&nbsp;&nbsp;' +\
        '               <span><a href="'+ burl +'static/taatu/index.html#tc" target="_blank">Terms and Conditions</a></span>&nbsp;&nbsp;&nbsp;&nbsp;' +\
        '<br /><br /><br /><br />'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


    except Exception as e: print(e)

    return box_content
