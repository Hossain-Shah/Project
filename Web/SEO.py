from urllib import parse
import html
from datetime import datetime
import requests
from requests_html import HTMLSession
import json
import re
import socket
from urllib.parse import urlparse
url="https://www.searchenginejournal.com/?s=google&search-orderby=relevance&searchfilter=0&search-date-from=January+1%2C+2016&search-date-to=January+7%2C+2019"
parsed_url=urlparse(url)
print(parsed_url)
print(parsed_url.netloc)
print(parsed_url.path)
url="https://www.searchenginejournal.com/category/digital-experience/"
parsed_url=urlparse(url)
print(parsed_url.path.split("/"))
bot_ip = "66.249.66.1"
host = socket.gethostbyaddr(bot_ip)
print(host[0])
log_line='66.249.66.1 - - [06/Jan/2019:14:04:19 +0200] "GET / HTTP/1.1" 200 - "" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'
regex='([(\d\.)]+) - - \[(.*?)\] \"(.*?)\" (\d+) - \"(.*?)\" \"(.*?)\"'
groups=re.match(regex, log_line).groups()
print(groups)
print(groups[5])
ip = socket.gethostbyname(host[0])
json_response = '{"website_name": "Search Engine Journal", "website_url":"https://www.searchenginejournal.com/"}'
parsed_response = json.loads(json_response)
print(parsed_response)
print(parsed_response["website_name"])
dt = datetime.strptime('Jan 5 2018 6:33PM', '%b %d %Y %I:%M%p')
print(dt)
title = "SEO <News & Tutorials>"
print(html.escape(title))
print(html.unescape(title))
url = "https://www.searchenginejournal.com/"
print(parse.quote(url))
api_uri = "https://www.googleapis.com/analytics/v3/data/ga?ids={gaid}&"\
 "start-date={start}&end-date={end}&metrics={metrics}&"\
 "dimensions={dimensions}&segment={segment}&access_token={token}&"\
 "max-results={max_results}"
r = requests.get(api_uri)
print(r.status_code)
print(r.headers['content-type'])
print(r.history)
print(r.url)
session = HTMLSession()
r = session.get('https://www.searchenginejournal.com/')
print(r.html.absolute_links)
print(r.html.xpath('//title/text()'))
print(r.html.xpath("//meta[@name='description']/@content"))
print(r.html.xpath("//link[@rel='canonical']/@href"))
print(r.html.xpath("//link[@rel='amphtml']/@href"))
print(r.html.xpath("//meta[@name='ROBOTS']/@content"))
print(r.html.xpath("//h1"))
print(r.html.xpath("//link[@rel='alternate']/@hreflang"))
print(r.html.xpath("//meta[@name='google-site-verification']/@content"))
print(r.html.render())
ajax_request='https://www.searchenginejournal.com/location.json'
r = requests.get(ajax_request)
results=r.json()
print(results)
