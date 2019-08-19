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

