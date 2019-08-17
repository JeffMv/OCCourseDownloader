# -*- coding: utf-8 -*-
"""Helper module to deal with external players and provide stable API

This module will need update when video players change their API.

Currently supported APIs:
- Vimeo 2019-08
"""

import json


### We want to extract the JSON dictionary between the following pargs
## var config = {"cdn_url":"https://f.vimeocdn.com","vimeo_api_url":"api.vimeo.com","request":{"files":{"dash":{"separate_av":true,"streams":[{"profile":119,"quality":"1080p","id":753898737,
## ...
## log_plays":1,"quality":null,"transparent":1,"loop":0,"autoplay":0},"view":1,"vimeo_url":"vimeo.com"};
##
##         if (!config.request) {
def vimeo_video_infos(script_tag_content):
	"""
	:rtyoe: dict
	:returns: ...
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
