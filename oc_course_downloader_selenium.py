#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import getpass

import requests

from bs4 import BeautifulSoup

import jmm.browsers

import utils

from markdown import html_to_markdown
from video_players import vimeo_video_infos
from utils import soupify_html

# class OcCourseFetcherSpider(scrapy.Spider):
# class OcCourseFetcher(object):
#     """
#     """


def reach_page(browser, url, time_to_wait='default'):
    """Navigates to a page and ensures the page has finished loading properly
    before returning its source code.
    :rtype: str
    :returns: source code of the target page.
    """
    time_to_wait = 5 if time_to_wait == 'default' else time_to_wait
    print("reaching page @ '%s'" % (url))
    browser.driver.get(url)
    # wait until finished loading
    # print("... did we wait until finished loading ? ...\n\t (url: '%s')" % (url))
    browser.waitTime(time_to_wait)
    return browser.driver.page_source



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
    course_page = course_page if course_page and len(course_page) > 0 else None
    
    # for url="https://openclassrooms.com/fr/courses/4011851-initiez-vous-au-machine-learning/4011858-identifez-les-differentes-etapes-de-modelisation"
    # would return: ('4011851-initiez-vous-au-machine-learning', '4011858-identifez-les-differentes-etapes-de-modelisation', 'fr')
    return (course_id, course_page, lang)


def helper_course_page_url(course_id, course_page=None, lang=None):
    """
    """
    lang = "fr" if lang is None else lang
    arr = ["https://openclassrooms.com", lang, "courses", course_id]
    if course_page is not None:
        arr.append(course_page)
    return "/".join(arr)


def extract_course_chapters(html_page):
    """
    :param html_page:
    :rtype: list<tuple>
    :returns: list of chapters infos
            a chapter is a tuple consisting of 
            (the part number, the chapter number, chapter path, chapter title, chapter url)
    """
    hostname = 'https://openclassrooms.com'
    
    course_description_page_soup = BeautifulSoup(html_page, 'lxml')
    
    # course_url = course_description_page_soup.find('link', {'rel': 'canonical'}).get('href')
    # course_id, course_chapter_subpath, lang = helper_parse_course_page_url(course_url)
    
    course_timeline = course_description_page_soup.find('div', {'class': 'timeline__steps'})
    timeline_elmts = course_timeline.findChildren(recursive=False)
    # first and last childs are chapter separators, so drop them
    timeline_elmts = timeline_elmts[1:-1]
    nbr_of_course_parts = len(course_timeline.find_all('span', {'class': 'timeline__splitChapter'})) - 2
    curr_part_nbr = 1
    curr_chap = 0
    
    course_page_url_path = course_description_page_soup.find('div', {'class': 'timeline__inner'}).find('a', {"class": 'timeline__roundIcon'}).get('href')
    course_title = course_description_page_soup.find('h1', 'courseHeader__title').get_text().strip()
    intro_chapter = (0, 1, course_page_url_path, course_title, (hostname + course_page_url_path))
    
    chapters = [intro_chapter]
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
    
    parser.add_argument('--videoQuality', '--quality', '-q', default='360p', help="""The video quality you want to download for videos (generally Vimeo offers "360p", "540p", "720p", or "1080p"). Pass in 0 or an invalid quality to ignore video files. Default is '360p', which the lowest quality normally""")
    parser.add_argument('--destination', '-d', default='.', help="""The directory to download the course to. Default will download in the current directory.""")
    parser.add_argument('--overwrite', '-o', action="store_true", help="""Overwrite images and videos (will fetch again even if there is already an existing file)""")
    parser.add_argument('--ignoreChapters', '-x', nargs="*", help="""Ignored chapters (in the form part-chapter like 2-4 to ignore chapter 4 of part 2). Example: 0-1 1-1 1-2 2-1 2-3""")
    return parser


###############################################################################


def extract_course_quiz_page_as_markdown(html_page):
    soup = soupify_html(html_page)
    page_content_tag = soup.find('div', {'class': "contentWithSidebar__content"})
    # page_content_tag = soup.find('div', {'class': "contentWithSidebar"})
    title = page_content_tag.h1.get_text().strip()  # chapter title
    markdown_text = html_to_markdown(str(page_content_tag)).strip()
    return markdown_text, title


