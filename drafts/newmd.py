import sys
from datetime import datetime

# TEMPLATE = """
# Title: {title}
# Date: {year}-{month:02d}-{day:02d} {hour}:{minute:02d}
# Category:
# Tags:
# Slug: {slug}
# Author: zhangsheng
# Summary:
# Status: draft
#
#
# """

TEMPLATE = """
Title: {title}
Date: {year}-{month:02d}-{day:02d} {hour}:{minute:02d}
Tags:
Slug: {slug}
Author: zhangsheng
"""
def make_entry(title):
    today = datetime.today()
    slug = title.lower().strip().replace(' ', '-')
    date = str(today.year) + '-' + str('{:02d}'.format(today.month)) + '-' + str('{:02d}'.format(today.day))
    filename = date + '-' + slug
    author = 'zhangsheng'
    f_create = "{}.md".format(filename)
    t = TEMPLATE.strip().format(title=title,
                                year=today.year,
                                month=today.month,
                                day=today.day,
                                hour=today.hour,
                                minute=today.minute,
                                slug=slug,
                                author=author)
    with open(f_create, 'w') as w:
        w.write(t)
    print("File created -> " + f_create)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        make_entry(sys.argv[1])
    else:
        print('Need a "Title"')
