#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

import requests

from bs4 import BeautifulSoup

import jmm.browsers

from jmm.soups import soupifyContent

from markdown import html_to_markdown

# class OcCourseFetcherSpider(scrapy.Spider):
# class OcCourseFetcher(object):
#     """
#     """
    
def extract_course_chapters(html_page, course_url):
    hostname = 'https://openclassrooms.com'
    
    course_description_page_soup = BeautifulSoup(html_page, 'lxml')
    if course_url is None:
        course_url = course_description_page_soup.find('link', {'rel': 'canonical'}).get('href')
        
    course_id, course_chapter_subpath, lang = helper_parse_course_page_url(course_url)
    
    course_timeline = course_description_page_soup.find('div', {'class': 'timeline__steps'})
    timeline_elmts = course_timeline.findChildren(recursive=False)
    # first and last childs are chapter separators, so drop them
    timeline_elmts = timeline_elmts[1:-1]
    nbr_of_course_parts = len(timeline_elmts.find_all('span', {'class': 'timeline__splitChapter'})) - 2
    curr_part_nbr = 1
    curr_chap = 0
    
    chapters = []
    for chapter_timeline_soup in timeline_elmts:
        node_classes = chapter_timeline_soup.attrs.get('class', [])
        if 'timeline__splitChapter' in node_classes:
            curr_part_nbr += 1
            curr_chap = 0
            continue
        elif 'timeline__step' in node_classes:
            # a chapter node
            curr_chap += 1
            chap_title = chapter_timeline_soup.attrs.get('title')
            # chap_path is absolute path, so already has '/'
            chap_path = chapter_timeline_soup.attrs.get('href')
            chap_url = (hostname + chap_path)
            chapter = (curr_part_nbr, curr_chap, chap_path, chap_title, chap_url)
            chapters.append(chapter)
            pass
        else:
            print('OcCourseFetcherSpider.start_requests() :: unrecognized node "%s"' % (chapter_timeline_soup))
            pass                
    
    return chapters


def parse_course_page_content(html_page, driver=None, verbose=1):
    """
    should return the HTML content 
    """
    soup = BeautifulSoup(html_page, 'lxml')
    content_node = soup.find('div', {'class': 'userContent'})
    # content_node = soup.find('div', {'class': 'js-userContent'})
    image_tags = content_node.find_all('img')
    
    image_infos = []
    for i, tag in enumerate(image_tags):
        url, description = tag.attrs.get('src'), tag.attrs.get('alt')
        caption_tag = tag.parent.figcaption
        caption = caption_tag.get_text().strip() if caption_tag else None
        
        course_id, course_page, lang = helper_parse_course_page_url(url)
        page_url = "/".join([lang, course_id, course_page])
        if verbose >= 1:
            print("fetching image %i / %i from course page %s" % (i+1, len(image_tags), page_url))
        image_data = requests.get(url).content
        
        image_infos.append((url, description, caption, image_data, i))
        # image_infos.append((url, description, caption))
    
    
    ### getting video infos
    # look for all iframe with src pointing to a vimeo player. Like
    # <iframe ... src="//player.vimeo.com/video/217633247?color=7451eb">
    vimeo_player_iframes_tags = [(i, frame) for i, frame in enumerate(soup('iframe')) if frame.get('src') is not None and frame.get('src').lower().find('player.vimeo.com') >= 0]
    iFrame = d.find_elements_by_tag_name("iframe")[0]
    if driver:
        # iframes that have 
        driver.switchTo().frame(iframe);
        driver.getPageSource();
        driver.switchTo().defaultContent();

    ### we now have already returned the html content and the image urls
    pass


def helper_parse_course_page_url(url):
    """
    Example of urls:
    course presentation page url example:
    https://openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning
    course chapter page url example:
    https://openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning/4011858-identifez-les-differentes-etapes-de-modelisation
    
    :return: tuple of str: (course path id, course page subpath or None, language)
    """
    hostname = 'openclassrooms.com/'
    has_hostname = url.find(hostname) >= 0
    if has_hostname:
        path = url[url.find(hostname)+len(hostname):]
    else:
        path = url[1:] if (url[0] == '/') else url
    
    lang, _, course_id, *course_page = path.split('/')
    course_page = course_page[0] if len(course_page) > 0 else None
    
    # for url="https://openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning/4011858-identifez-les-differentes-etapes-de-modelisation"
    # would return: ('4011851-initiez-vous-au-machine-learning', '4011858-identifez-les-differentes-etapes-de-modelisation', 'fr')
    return (course_id, course_page, lang)

