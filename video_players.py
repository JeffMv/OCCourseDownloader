# -*- coding: utf-8 -*-
"""Helper module to deal with external players and provide stable API

This module will need update when video players change their API.

Currently supported APIs:
- Vimeo 2019-08
"""

import json

from bs4 import BeautifulSoup

### Usual video qualities for Vimeo: "360p","540p","720p","1080p"

### We want to extract the JSON dictionary between the following pargs
## var config = {"cdn_url":"https://f.vimeocdn.com","vimeo_api_url":"api.vimeo.com","request":{"files":{"dash":{"separate_av":true,"streams":[{"profile":119,"quality":"1080p","id":753898737,
## ...
## log_plays":1,"quality":null,"transparent":1,"loop":0,"autoplay":0},"view":1,"vimeo_url":"vimeo.com"};
##
##         if (!config.request) {
def vimeo_video_infos(script_tag_content):
    """
    :rtyoe: dict
    :returns: summary, video_formats
                summary: tuple summary of video infos returned by the API
                    (video quality (ex. '540p'), width (int), height (int), video url, video fps)
                video_formats: exactly what vimeo returns (array of video infos):
                    [
                        {
                          "width": 960,
                          "height": 540
                          "fps": 25,
                          "quality": "540p",
                          "url": "https://gcs-vimeo.akamaized.net/exp=1565959533~acl=%2A%2F753898738.mp4%2A~hmac=d9edf1c1542b4577bc196d2f942241b755b740087b4345db0299879c59f10f0c/vimeo-prod-skyfire-std-us/01/3526/8/217633069/753898738.mp4",
                          "profile": 165,
                          "mime": "video/mp4",
                          "id": 753898738,
                          ...
                        },
                        ...
                    ]
                    
    """
    start_mark = 'var config = '
    start_index = script_tag_content.find(start_mark) + len(start_mark)
    end_mark = 'if (!config.request) {'
    end_index = script_tag_content.find(end_mark)
    
    js_txt = script_tag_content[start_index: end_index].strip()
    assert js_txt[-2:] == '};'
    js_txt = js_txt[:-1]
    
    page_infos_json = json.loads(js_txt)
    video_formats = page_infos_json['request']['files']['progressive']
    
    summary = [(vid['quality'], (vid['width'], vid['height']), vid['url'], vid['fps']) for vid in video_formats]
    
    return summary, video_formats

def vimeo_video_infos_from_video_page(html_content):
    """
    :param str html_content: the HTML
    """
    vimeo_page_soup = BeautifulSoup(html_content, 'html.parser')
    script_tags_content = [tag.get_text() for tag in vimeo_page_soup.find_all('script') 
                           if tag.get_text().find('''"mime":"video/mp4"''') >= 0]
    
    assert len(script_tags_content) == 1
    content = script_tags_content[0]
    return vimeo_video_infos(content)
