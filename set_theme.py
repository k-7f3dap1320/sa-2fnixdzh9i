""" Application theme selection """
from app_head import get_head
from app_body import get_body
from app_page import set_page

def theme_redirect(burl, terminal):
    """ xxx """
    return_data = ''
    if terminal is None:
        redirect_terminal = ''
    else:
        redirect_terminal = 'terminal'

    return_data = set_page(get_head('<meta http-equiv="refresh" content="0;URL=' +\
                                     burl +'?'+ redirect_terminal +\
                                     '" />') + get_body('', '', ''))
    return return_data
