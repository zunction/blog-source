#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Theme-specific settings
SITENAME = u"Zhangsheng Lai"
DOMAIN = 'https://github.zunction.io'
BIO_TEXT = 'Learning How Machines Learn'
FOOTER_TEXT = 'Powered by <a href="http://getpelican.com">Pelican</a> and <a href="http://pages.github.com">GitHub&nbsp;Pages</a>.'

SITE_AUTHOR = 'Zhangsheng Lai'
TWITTER_USERNAME = '@zunction'
#GOOGLE_PLUS_URL = ''
INDEX_DESCRIPTION = 'Website and blog of Zhangsheng, a soon to be graduate student at SUTD and an employee of Nvidia'

SIDEBAR_LINKS = [
    '<a href="/about/">About</a>',
    '<a href="/archive/">Archive</a>',
]

ICONS_PATH = 'images/icons'

GOOGLE_FONTS = [
    "Raleway:400,600",
    "Source Code Pro",
]

SOCIAL_ICONS = [
    ('mailto:zhangsheng_lai@mymail.sutd.edu.sg', 'Email (zhangsheng_lai@mymail.sutd.edu.sg)', 'fa-envelope'),
    ('http://twitter.com/zunction', 'Twitter', 'fa-twitter'),
    ('http://github.com/zunction', 'GitHub', 'fa-github'),

]

THEME_COLOR = '#FF8000'


# Pelican settings
RELATIVE_URLS = False
SITEURL = 'https://github.zunction.io'
TIMEZONE = 'Asia/Singapore'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%B %d, %Y'
DEFAULT_PAGINATION = False
SUMMARY_MAX_LENGTH = 42

THEME = 'pelican-themes/pneumatic'

ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'

ARCHIVES_SAVE_AS = 'archive/index.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Disable authors, categories, tags, and category pages
DIRECT_TEMPLATES = ['index', 'archives']
CATEGORY_SAVE_AS = ''

# Disable Atom feed generation
FEED_ATOM = 'atom.xml'
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True
MD_EXTENSIONS = ['admonition', 'codehilite(linenums=True)', 'extra']

CACHE_CONTENT = False
DELETE_OUTPUT_DIRECTORY = False
OUTPUT_PATH = 'output/'
PATH = 'content'

templates = ['404.html']
TEMPLATE_PAGES = {page: page for page in templates}

STATIC_PATHS = ['images', 'uploads', 'extra']
IGNORE_FILES = ['.DS_Store', 'pneumatic.scss', 'pygments.css']

extras = ['CNAME', 'favicon.ico', 'keybase.txt', 'robots.txt']
EXTRA_PATH_METADATA = {'extra/%s' % file: {'path': file} for file in extras}

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['assets', 'neighbors', 'render_math', 'liquid_tags.img',
            'liquid_tags.include_code']
ASSET_SOURCE_PATHS = ['static']
ASSET_CONFIG = [
    ('cache', False),
    ('manifest', False),
    ('url_expire', False),
    ('versions', False),
]
DISQUS_SITENAME = 'zunction-github-io'
GOOGLE_ANALYTICS = 'UA-73850109-1'


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
