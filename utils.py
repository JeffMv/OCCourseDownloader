# -*- coding: utf-8 -*-

import os

import requests

from bs4 import BeautifulSoup

# progressbar is provided by progressbar2 on PYPI.
import progressbar
from requests_download import download, TrackerBase


class UIProgressTracker(TrackerBase):
    def __init__(self, progressbar):
        self.progressbar = progressbar
        self.recvd = 0

    def on_start(self, response):
        max_value = None
        if 'content-length' in response.headers:
            max_value = int(response.headers['content-length'])
        self.progressbar.maxval = max_value
        self.progressbar.start()
        self.recvd = 0

    def on_chunk(self, chunk):
        self.recvd += len(chunk)
        try:
            self.progressbar.update(self.recvd)
        except ValueError:
            # Probably the HTTP headers lied.
            pass

    def on_finish(self):
        self.progressbar.finish()


# progress = UIProgressTracker(progressbar.ProgressBar())
# download('https://github.com/takluyver/requests_download/archive/master.zip',
#          'requests_download.zip', trackers=[progress])

def download_with_progress_indicator(url, path, create_dirs=True):
    if create_dirs:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    
    progress = UIProgressTracker(progressbar.ProgressBar())
    download(url, path, trackers=[progress])


def soupify_html(content):
    return BeautifulSoup(content, 'lxml')
