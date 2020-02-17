import json
import time
import requests

SCROLL     = "5m"
LIMIT      = 10000
URL        = "http://epfl.elasticsearch.spinn3r.com/content_*/_search?scroll=%s" % SCROLL
URL_SCROLL = "http://epfl.elasticsearch.spinn3r.com/_search/scroll"
TAG        = "coronavirus"
OUT        = "/Volumes/JAY_DATA/coronavirus/%d.json"

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
with open(OUT % cnt,'w') as fout:
    json.dump(output_data, fout)

total_downloaded = len(hits['hits'])
print('Downloaded %d records' % total_downloaded)

while len(hits['hits']) > 0:
  cnt      += 1
  scroll_id = data['_scroll_id']
 
  data_post = {}
  data_post['scroll_id'] = scroll_id
  data_post['scroll']    = SCROLL
  data_post = json.dumps(data_post)
  response = requests.post(URL_SCROLL, headers=HEADERS, data=data_post)
  if not response.text:
      print("empty response")
      continue

  data = json.loads(response.text)

  hits = data['hits']
  output_data = hits['hits']
  with open(OUT % cnt,'w') as fout:
    json.dump(output_data, fout)

  total_downloaded += len(hits['hits'])
  print('Downloaded %d records' % total_downloaded)
  if len(hits['hits']) == 0:
      print("no more hits")
      break

print("Writing %d records to file" % total_downloaded)

