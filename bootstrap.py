""" bootstrap framework """
from sa_func import *

def get_bootstrap(theme,burl):
    """ Load Bootstrap frontend framework """

    bootcss_url = 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'
    bootcss_dark_url = burl + 'static/bootstrap_custom_dark.css?' + get_random_str(10)
    selected_bootcss = ''

    if theme == 'light':
        selected_bootcss = bootcss_url
    else:
        selected_bootcss = bootcss_dark_url

    jquery = '<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>'
    popper = '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>'
    bootcss = '<link rel="stylesheet" href="'+ selected_bootcss +'" >'
    bootsmin = '<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>'
    tooltip ="<script>$(function () {$('[data-toggle=\"tooltip\"]').tooltip()})</script>"

    return_data = jquery + popper + bootcss + bootsmin + tooltip

    return return_data
