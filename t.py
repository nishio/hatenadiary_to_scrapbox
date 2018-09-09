# -*- coding: utf-8 -*-
"""

"""
import json
import codecs
import bs4
from collections import defaultdict

tree = bs4.BeautifulSoup(open("nishiohirokazu.xml"), bs4.builder.XML)

date_to_body = {}
ym_to_ymd = defaultdict(set)
y_to_ym = defaultdict(set)

for d in tree.diary.findAll("day"):
    date = d.attrs["date"]
    title = d.attrs["title"]
    body = d.body.text

    date_to_body[date] = body
    y, m, d = date.split("-")
    ym = "%s-%s" % (y, m)
    ym_to_ymd[ym].add(date)
    y_to_ym[y].add(ym)

pages = []
def add_page(title, lines):
    page = dict(
        title=title, 
        lines=[title] + lines)
    pages.append(page)    


for y in y_to_ym:
    add_page(
        title=y, 
        lines=["[%s]" % ym for ym in sorted(y_to_ym[y])])

for ym in ym_to_ymd:
    add_page(
        title=ym,
        lines=["[%s]" % ymd for ymd in sorted(ym_to_ymd[ym])])

for date in date_to_body:
    add_page(
        title=date,
        lines=date_to_body[date].split("\n"))

json.dump(dict(pages=pages), codecs.open('to_scrapbox.json', 'w', encoding="utf-8"), ensure_ascii=False, indent=2)
