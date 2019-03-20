# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def print_google_ads(format):
    r = ''
    try:

        if format == 'leaderboard':
            r = '' +\
            '<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>'+\
            '<!-- sa-list -->'+\
            '<ins class="adsbygoogle"'+\
            '     style="display:inline-block;width:970px;height:90px"'+\
            '     data-ad-client="ca-pub-1605085568476447"'+\
            '     data-ad-slot="1311827228"></ins>'+\
            '<script>'+\
            '(adsbygoogle = window.adsbygoogle || []).push({});'+\
            '</script>'

        if format == 'small_leaderboard':
            r = '' +\
            '<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>'+\
            '<!-- sa-main -->'+\
            '<ins class="adsbygoogle"'+\
            '     style="display:inline-block;width:728px;height:90px"'+\
            '     data-ad-client="ca-pub-1605085568476447"'+\
            '     data-ad-slot="2896371631"></ins>'+\
            '<script>'+\
            '(adsbygoogle = window.adsbygoogle || []).push({});'+\
            '</script>'

    except Exception as e: print(e)
    return r
