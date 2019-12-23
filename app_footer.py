""" Footer of the page """
from app_cookie import user_is_login

def get_page_footer(burl, force_display):
    """ xxx """
    box_content = ''
    if user_is_login() == 0 or force_display:
        box_content = ' '+\
        '<div class="box">' +\
        '   <div class="row">'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '               <br /><br /><strong>'+\
        '               <span style="font-size:large;"><a href="'+\
        burl +'static/taatu/index.html" target="_blank" '+\
        'class="text-info">Company</a></span>' +\
        '               <br /><br /></strong>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '               <br /><br /><strong>'+\
        '               <span style="font-size:large;"><a href="'+\
        burl +'static/taatu/index.html#contact" target="_blank" '+\
        'class="text-info">Contact Us</a></span>' +\
        '               <br /><br /></strong>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '               <br /><br /><strong>'+\
        '               <span style="font-size:large;"><a href="'+\
        burl +'static/taatu/index.html#business" target="_blank" '+\
        'class="text-info">Products and Services</a></span>' +\
        '               <br /><br /></strong>'+\
        '            </div>'+\
        '        </div>'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '               <br /><br /><strong>'+\
        '               <span style="font-size:large;"><a href="'+\
        burl +'static/taatu/index.html#tc" target="_blank" '+\
        'class="text-info">Terms and Conditions</a></span>' +\
        '               <br /><br /></strong>'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '   <div class="row">'+\
        '        <div class="col-lg-2 col-md-2 col-sm-1 col-xs-1">'+\
        '            <div class="sa-center-content footer">'+\
        '            </div>'+\
        '        </div>'+\
        '   </div>'+\
        '</div>'+\
        '<hr />'+\
        '<div class="box">'+\
        '   <div class="row">'+\
        '      <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">'+\
        '           <div class="sa-center-content text-secondary">'+\
        'Made with <i class="fas fa-heart"></i> '+\
        'from London, Nairobi to Bangkok - <span class="text-muted">'+\
        'Copyright &copy; Taatu Ltd. 2019</span></div>'+\
        '      </div>'+\
        '   </div>'+\
        '</div>'+\
        '<br /><br /><br /><br />'
    return box_content
