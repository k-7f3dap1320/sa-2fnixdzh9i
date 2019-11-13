""" Loading page display animation """
def get_loading_body():
    """ xxx """
    return_data = '<div id="load"></div>'
    return return_data

def get_loading_head():
    """ xxx """
    loading_script = '<script>'+\
    'document.onreadystatechange = function () {'+\
    '   var state = document.readyState;'+\
    '   if (state == "interactive") {'+\
    '        document.getElementById("content").style.visibility="hidden";'+\
    '   } else if (state == "complete") {'+\
    '   setTimeout(function(){'+\
    '       document.getElementById("interactive");'+\
    '       document.getElementById("load").style.visibility="hidden";'+\
    '       document.getElementById("content").style.visibility="visible";'+\
    '    },10);}}'+\
    '</script>'
    return loading_script