def helper_course_page_url(course_id, course_page=None, lang=None):
    """
    """
    lang = "fr" if lang is None
    arr = ["https://openclassrooms.com", lang, "courses", course_id]
    if course_page is not None:
        arr.append(course_page)
    return "/".join(arr)


###############################################################################


def argParser():
    """Creates the argument parser of the program.
    See the following answer to see how to implement a multi-level arg parse:
        https://stackoverflow.com/a/10579924/4418092
    Or see here https://docs.python.org/dev/library/argparse.html#sub-commands
    to see how to implement one-level subcommands.
    """
    parser = argparse.ArgumentParser(
        description="""Data fetching"""
        )
    
    parser.add_argument('--courseUrls', '-c', nargs="+", required=True, help="Course urls of the courses to fetch")
    # parser.add_argument('--startUrls', '-u', nargs="+", required=True, help="Start urls of the crawler")
    # parser.add_argument('--allowedDomains', '-d', nargs="+", required=False, help="Allowed domains of the crawler")
    
    parser.add_argument('--username', '-u', help="username or email of the service")
    parser.add_argument('--password', '-p', help="password of the service. If not provided it will be asked in a secure way interactively")
    return parser


def extract_course_page_content(driver):
    driver.switchTo().defaultContent()
    
    soup = soupifyContent(driver.page_source)
    page_content_tag = soup.find('div', {'class': "contentWithSidebar__content"})
    infos = {'main': html_to_markdown(str(page_content_tag))}
    
    images_to_fetch = []
    videos_to_fetch = []
    
    return infos


def reach_page(driver, url):
    driver.get(url)
    # wait until finished loading
    print("... did we wait until finished loading ? ...\n\t (url: '%s')" % (url))
    return driver.page_source


def fetch_page_and_contents(driver, url, directory, content_prefix, image_prefix=None, video_prefix=None):
    """Fetches the page and saves it to disk
    :param str directory: directory to save to.
    :param str content_prefix: a filepath prefix to prepend to the saved files.
                    The prefix is relative to the `directory` parameter.
    :param str image_prefix: a filepath prefix to prepend to image files.
                    The prefix is relative to the `directory` parameter.
                    If None, a default architecture will be used.
                    The default architecture uses content_prefix.
    :param str video_prefix: a filepath prefix to prepend to image files.
                    The prefix is relative to the `directory` parameter.
                    If None, a default architecture will be used.
                    The default architecture uses content_prefix.
    """
    directory = os.path.abspath(directory)
    
    pass


def fetch_course(browser, course_url):
    course_id, course_page, lang = helper_parse_course_page_url(course_url)
    course_home_page_url = helper_course_page_url(course_id, None, lang)
    
    reach_page(browser, course_home_page_url)
    chapters = extract_course_chapters(browser.page_source, course_home_page_url)
    
    ### cycle through the URLs and pages
    ### save home page to disk
    
    ### go to a page
    
    ### get page source and content ()
    ## function
        ## reads HTML
    
    browser.get(course_home_page_url)
    _ = browser.page_source
    pass


def main_selenium():
    parser = argParser()
    args = parser.parse_args()
    
    if args.password is None:
        args.password = getpass.getpass("Openclassrooms.com password: ")
    
    nav = jmm.browsers.SeleniumHelper()
    
    ### login
    nav.get('https://openclassrooms.com/fr/login')
    nav.enter_textfield('input#field_username', args.username)
    nav.enter_textfield('input#field_password', args.password)
    nav.click_element('button#login-button')
    
    for url in args.courseUrls:
        print("Fetching course for %s" % url)
        
        # ...
        fetch_course(nav, url)


if __name__ == '__main__':
    main_selenium()
