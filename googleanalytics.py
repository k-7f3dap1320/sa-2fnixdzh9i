""" Google Analytics Library """

def get_googleanalytics():
    """ Get Google Analytics script """
    google_anal_id = 'UA-100755106-1'
    ganal = ' '+\
                '<script async src="https://www.googletagmanager.com/gtag/js?id='+\
                str(google_anal_id) +'"></script>'+\
                '<script>'+\
                '   window.dataLayer = window.dataLayer || [];'+\
                '   function gtag(){dataLayer.push(arguments);}'+\
                '       gtag("js", new Date());'+\
                '       gtag("config", "UA-100755106-1");'+\
                '</script>'
    return_data = ganal

    return return_data
