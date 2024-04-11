

import sys
import json
from time import mktime
from datetime import datetime

import feedparser as fp
import newspaper
from newspaper import Article


data = {}
data["newspapers"] = {}


def parse_config(fname):
   
    with open(fname, "r") as data_file:
        cfg = json.load(data_file)

    for company, value in cfg.items():
        if "link" not in value:
            raise ValueError(f"Configuration item {company} missing obligatory 'link'.")

    return cfg


def _handle_rss(company, value, count, limit):
   

    fpd = fp.parse(value["rss"])
    print(f"Downloading articles from {company}")
    news_paper = {"rss": value["rss"], "link": value["link"], "articles": []}
    for entry in fpd.entries:
        
        if not hasattr(entry, "published"):
            continue
        if count > limit:
            break
        article = {}
        article["link"] = entry.link
        date = entry.published_parsed
        article["published"] = datetime.fromtimestamp(mktime(date)).isoformat()
        try:
            content = Article(entry.link)
            content.download()
            content.parse()
        except Exception as err:
            # If the download for some reason fails (ex. 404) the
            # script will continue downloading the next article.
            print(err)
            print("continuing...")
            continue
        article["title"] = content.title
        article["text"] = content.text
        news_paper["articles"].append(article)
        print(f"{count} articles downloaded from {company}, url: {entry.link}")
        count = count + 1
    return count, news_paper
