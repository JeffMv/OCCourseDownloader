# -*- coding: utf-8 -*-
"""Tests for OpenClassrooms course downloader
"""

import os
import json

import requests

import oc_course_downloader_selenium as script
import video_players as video_players_module


def _content_of_file(filepath, mode='r'):
    with open(filepath, mode) as fh:
        return fh.read()


######      Tests       ######


def test_helper_parse_course_page_url():
    course_url = "https://openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning/4011858-identifez-les-differentes-etapes-de-modelisation"
    expected_lang = "fr"
    expected_course_id = "4011851-initiez-vous-au-machine-learning"
    expected_chapter_id = "4011858-identifez-les-differentes-etapes-de-modelisation"
    assert (expected_course_id, expected_chapter_id, expected_lang) == script.helper_parse_course_page_url(course_url)
    
    course_url = "https://openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning/"
    expected_chapter_id = None
    assert (expected_course_id, expected_chapter_id, expected_lang) == script.helper_parse_course_page_url(course_url)
    
    course_url = "https://openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning"
    assert (expected_course_id, expected_chapter_id, expected_lang) == script.helper_parse_course_page_url(course_url)
    
def test_helper_course_page_url():
    course_id = "4011851-initiez-vous-au-machine-learning"
    lang = "fr"
    course_page = None
    expected_url_part = 'openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning'
    assert script.helper_course_page_url(course_id, course_page, lang).find(expected_url_part) >= 0
    
    course_page = "4011858-identifez-les-differentes-etapes-de-modelisation"
    expected_url_part = 'openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning/4011858-identifez-les-differentes-etapes-de-modelisation'
    assert script.helper_course_page_url(course_id, course_page, lang).find(expected_url_part) >= 0


def test_extract_course_chapters_as_json():
    base_test_data_path = "./tests/test_data/course-pages/test-project-with-python/"
    fname_raw = "Utilisez des mocks - Testez votre projet avec Python - OpenClassrooms.html"
    fname_json = "Utilisez des mocks - Testez votre projet avec Python - OpenClassrooms.html.chapters.json"
    
    with open(os.path.join(base_test_data_path, fname_json)) as fh:
        expected_json_str = json.dumps(json.load(fh))
    
    with open(os.path.join(base_test_data_path, fname_raw)) as fh:
        chapters = script.extract_course_chapters(fh.read())
        chapters_json_str = json.dumps(chapters)

    assert expected_json_str == chapters_json_str


def test_video_players__vimeo_video_infos_from_video_page():
    base_test_data_path = "./tests/test_data/course-pages/test-project-with-python/"
    
    ### We will test the same video description with the two different functions
    expected_result = json.loads(_content_of_file(os.path.join(base_test_data_path, "Utilisez des mocks--video-script.extracted-infos.js"), 'r'))
    expected_result_as_json = json.dumps(expected_result)
    
    filepath = os.path.join(base_test_data_path, "Utilisez des mocks--video-script.js")
    script_tag_content = _content_of_file(filepath, 'r')
    result = video_players_module.vimeo_video_infos(script_tag_content)
    # print(json.dumps(result, indent=2))
    assert json.dumps(result[0]) == json.dumps(expected_result[0])
    assert json.dumps(result[1]) == json.dumps(expected_result[1])
    
    filepath = os.path.join(base_test_data_path, "Utilisez des mocks--vimeo-page.html")
    video_page_source = _content_of_file(filepath, 'r')
    assert json.dumps(video_players_module.vimeo_video_infos_from_video_page(video_page_source)) == expected_result_as_json
    
    # ### test with fetching from the url 
    # ### make sure you check that the video URLs are similar *BUT* not equal
    # ### (since the actual video urls are renewed each time)
    # video_page_url = "https://player.vimeo.com/video/217633247?color=7451eb"
    # response = requests.get(video_page_url)
    # res = video_players_module.vimeo_video_infos_from_video_page(response.content.decode(encoding=response.encoding))
    # assert json.dumps(res) == expected_result_as_json


# def test_video_players__vimeo_video_infos():
#     assert False
