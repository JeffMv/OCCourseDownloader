# -*- coding: utf-8 -*-
"""Converting HTML to markdown
"""

import tomd

def html_to_markdown(html):
    return tomd.Tomd(html).markdown
