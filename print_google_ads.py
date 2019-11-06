
def print_google_ads(format,align):
    return_data = ''
    if format == 'rectangle':
        return_data = '' +\
        '<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>'+\
        '<!-- sa-signal -->'+\
        '<ins class="adsbygoogle"'+\
        '     style="display:inline-block;width:300px;height:250px"'+\
        '     data-ad-client="ca-pub-1605085568476447"'+\
        '     data-ad-slot="4165991783"></ins>'+\
        '<script>'+\
        '(adsbygoogle = window.adsbygoogle || []).push({});'+\
        '</script>'

    if format == 'billboard':
        return_data = '' +\
        '<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>'+\
        '<!-- sa-list-large -->'+\
        '<ins class="adsbygoogle"'+\
        '     style="display:inline-block;width:970px;height:250px"'+\
        '     data-ad-client="ca-pub-1605085568476447"'+\
        '     data-ad-slot="2109548352"></ins>'+\
        '<script>'+\
        '(adsbygoogle = window.adsbygoogle || []).push({});'+\
        '</script>'

    if format == 'leaderboard':
        return_data = '' +\
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
        return_data = '' +\
        '<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>'+\
        '<!-- sa-main -->'+\
        '<ins class="adsbygoogle"'+\
        '     style="display:inline-block;width:728px;height:90px"'+\
        '     data-ad-client="ca-pub-1605085568476447"'+\
        '     data-ad-slot="2896371631"></ins>'+\
        '<script>'+\
        '(adsbygoogle = window.adsbygoogle || []).push({});'+\
        '</script>'
    return_data = '<div style="margin: 0px; float: '+ align +';">' + return_data + '</div>'
    return return_data