def extract_course_activity_page(browser):
    """
    :param browser: navigator helper
    """
    html_page = browser.driver.page_source if getattr(browser, 'driver', None) else browser
    browser = browser if getattr(browser, 'driver', None) else None
    if browser:
        ## TODO
        browser.click_element('.p2p__stepBoxAction > button')
        browser.waitTime(5)
        html_page = browser.driver.page_source
    
    if html_page:
        soup = soupify_html(html_page)
        page_content_tag = soup.find('div', {'class': "contentWithSidebar__content"})
        title = page_content_tag.h2.get_text().strip()  # chapter title
        markdown_text = html_to_markdown(str(page_content_tag)).strip()
        return markdown_text, title, html_page


def extract_course_page_main_text_as_markdown(html_page):
    soup = soupify_html(html_page)
    page_content_tag = soup.find('div', {'class': "contentWithSidebar__content"})
    title_tag = page_content_tag.h2
    if title_tag is None:
        # it is probably a Quiz page
        # title_tag = page_content_tag.h1.get_text.strip()
        return extract_course_quiz_page_as_markdown(html_page)
    else:
        title = title_tag.get_text().strip()  # chapter title
        content = page_content_tag.find('div', {'class': 'static'}).section.find('div', {'itemprop': "articleBody"})
        markdown_text = html_to_markdown(str(content)).strip()
        markdown_text = """## %s\n\n%s\n""" % (title, markdown_text)
        return markdown_text, title


def extract_course_page_images(html_page):
    hostname = "https://openclassrooms.com"
    
    soup = soupify_html(html_page)
    page_content_tag = soup.find('div', {'class': "contentWithSidebar__content"})
    
    images_to_fetch = []
    
    image_tags = page_content_tag('img')
    for i, tag in enumerate(image_tags):
        image_desc = tag.get('alt')
        image_src = tag['src']
        if image_src.find('/') == 0:
            if image_src.find('//') == 0:
                # get full URL (absolute) for `<img src="//static.oc-static.com/prod/images/courses/certif.jpg">`
                image_src = ("https:" + image_src)
            else:
                # get full URL (absolute) for `<img src="/path/to/img.jpg">`
                image_src = (hostname + "/" + image_src) if image_src.find('/') == 0 else image_src
        
        image_file_basename = image_src.split('/')[-1].split('?')[0].split('#')[0]
        image_info = (i + 1, image_src, image_desc, image_file_basename)    
        
        images_to_fetch.append(image_info)
    
    return images_to_fetch


def fetch_course_page_video_informations(html_page, video_pages_html=None):
    """
    :param list<str> video_pages_html: instead of fetching, the parser will use an html content out of it
                each time it encounters a video it needs to fetch
    """
    hostname = "https://openclassrooms.com"
    soup = soupify_html(html_page)
    page_content_tag = soup.find('div', {'class': "contentWithSidebar__content"})
    
    videos_to_fetch = []
    video_frame_tags = [[j, iframe_tag, ("https:" + iframe_tag['src'])] for j, iframe_tag in enumerate(page_content_tag('iframe')) 
                        if 'src' in iframe_tag.attrs and iframe_tag.get('src').find('player.vimeo') >= 0]
    
    if len(video_frame_tags) == 0:
        # in case we fetch without javascript, Vimeo videos are in the following form
        # <video id="r-4452461" data-claire-element-id="7904382" src="https://vimeo.com/217633069"><a href="https://vimeo.com/217633069">https://vimeo.com/217633069</a></video>
        # "https://vimeo.com/217633069" -> "https://player.vimeo.com/video/217633069?color=7451eb"
        []
        vimeo_video_url_to_player_url = lambda url: "https://player.vimeo.com/video/%s?color=7451eb" % (url.split('?')[0].split('/')[-1])
        video_frame_tags = [[j, None, vimeo_video_url_to_player_url(video_tag['src'])] for j, video_tag in enumerate(page_content_tag('video')) 
                            if 'src' in video_tag.attrs and video_tag.get('src').find('//vimeo.com/') >= 0]
    
    assert video_pages_html is None or len(video_pages_html) >= len(video_frame_tags)    
    for k, tag_details in enumerate(video_frame_tags):
        # j, iframe_tag, video_src = tag_details
        _, _, video_src = tag_details
        
        # video/iframe tags of the course's videos
        if video_pages_html:
            iframe_source = video_pages_html[k]
        else:
            resp = requests.get(video_src)
            iframe_source = resp.content.decode(encoding=resp.encoding)
        vimeo_page_soup = soupify_html(iframe_source)
        script_tags_content = [tag.get_text() for tag in vimeo_page_soup.find_all('script') 
                               if tag.get_text().find('''"mime":"video/mp4"''') >= 0]
        
        assert len(script_tags_content) == 1
        content = script_tags_content[0]
        video_formats_infos_summary, video_formats_infos = vimeo_video_infos(content)
        
        video_title = vimeo_page_soup.title.get_text().strip()
        
        video_info = (k + 1, video_title, video_formats_infos_summary, video_formats_infos)
        videos_to_fetch.append(video_info)
    
    return videos_to_fetch


