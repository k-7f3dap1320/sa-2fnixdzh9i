""" html body """
def get_body(outside_container, content):
    """ xxx """
    return_data = '<body>'+ outside_container +\
    '<div class="container-fluid" id="content">'+ content +'</div></body>'
    return return_data
