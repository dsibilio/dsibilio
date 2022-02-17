#!/usr/bin/env python

import feedparser
import re


TABLE_TEMPLATE = """
<table>
    {rows}
</table>
"""

LATEST_ARTICLE_TEMPLATE = """    <tr>
        <td>
            {banner}
        </td>
        <td>
            {title}
            {description}
        </td>
    </tr>
"""

BANNER_START = '<p class="medium-feed-image">'
BANNER_END = '</p>'

LATEST_ARTICLES_START = '<!-- latest articles start -->'
LATEST_ARTICLES_END = '<!-- latest articles end -->'
REPLACE_PATTERN = re.compile(rf'({LATEST_ARTICLES_START}).*({LATEST_ARTICLES_END})', re.DOTALL)


def add_row(feed_entry):
    title = f'<h2><a href="{feed_entry.link}">{feed_entry.title}</a></h2>'
    original_banner = feed_entry.description.split(BANNER_START)[1].split(BANNER_END)[0]
    banner = re.sub(r'width="\d+"', r'width="200"', original_banner)
    description = f'<i>{feed_entry.description.replace(original_banner, "")}</i>'
    return LATEST_ARTICLE_TEMPLATE.format(banner=banner, title=title, description=description)


def update_readme(updated_table):
    with open('README.md', mode='r+', encoding='utf-8') as readme:
        current = readme.read()
        updated = re.sub(REPLACE_PATTERN, rf'\1{updated_table}\2', current)
        readme.seek(0)
        readme.write(updated)
        readme.truncate()


res = feedparser.parse("https://medium.com/feed/@domenicosibilio")

rows = ''
for entry in res.entries[0:5]:
    rows += add_row(entry)

updated_table = TABLE_TEMPLATE.format(rows=rows.strip())
update_readme(updated_table)