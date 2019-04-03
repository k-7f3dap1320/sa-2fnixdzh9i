# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from app_head import *; from app_body import *; from app_page import *; from app_loading import *
from app_footer import *
from app_ogp import *
from app_title import *; from app_metatags import *; from bootstrap import *
from awesomplete import *; from font_awesome import *; from app_navbar import *
from googleanalytics import *; from tablesorter import *

def get_box_plan_selection(burl):

    box_content = ''

    try:

        box_content = '<div class="box-top">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '            <div class="box-part rounded sa-center-content">'+\
        '<table class="table table-hover table-sm sa-table-sm">'+\
        '  <thead>'+\
        '    <tr>'+\
        '      <th scope="col">Features</th>'+\
        '      <th scope="col"><h6>SmartAlpha Basic</h6><h2>Free</h2></th>'+\
        '      <th scope="col"><h6>SmartAlpha Premium</h6><h2>USD 5.00<sup> / month</sup></h2></th>'+\
        '      <th scope="col"><h6>SmartAlpha Professional</h6><h2>USD 20.00<sup>/month</sup></h2></th>'+\
        '    </tr>'+\
        '  </thead>'+\
        '  <tbody>'+\
        '    <tr>'+\
        '      <td scope="row">No Ads</td>'+\
        '      <td>&nbsp;</td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row">Last 3-day signals with open orders and closed trades</td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td>&nbsp;</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row">Create portfolios, backtest and simulate performance</td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td>&nbsp;</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row">All trading signals with instant email notifications</td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td>&nbsp;</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row">Concrete and precise trading instruction report</td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td>&nbsp;</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row">Daily personalized trading intelligence report</td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td>&nbsp;</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row">Dedicated account manager to support your trading desk</td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td>&nbsp;</td>'+\
        '    </tr>'+\
        '    <tr>'+\
        '      <td scope="row">Get paid if ranked in the top 50 traders of the month</td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td><i class="fas fa-check-circle"></i></td>'+\
        '      <td>&nbsp;</td>'+\
        '    </tr>'+\
        '  </tbody>'+\
        '</table>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'

    except Exception as e: print(e)

    return box_content


def get_plan_selection_page(appname,burl):
    r = ''
    try:
        r = get_head( get_loading_head() + get_googleanalytics() + get_title( appname ) + get_metatags(burl) + set_ogp(burl,1,'','') + get_bootstrap() + get_awesomplete() + get_tablesorter() + get_font_awesome() + get_stylesheet(burl) )
        r = r + get_body( get_loading_body(), navbar(burl) + get_box_plan_selection(burl) + get_page_footer(burl) )
        r = set_page(r)
    except Exception as e: print(e)

    return r
