import os
import json
import pprint
import requests
import validators
from bs4 import BeautifulSoup

def proc_comments(comlist):
    out = []
    if not comlist:
        return out
    for c in comlist.findAll("li", {"class": "comment"}):
        com = {}
        com['author'] = c.find("span", {"class": "fn"}).text
        com['date']   = c.find("time").get("datetime")
        com['body']   = c.find("div", {'class': 'comment-content'}).text
        out.append(com)
    return out

def extract_link(body_el):
    out = []
    for l in body_el.findAll("a"):
        ll = l.get("href")
        try:
            if validators.url(ll):
                out.append(ll)
        except:
            continue
    return out

def proc_article(article):
    url = article['url']
    res  = requests.get(url)
    soup = BeautifulSoup(res.content, features="lxml")
    body_el = soup.findAll(True ,{"class": "articlecomponent"})



    store = {}
    store['id']       = article['documentId']
    store['title']    = article['title']
    store['body']     = "\n".join([p.text for p in body_el])
    store['links']    = extract_link(soup.find("div" ,{"class": "article"}))
    store['date']     = article['publicationDate']
    store['url'] = url

    return store

def save(art,outdir):
    with open(os.path.join(outdir,art['id'] + '.json'),'w') as fout:
        json.dump(art, fout)

def file_exist(post_id):
    return os.path.exists(os.path.join("data",post_id+"json"))

def scrape(limit, offset,outdir):
    url = "https://enrico.nzz-tech.ch/v2/newest-articles?product=nzz&limit=" + str(limit) + "&offset=" + str(offset)
    res  = requests.get(url)
    articles = json.loads(res.text)

    for i, article in enumerate(articles['data']):
        print("article ", str(i), "\r", end="")
        art = proc_article(article['metadata'])
        save(art,outdir)


scrape(50, 0,"test/")
