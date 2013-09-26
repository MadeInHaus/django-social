'''
Created on Sep 26, 2013
'''

def parse_twitter_picture_embed(msg, width="200px", height="200px"):
    urls = msg.get('entities', {}).get('utls', [])
    
    picture = None
    for url in urls:
        if 'pic.twitter.com':
            picture = url
    
    if not picture:
        return ''

    return '<img src="{}" width="{}" height="{}">'.format(picture, width, height)

def parse_twitter_video_embed(msg, width="200px", height="200px"):
    """ need to put in proper video embed here """
    urls = msg.get('entities', {}).get('utls', [])
    
    video = None
    for url in urls:
        if 'youtu.be' in url or 'youtube.com' in url or 'vine.co' in url:
            video = url

    if 'vine.co' in video:
        return '<iframe class="vine-embed" src="{}/embed/simple" frameborder="0" width="{}" height="{}"></iframe><script async src="//platform.vine.co/static/scripts/embed.js" charset="utf-8"></script>'.format(video, width, height)

    return '<video src="{}" width="{}" height="{}">'.format(video, width, height)
