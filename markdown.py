# -*- coding: utf-8 -*-
"""Converting HTML to markdown
"""
import tomd

# try:
#   import
# except ModuleNotFoundError:
#   pass


def html_to_markdown(html):
    return tomd.Tomd(html).markdown
