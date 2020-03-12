import json
import time
import requests
from funcy import project
 
SCROLL     = "5m"
LIMIT      = 10000
URL        = "http://epfl.elasticsearch.spinn3r.com/content_*/_search?scroll=%s" % SCROLL
URL_SCROLL = "http://epfl.elasticsearch.spinn3r.com/_search/scroll"
TAG        = "((main:virus AND main:Wuhan)  OR main:coronavirus  OR main:nCoV_2019) AND source_publisher_subtype:twitter"
OUT        = "/mnt/datastore/data/coronavirus/%d.json"

fields     = ['author_handle','main','permalink','geo_location', 'geo_country', 'geo_state', 'geo_city' ,'lang','source_followers', 'source_following','published', 'likes', 'shares', 'replied', 'shared_type']

HEADERS = {
  'Content-Type': 'application/json',
  'X-vendor': 'epfl',
  'X-vendor-auth': 'J1Hr4Qc2a9UrU9tHweEO1KFDypA'
}

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

  hits = data['hits']
  output_data = hits['hits']
  format_data = []
  for o in output_data:
      format_data.append(project(o['_source'],fields))
  with open(OUT % cnt,'w') as fout:
      json.dump(format_data, fout)

  total_downloaded += len(hits['hits'])
  print('Downloaded %d records' % total_downloaded)
  if len(hits['hits']) == 0:
      print("no more hits")
      break

print("Writing %d records to file" % total_downloaded)

