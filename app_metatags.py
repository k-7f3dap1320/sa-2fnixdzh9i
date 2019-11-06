
from app_stylesheet import get_theme_color
from sa_func import get_random_str

def get_metatags(burl):
    charset = '<meta charset="UTF-8" />'
    theme_color = '<meta name="theme-color" content="'+ get_theme_color() +'" />'
    favicon = '<link rel="icon" href="'+ burl +'static/favicon.ico?r='+ get_random_str(9) +'">'
    return_data = charset +\
        theme_color +\
        favicon
    return return_data
