#!/usr/bin/env python
# encoding: utf-8
"""
K.py

Created by Loïc Wolff on 2009-04-25.
Copyright (c) 2009 loicwolff.eu. All rights reserved.
"""

# tag constants
NTA_ITA_OPEN = u"[i]"
NTA_ITA_CLOSE = u"[/i]"
ASS_ITA_OPEN = u"{\i1}"
ASS_ITA_CLOSE = u"{\i0}"
SRT_ITA_OPEN = u"<i>"
SRT_ITA_CLOSE = u"</i>"

NTA_BOLD_OPEN = u"[b]"
NTA_BOLD_CLOSE = u"[/b]"
ASS_BOLD_OPEN = u"{\b1}"
ASS_BOLD_CLOSE = u"{\b0}"
SRT_BOLD_OPEN = u"<b>"
SRT_BOLD_CLOSE = u"</b>"

NTA_UNDER_OPEN = u"[u]"
NTA_UNDER_CLOSE = u"[/u]"
ASS_UNDER_OPEN = r"{\u1}"
ASS_UNDER_CLOSE = r"{\u0}"
SRT_UNDER_OPEN = u"<u>"
SRT_UNDER_CLOSE = u"</u>"

NTA_COLOR_OPEN = u"[c=%s]"
NTA_COLOR_CLOSE = u"[/c]"
ASS_COLOR_OPEN = u"{\c&%s%s%s&}"
ASS_COLOR_CLOSE = u"{\c}"
SRT_COLOR_OPEN = u"<font color=\"#%s%s%s\">"
SRT_COLOR_CLOSE = u"</font>"
