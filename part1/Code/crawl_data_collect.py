# Reference - https://www.bellingcat.com/resources/2015/08/13/using-python-to-mine-common-crawl/

import requests
import argparse
import time
import json
import StringIO

import gzip
import csv
import codecs
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d","--domain",required=True,help="The domain to target ie. cnn.com")
args = vars(ap.parse_args())

domain = args['domain']

# list of available indices
index_list = ["2019-04","2019-09","2019-11","2019-14","2019-16"]

keywords = ["trump", "president", "democrats",  "party", "election", "people", "polytics", "government", "republicans"]
crawl_data = []
#
# Searches the Common Crawl Index for a domain.
#
def search_domain(domain):

    record_list = []
    
    print("[*] Trying target domain: %s" % domain)
    
    for index in index_list:
        
        print("[*] Trying index %s" % index)
        
        cc_url  = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json" % domain
        
        response = requests.get(cc_url)
        
        if response.status_code == 200:
            
            records = response.content.splitlines()
            
            for record in records:
                record_list.append(json.loads(record))
            
            print("[*] Added %d results." % len(records))
            
    
    print("[*] Found a total of %d hits." % len(record_list))
    
    return record_list        

#
# Downloads a page from Common Crawl - adapted graciously from @Smerity - thanks man!
# https://gist.github.com/Smerity/56bc6f21a8adec920ebf
#
def download_page(record):

    offset, length = int(record['offset']), int(record['length'])
    offset_end = offset + length - 1

    # We'll get the file via HTTPS so we don't need to worry about S3 credentials
    # Getting the file on S3 is equivalent however - you can request a Range
    prefix = 'https://commoncrawl.s3.amazonaws.com/'
    # print prefix + record['filename']
    # We can then use the Range header to ask for just this set of bytes
    resp = requests.get(prefix + record['filename'], headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})
    
    # The page is stored compressed (gzip) to save space
    # We can extract it using the GZIP library
    raw_data = StringIO.StringIO(resp.content)
    f = gzip.GzipFile(fileobj=raw_data)
    
    # What we have now is just the WARC response, formatted:
    data = f.read()
    
    response = ""
    
    if len(data):
        try:
            warc, header, response = data.strip().split('\r\n\r\n', 2)
        except:
            pass
            
    return response



def checkForContent(html_content, found):
    parser = BeautifulSoup(html_content, "html.parser")
    for script in parser(["script", "style"]):
        script.extract()
    content = parser.get_text()
    # print(content)
    # print(text)
    if any(key in text for key in keywords):
        found += 1
        crawl_data.append(text)
    return found

record_list = search_domain(domain)
link_list   = []
found = 0

for i, record in enumerate(record_list):
    
    html_content = download_page(record)
    
    print("[*] Retrieved %d bytes for %s" % (len(html_content),record['url']))
    
    found = checkForContent(html_content, found)
    # link_list = extract_external_links(html_content,link_list)
    
print("Total Results found = " + str(found));

# print("[*] Total external links discovered: %d" % len(link_list))

with codecs.open("%s-links.csv" % "crawl_data","wb",encoding="utf-8") as output:

    fields = ["data"]
    
    logger = csv.DictWriter(output,fieldnames=fields)
    logger.writeheader()

    for data in crawl_data:
        logger.writerow({"data":data})

