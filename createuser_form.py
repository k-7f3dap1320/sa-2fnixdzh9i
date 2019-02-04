# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from sa_func import *
from sa_db import *
from app_cookie import *


def get_user_ip_input():
    r = ''
    try:
        r = '' +\
        '<script type="application/javascript">'+\
        '  function getIP(json) {'+\
        '    document.write("<input type=\"hidden\" value=\" ", json.ip,"\" id=\"from_ip\" name=\"from_ip\">");'+\
        '  }'+\
        '</script>'+\
        '<script type="application/javascript" src="https://api.ipify.org?format=jsonp&callback=getIP"></script>'

    except Exception as e:
        print(e)
    return r


def get_user_creation_form(burl):

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part">'+\
        '     <form method="POST" action="'+ burl +'n/?uid='+ get_random_str(99)  +'" style="width: 100%; max-width: 600px; padding: 2%; margin: auto;">'+\
        '         <div>'+\
        '            <div>'+\
        '<div style="text-align: center;"><img src="'+ burl +'static/logo_light.png?'+ get_random_str(9) +'" height="88"></div>'+\
        '                <hr>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '               <div class="input-group input-group-lg">'+\
        '                 <div class="input-group-prepend">'+\
        '                   <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-user-alt" style="font-size: large;"></i></span>'+\
        '                 </div>'+\
        '                 <input type="text" id="name" name="name" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="Your name" required autofocus>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '               <div class="input-group input-group-lg">'+\
        '                 <div class="input-group-prepend">'+\
        '                   <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-at" style="font-size: large;"></i></span>'+\
        '                 </div>'+\
        '                 <input type="email" id="email" name="email" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="Your email: you@example.com" required autofocus>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '               <div class="input-group input-group-lg">'+\
        '                 <div class="input-group-prepend">'+\
        '                   <span class="input-group-text" id="inputGroup-sizing-lg"><i class="fa fa-key" style="font-size: large;"></i></span>'+\
        '                 </div>'+\
        '                 <input type="password" id="password" name="password" class="form-control" aria-label="Large" aria-describedby="inputGroup-sizing-sm" placeholder="Password" required>'+\
        '               </div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div>'+\
        '            <div>'+\
        '                <div>&nbsp;</div>'+\
        get_user_ip_input() +\
        '                <button type="submit" class="btn btn-info btn-lg btn-block form-signin-btn"><i class="fa fa-user-plus"></i> Sign up</button>'+\
        '            </div>'+\
        '        </div>'+\
        '<div class="expl" style="text-align: center;">*We respect your privacy and will never share your email address with any person or organization.</div>'+\
        '    </form>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'


        box_content = box_content + '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part" style="padding: 30px; height:250px">'+\
        '               <div>&nbsp;</div>'+\
        '               <h5>Taatu Ltd.</h5>'+\
        '               <div>27 Old Gloucester Street</div>'+\
        '               <div>London</div>'+\
        '               <div>WC1N 3AX</div>'+\
        '               <div>United Kingdom</div>'+\
        '               <div>&nbsp;</div>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12">'+\
        '            <div class="box-part" style="padding: 30px; height:250px">'+\
        '               <div>&nbsp;</div>'+\
        '               <h5>Contact us, we love feedback</h5>'+\
        '               <div>e: <a href="mailto:info@taatu.co">info@taatu.co</a></div>'+\
        '               <div>w: <a href="http://taatu.co">www.taatu.co</a></div>'+\
        '               <div>&nbsp;</div>'+\
        '               <div>Do you have any problem to log in? Drop us an <a href="mailto:info@taatu.co">email</a> or talk with us on <a href="https://www.facebook.com/messages/t/taatuco" target="_blank">messenger</a>.</div>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content