def extract_course_page_main_content(html_page, video_pages_html=None):
    content, chapter_title = extract_course_page_main_text_as_markdown(html_page)
    images_to_fetch = extract_course_page_images(html_page)
    videos_to_fetch = fetch_course_page_video_informations(html_page, video_pages_html=video_pages_html)
    page_infos = {
        'title': chapter_title,
        'markdown_text': content,
        'to_fetch': {
            'images': images_to_fetch,
            'videos': videos_to_fetch
        },
        'html': html_page
    }
    return page_infos


def paths_for_course(chapter_infos, part_nbr, chapter_nbr, video_quality, prefix):
    ### fetching the chapter's page
    base_chapter_path = os.path.join(prefix, '%i-%i' % (part_nbr, chapter_nbr))
    
    text_infos = (0, os.path.join(base_chapter_path, chapter_infos['title'] + ".md"), chapter_infos['markdown_text'])
    html_infos = (0, os.path.join(base_chapter_path, chapter_infos['title'] + ".html"), chapter_infos['html'])
    
    ### fetching the images
    base_media_path = 'medias'
    # base_media_path = '.'
    images = chapter_infos.get('to_fetch').get('images') if chapter_infos.get('to_fetch') is not None and chapter_infos['to_fetch'].get('images') else []
    # download_infos: [(path to save to,  url, image description), ...]
    images_download_infos = [(os.path.join(base_chapter_path, base_media_path, image_info[3]),  # destination path
                       image_info[1],  # url
                       image_info[2])  # image description
                      for image_info in images]
    
    
    ### fetching the videos
    get_at_index_or_default = lambda x, k, default_value: x[k] if x is not None and k < len(x) else default_value
    first_element = lambda arr: arr[0] if len(arr) > 0 else None
    video_infos_for_quality = lambda video_infos_tuple, quality: first_element([video_infos for video_infos in video_infos_tuple[2] if str(video_infos[0]) == str(quality)])
    video_for_quality = lambda video_infos_tuple, quality: get_at_index_or_default(first_element([video_infos for video_infos in video_infos_tuple[2] if str(video_infos[0]) == str(quality)]), 2, None)
    videos = chapter_infos['to_fetch']['videos'] if chapter_infos.get('to_fetch') is not None and chapter_infos['to_fetch'].get('videos') else []
    
    video_download_infos = []
    for i, video_info in enumerate(videos):
        # video_info: (k+1, video_title, video_formats_infos_summary, video_formats_infos, video_extension)
        #       video_formats_infos_summary: (video quality (ex. '540p'), *tuple*(width (int), height (int))*/tuple*, video url, file extension)
        extension = video_infos_for_quality(video_info, video_quality)[3]
        
        dest_path = os.path.join(base_chapter_path, base_media_path, (video_info[1] + "." + extension))
        url = video_for_quality(video_info, video_quality)
        title = video_info[1]
        video_download_infos.append((dest_path, url, title))
    
    return text_infos, html_infos, images_download_infos, video_download_infos


