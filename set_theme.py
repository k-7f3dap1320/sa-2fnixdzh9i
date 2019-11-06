
from app_head import get_head
from app_body import get_body
from app_page import set_page

def theme_redirect(burl):
    return_data = ''
    return_data = set_page( get_head('<meta http-equiv="refresh" content="0;URL=' + burl +'" />') + get_body('','') )
    return return_data
