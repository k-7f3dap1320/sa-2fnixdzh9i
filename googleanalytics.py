
def get_googleanalytics():

    ga = '<!-- Global site tag (gtag.js) - Google Analytics -->'+\
                '<script async src="https://www.googletagmanager.com/gtag/js?id=UA-100755106-1"></script>'+\
                '<script>'+\
                '   window.dataLayer = window.dataLayer || [];'+\
                '   function gtag(){dataLayer.push(arguments);}'+\
                '       gtag("js", new Date());'+\
                '       gtag("config", "UA-100755106-1");'+\
                '</script>'
    return_data = ga

    return return_data