def fetch_and_save_course_chapter_infos(chapter_infos, part_nbr, chapter_nbr, video_quality, prefix, overwrite):
    """Fetches and writes following the architecture pattern.
    :param infos:
                ...
    :param video_quality:
                Also accepts 'low', 'medium', 'hd', 'full'
    """
    text_infos, html_infos, images_download_infos, video_download_infos = paths_for_course(chapter_infos, part_nbr, chapter_nbr, video_quality, prefix)
    
    ### Saving the text and HTML
    filepath = text_infos[1]
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath) or overwrite:
        with open(filepath, 'w') as fh:
            fh.write(text_infos[2])
    
    filepath = html_infos[1]
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath) or overwrite:
        with open(filepath, 'w') as fh:
            fh.write(html_infos[2])
    
    ### fetching the images and videos
    download_infos = images_download_infos + video_download_infos
    for i, media_infos in enumerate(download_infos):
        filepath, url, description, *_ = media_infos
        if url is not None:
            relative = os.path.relpath(filepath)
            descriptive_filepath = filepath if relative.find('..') == 0 else relative
            if not os.path.exists(filepath) or overwrite:
                print("""%i/%i) Fetching "%s" to "%s" ...""" % (i+1, len(download_infos), description, descriptive_filepath))
                utils.download_with_progress_indicator(url, filepath, True)
            else:
                print("%i/%i) Found already fetched content %s" % (i+1, len(download_infos), descriptive_filepath))
        else:
            print("Did not find quality '%s' for the video %s" % (description))
    
    pass


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
    # ...
    # fetch content and save them to the prefixed
    # fetch imges and save them to the prefixed
    # fetch videos and save them to the prefixed
    
    # iFrame = d.find_elements_by_tag_name("iframe")[0]
    # if driver:
    #     # iframes that have 
    #     driver.switch_to.frame(iframe);
    #     driver.getPageSource();
    #     driver.switch_to.default_content();
    
    pass


def fetch_course(browser, course_url, video_quality, overwrite=False, directory=None, ignored_chapters=None):
    """
    :param str directory: where to download the course
    """
    ignored_chapters = [] if ignored_chapters is None else ignored_chapters
    
    course_id, course_page, lang = helper_parse_course_page_url(course_url)
    course_home_page_url = helper_course_page_url(course_id, None, lang)
    
    reach_page(browser, course_home_page_url)
    
    chapters = extract_course_chapters(browser.driver.page_source)
    soup = soupify_html(browser.driver.page_source)
    course_title = soup.title.get_text().strip()

    home_page_chapter = (0, 1, course_home_page_url, course_title, course_home_page_url)
    chapters = [home_page_chapter] + chapters
    
    prefix = os.path.join(directory, course_title)
    os.makedirs(prefix, exist_ok=True)
    
    ### cycle through the URLs and pages
    for chapter in chapters:
        part_nbr, chapter_nbr, chap_path, chap_title, chap_url = chapter
        
        if (part_nbr, chapter_nbr) in ignored_chapters:
            print("Ignored chapter %i-%i" % (part_nbr, chapter_nbr))
            continue
        
        ### go to a page
        reach_page(browser, chap_url)
        
        is_quiz_chapter = chap_title.strip().lower().find('Quiz') == 0
        is_exercise_chapter = chap_title.strip().lower().find('Activité') == 0
        
        if is_quiz_chapter or is_exercise_chapter:
            if is_exercise_chapter:
                markdown_text, title = extract_course_quiz_page_as_markdown(html_page)
            else:
                markdown_text, title, html_page = extract_course_activity_page(browser)
            chapter_infos = {
                'title': chap_title,
                'markdown_text': markdown_text,
                'html': html_page
            }
        else:
            chapter_infos = extract_course_page_main_content(browser.driver.page_source)
        
        ### save page to disk
        fetch_and_save_course_chapter_infos(chapter_infos, part_nbr, chapter_nbr, video_quality, prefix, overwrite)
        print()
    pass


def main_selenium():
    parser = argParser()
    args = parser.parse_args()
    
    if args.username is None:
        args.username = input("Please input your OpenClassrooms.com username: ")
    
    if args.password is None:
        args.password = getpass.getpass("Openclassrooms.com password: ")
    
    nav = jmm.browsers.SeleniumHelper()
    
    ### login
    nav.get('https://openclassrooms.com/fr/login')
    nav.waitTillExists('input#field_username')
    nav.enter_textfield('input#field_username', args.username)
    nav.enter_textfield('input#field_password', args.password)
    nav.click_element('button#login-button')
    nav.waitTime(5)
    
    for url in args.courseUrls:
        print("Fetching course for %s" % url)
        directory = os.path.abspath(os.path.expanduser(args.destination))
        ignored_chapters = [(int(tup.split('-')[0]), int(tup.split('-')[1])) for tup in args.ignoreChapters]
        fetch_course(nav, url, args.videoQuality, args.overwrite, directory, ignored_chapters=ignored_chapters)
        print("---- Finished fetching the course %s ----\n" % (url))


if __name__ == '__main__':
    main_selenium()
