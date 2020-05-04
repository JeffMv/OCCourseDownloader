# -*- coding: utf-8 -*-
"""Tests for OpenClassrooms course downloader
"""

import os
import json

import pytest
import requests

os.sys.path += ".."
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
    base_test_data_path = os.path.join("tests", "test_data", "course-pages", "test-project-with-python")
    fname_raw = os.path.join("2-5-Utilisez-des-mocks", "2-5-Utilisez des mocks - Testez votre projet avec Python - OpenClassrooms.html")
    fname_json = os.path.join("2-5-Utilisez-des-mocks", "2-5-Utilisez des mocks - Testez votre projet avec Python - OpenClassrooms.html.chapters.json")
    
    with open(os.path.join(base_test_data_path, fname_json)) as fh:
        expected_json_str = json.dumps(json.load(fh))
    
    with open(os.path.join(base_test_data_path, fname_raw)) as fh:
        chapters = script.extract_course_chapters(fh.read())
        chapters_json_str = json.dumps(chapters)

    assert expected_json_str == chapters_json_str


def test_extracts_of_course_page():
    base_test_data_path = os.path.join("tests", "test_data", "course-pages", "test-project-with-python")
    chapter_test_directory = os.path.join(base_test_data_path, "2-5-Utilisez-des-mocks")
    filepath_html = os.path.join(chapter_test_directory, "2-5-Utilisez des mocks - Testez votre projet avec Python - OpenClassrooms.html")
    filepath_vimeo_page_html = os.path.join(chapter_test_directory, "2-5-Utilisez des mocks--vimeo-page.html")
    filepath_videos = os.path.join(chapter_test_directory, "result--fetch_course_page_video_informations_2-5-Utilisez des mocks.json")
    
    html_page = _content_of_file(filepath_html, 'r')
    
    expected_images = [
      (1, 'https://user.oc-static.com/upload/2017/05/04/14939097968461_Capture%20d%E2%80%99e%CC%81cran%202017-05-04%20a%CC%80%2016.56.17.png', '', '14939097968461_Capture%20d%E2%80%99e%CC%81cran%202017-05-04%20a%CC%80%2016.56.17.png'),
      (2, 'https://static.oc-static.com/prod/images/courses/certif.jpg', 'Exemple de certificat de réussite', 'certif.jpg'),
      (3, 'https://static.oc-static.com/prod/images/courses/certif.jpg', 'Exemple de certificat de réussite', 'certif.jpg')
    ]
    expected_videos = json.loads(_content_of_file(filepath_videos, 'r'))
    vimeo_page_mock_responses = [_content_of_file(filepath_vimeo_page_html, 'r')]
    
    content, chapter_title = script.extract_course_page_main_text_as_markdown(html_page)
    images_to_fetch = script.extract_course_page_images(html_page)
    videos_to_fetch = script.fetch_course_page_video_informations(html_page, vimeo_page_mock_responses)
    
    assert chapter_title.lower() == "utilisez des mocks"
    assert json.dumps(expected_images) == json.dumps(images_to_fetch)
    assert json.dumps(expected_videos) == json.dumps(videos_to_fetch)
    
    result = script.extract_course_page_main_content(html_page, video_pages_html=vimeo_page_mock_responses)
    assert json.dumps(result['to_fetch']) == json.dumps({'images': expected_images, 'videos': expected_videos})
    

def test_paths_for_course():
    base_test_data_path = os.path.join("tests", "test_data", "course-pages", "test-project-with-python")
    chapter_test_directory = os.path.join(base_test_data_path, "2-5-Utilisez-des-mocks")
    result_directory = os.path.join("tests", "result_data", "2-5-Utilisez-des-mocks")
    
    filepath = os.path.join(chapter_test_directory, "2-5-Utilisez des mocks - Testez votre projet avec Python - OpenClassrooms.html")
    filepath_vimeo_page_html = os.path.join(chapter_test_directory, "2-5-Utilisez des mocks--vimeo-page.html")
    
    html_page = _content_of_file(filepath, 'r')
    vimeo_page_mock_responses = [_content_of_file(filepath_vimeo_page_html, 'r')]
    chapter_infos = script.extract_course_page_main_content(html_page, video_pages_html=vimeo_page_mock_responses)
    
    video_quality = '360p'
    prefix = result_directory
    
    chapter_2_5 = chapter_infos
    # print("chapter_2_5:", chapter_2_5)
    ### 
    all_videos_in_same_folder = False
    result_page_text, result_page_html, images_to_fetch, videos_to_fetch = script.paths_for_course(chapter_2_5, 2, 5, video_quality, prefix, all_videos_in_same_folder)
    download_infos = images_to_fetch + videos_to_fetch
    
    print("download_infos:\n%s" % json.dumps(download_infos, indent=2))
    # print("download_infos[...]:", json.dumps(download_infos[0], indent=2))
    
    expectation_filepath = os.path.join(chapter_test_directory, 'result--paths_for_course_2-5-Utilisez des mocks.json')
    expected_result = json.loads(_content_of_file(expectation_filepath))
    assert json.dumps(expected_result) == json.dumps(download_infos)
    
    ###
    all_videos_in_same_folder = True
    result_page_text, result_page_html, images_to_fetch, videos_to_fetch = script.paths_for_course(chapter_2_5, 2, 5, video_quality, prefix, all_videos_in_same_folder)
    download_infos = images_to_fetch + videos_to_fetch
    
    print("download_infos:\n%s" % json.dumps(download_infos, indent=2))
    # print("download_infos[...]:", json.dumps(download_infos[0], indent=2))
    expectation_filepath = os.path.join(chapter_test_directory, 'result--paths--all-videos-same-in-same-dir_for_course_2-5-Utilisez des mocks.json')
    expected_result = json.loads(_content_of_file(expectation_filepath))
    assert json.dumps(expected_result) == json.dumps(download_infos)


# TODO : this test
# def test_fetch_and_save_course_chapter_infos():
#     base_test_data_path = os.path.join("tests", "test_data", "course-pages", "test-project-with-python")
#     filepath = os.path.join(base_test_data_path, "2-5-Utilisez-des-mocks", "2-5-Utilisez des mocks - Testez votre projet avec Python - OpenClassrooms.html.chapters.json")
#     course_chapters = _content_of_file(filepath, 'r')
#     assert False


@pytest.mark.skip(reason="YAGNI.")
def test_result_page_written_content():
    # testing the html/markdown
    assert False


def test_video_players__vimeo_video_infos_from_video_page():
    base_test_data_path = os.path.join("tests", "test_data", "course-pages", "test-project-with-python")
    
    ### We will test the same video description with the two different functions
    expected_result = json.loads(_content_of_file(os.path.join(base_test_data_path, "2-5-Utilisez-des-mocks", "2-5-Utilisez des mocks--video-script.extracted-infos.js"), 'r'))
    expected_result_as_json = json.dumps(expected_result)
    
    filepath = os.path.join(base_test_data_path, "2-5-Utilisez-des-mocks", "2-5-Utilisez des mocks--video-script.js")
    script_tag_content = _content_of_file(filepath, 'r')
    result = video_players_module.vimeo_video_infos(script_tag_content)
    # print(json.dumps(result, indent=2))
    assert json.dumps(result[0]) == json.dumps(expected_result[0])
    assert json.dumps(result[1]) == json.dumps(expected_result[1])
    
    filepath = os.path.join(base_test_data_path, "2-5-Utilisez-des-mocks", "2-5-Utilisez des mocks--vimeo-page.html")
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
