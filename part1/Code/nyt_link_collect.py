

pip install nytimesarticle

from nytimesarticle import articleAPI
my_api = articleAPI('***')

# articles = my_api.search( q = ['Trump', 'Democrats', 'Republican', 'President', 'Election'],
#      fq = {'headline':'Obama', 'source':['Reuters','AP', 'The New York Times']}, 
#      begin_date = 20190101 )

# articles = my_api.search(q='TRUMP', 
#                          fq={'headline':'Obama', 'source':['Reuters','AP', 'The New York Times']}, 
#                          begin_date = 20190101)

#articles = my_api.search( q = 'Obama', fq = {'headline':'Obama', 'source':['Reuters','AP', 'The New York Times']}, begin_date = 20111231, facet_field = ['source','day_of_week'], facet_filter = True )

# my_api.search( q = 'Obama', fq = {'headline':'Obama', 'source':['Reuters','AP', 'The New York Times']}, begin_date = 20111231, facet_field = ['source','day_of_week'], facet_filter = True )
import json
import time

keywords = ['Trump', 'Democrats', 'Republican', 'President', 'Election']
f = open("web_urls.json".format(keyword), "w")
result = []

for keyword in keywords:
  for i in range(15):
    data = my_api.search( q = keyword, begin_date = 20190101, page= i+1 )
    print(data)
    for row in data['response']['docs']:
      result.append(row['web_url'])
    time.sleep(7)

f.write(json.dumps(result))
f.close()

# data = my_api.search( q = 'Trump', begin_date = 20190101, page=1 )
# result = []
# for row in data['response']['docs']:
#   result.append(row['lead_paragraph'])

