import json
import time
import requests
from funcy import project

SCROLL     = "5m"
LIMIT      = 10000
URL        = "http://epfl.elasticsearch.spinn3r.com/content_*/_search?scroll=%s" % SCROLL
URL_SCROLL = "http://epfl.elasticsearch.spinn3r.com/_search/scroll"

ACCOUNTS   = ['nytimes', 'guardian']
FROM_DATE  = "2020-01-01"
TO_DATE    = None

TAG        = "source_publisher_subtype:twitter"

OUT        = "/mnt/datastore/data/medias/%d.json"

fields     = ['author_handle','main','permalink','geo_location', 'geo_country', 'geo_state', 'geo_city' ,'lang','source_followers', 'source_following','published', 'likes', 'shares', 'replied', 'shared_type']

HEADERS = {
  'Content-Type': 'application/json',
  'X-vendor': 'epfl',
  'X-vendor-auth': 'J1Hr4Qc2a9UrU9tHweEO1KFDypA'
}


if len(ACCOUNTS) > 0:
  TAG += " AND (author_handle:" + ACCOUNTS[0]

for account in ACCOUNTS[1:]:
  TAG += " OR author_handle:" + account

if len(ACCOUNTS) > 0:
  TAG += ")"

if FROM_DATE is not None:
  TAG += " AND published:>" + FROM_DATE

if TO_DATE is not None:
  TAG += " AND published:<" + TO_DATE

data_post = {}
data_post['size'] = LIMIT
data_post['query'] = {}
data_post['query']['query_string'] = {}
data_post['query']['query_string']['query'] = "%s" % TAG

data_post = json.dumps(data_post)
response  = requests.post(URL, headers=HEADERS, data=data_post)

cnt  = 0

data = json.loads(response.text)
hits = data['hits']
output_data = hits['hits']
format_data = []
for o in output_data:
    format_data.append(project(o['_source'],fields))
with open(OUT % cnt,'w') as fout:
    json.dump(format_data, fout)

total_downloaded = len(hits['hits'])
print('Downloaded %d records' % total_downloaded)

while len(hits['hits']) > 0:
  cnt      += 1
  scroll_id = data['_scroll_id']

  data_post = {}
  data_post['scroll_id'] = scroll_id
  data_post['scroll']    = SCROLL
  data_post = json.dumps(data_post)
  try:
      response = requests.post(URL_SCROLL, headers=HEADERS, data=data_post)
  except:
      print("Broken connection, damn!")
      continue

  if not response.text:
      print("empty response")
      continue

  data = json.loads(response.text)
