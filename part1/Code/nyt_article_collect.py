pip install bs4

pip install request

import requests
import json
from bs4 import BeautifulSoup

links = json.loads(open("web_urls.json").read())
data_file = open("articles.txt", "w")
data_file.close()
i = 1
for link in links:
  try:
    data_file = open("articles.txt", "a")
    data = requests.get(link)
    soup = BeautifulSoup(data.text, 'html.parser')
    article_text = ""
    for node in soup.findAll('p'):
      article_text += ''.join(node.findAll(text=True))
      article_text += "\r\n"
    data_file.write(article_text)
    data_file.close()
    print(i)
    i = i + 1
  except:
    data_file.close()
    print("exception raised at" + str(i))
    i = i + 1
    continue


