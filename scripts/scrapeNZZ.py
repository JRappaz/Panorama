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
    with requests.get(url) as res:
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
    max_limit = 500
    steps = range(offset, limit + max_limit, max_limit)

    for step in steps:
        url  = "https://enrico.nzz-tech.ch/v2/newest-articles?product=nzz&limit={}&offset={}".format(max_limit, step)
        with requests.get(url) as res:
            articles = json.loads(res.text)

        for i, article in enumerate(articles['data']):
            print("article ", str(step + i), "\r", end="")
            try:
                art = proc_article(article['metadata'])
                save(art,outdir)
            except: 
                print("Error with: ", article['metadata']['url'])


scrape(10000, 0,"/mnt/datastore/data/medias/nzz/")
