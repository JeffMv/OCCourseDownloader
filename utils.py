# -*- coding: utf-8 -*-

import os

import requests

from bs4 import BeautifulSoup

try:
    # progressbar is provided by progressbar2 on PYPI.
    import progressbar
    from requests_download import download, TrackerBase
except:
    progressbar = None
    download, TrackerBase = None, None


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
    
    if progress is not None and download is not None:
        progress = UIProgressTracker(progressbar.ProgressBar())
        download(url, path, trackers=[progress])
    else:
        print("""Downloading "%s" to "%s" ... please wait.""" % (url, path))
        with open(path, 'wb') as fh:
            response = requests.get(url)
            fh.write(response.content)
        print("""\tFinished downloading the file "%s" """ % (path))


def soupify_html(content):
    return BeautifulSoup(content, 'lxml')
