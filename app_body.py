""" html body """
def get_body(outside_container, content, style):
    """ xxx """
    if style != '':
        style = ' style="'+ style +'"'
    return_data = '<body'+ style +'>'+ outside_container +\
    '<div class="container-fluid" id="content">'+ content +'</div></body>'
    return return_data
