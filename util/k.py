#!/usr/bin/env python
# encoding: utf-8
"""
K.py

Created by Loïc Wolff on 2009-04-25.
Copyright (c) 2009 loicwolff.eu. All rights reserved.
"""

# tag constants
NTA_ITA_OPEN = "[i]"
NTA_ITA_CLOSE = "[/i]"
ASS_ITA_OPEN  = "{\i1}"
ASS_ITA_CLOSE = "{\i0}"
SRT_ITA_OPEN = "<i>"
SRT_ITA_CLOSE = "</i>"

NTA_BOLD_OPEN = "[b]"
NTA_BOLD_CLOSE = "[/b]"
ASS_BOLD_OPEN  = r"{\b1}"
ASS_BOLD_CLOSE = r"{\b0}"
SRT_BOLD_OPEN = "<b>"
SRT_BOLD_CLOSE = "</b>"

NTA_UNDER_OPEN = "[u]"
NTA_UNDER_CLOSE = "[/u]"
ASS_UNDER_OPEN  = "{\u1}"
ASS_UNDER_CLOSE = "{\u0}"
SRT_UNDER_OPEN = "<u>"
SRT_UNDER_CLOSE = "</u>"

NTA_COLOR_OPEN = "[c=%s]"
NTA_COLOR_CLOSE = "[/c]"
ASS_COLOR_OPEN = "{\c&%s%s%s&}"
ASS_COLOR_CLOSE = "{\c}"
SRT_COLOR_OPEN = '<font color="#%s%s%s">'
SRT_COLOR_CLOSE = "</font>"
