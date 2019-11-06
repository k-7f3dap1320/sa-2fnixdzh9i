
from app_cookie import *

def get_purechat(forceDisplay):
    return_data = ''
    content = ""
    if user_is_login() == 0 or forceDisplay == 1:
        content="<script type='text/javascript' data-cfasync='false'>"+\
        "window.purechatApi = { l: [], t: [], on: function () { this.l.push(arguments); } }; "+\
        "(function () { var done = false; var script = document.createElement('script'); "+\
        "script.async = true; script.type = 'text/javascript'; "+\
        "script.src = 'https://app.purechat.com/VisitorWidget/WidgetScript'; "+\
        "document.getElementsByTagName('HEAD').item(0).appendChild(script); "+\
        "script.onreadystatechange = script.onload = function (e) { if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) "+\
        "{ var w = new PCWidget({c: '712eb02f-e280-45ee-ab5f-3b25c0c77aed', f: true }); done = true; } }; })();</script>"
    return_data = content
    return return_data
