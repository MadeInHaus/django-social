'''
Created on Sep 26, 2013
'''

def parse_instagram_picture_embed(msg, width="200px", height="200px"):
    picture = msg['images']['standard_resolution']['url']
    return '<img src="{}" width="{}" height="{}">'.format(picture, width, height)

def parse_instagram_video_embed(msg, width="200px", height="200px"):
    """ need to put in proper video embed here """
    video_url = msg['videos']['standard_resolution']['url']
    picture_url = msg['images']['standard_resolution']['url']
    video_str = """<video controls preload="none" width="{}" height="{}" poster="{}">
                    <source src="{}" type='video/mp4' />
                </video>""".format( width, height, picture_url, video_url)
    return video_str
