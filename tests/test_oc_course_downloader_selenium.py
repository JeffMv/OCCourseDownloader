# -*- coding: utf-8 -*-
"""Tests for OpenClassrooms course downloader
"""

import os
import json

import oc_course_downloader_selenium as script


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
