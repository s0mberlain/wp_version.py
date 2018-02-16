from lxml import html
import requests
import re
import json
import sys

#DEFINITIONS
WP_LATEST_VERSION_URL = "https://wordpress.org/download/release-archive/"

#append "feed" to URL
args = json.loads(sys.argv[1])
url = args['params']

url = url.replace("\\", "")

WP_URL_TO_CHECK = str(url) + "feed/"

print(str(url))

REGEX_WP_VERSION = re.compile("\d+\.\d+\.\d+")
REGEX_WP_GET_GENERATOR = re.compile("<generator>.+<\/generator>")

#Get latest Wordpress Version from WP Site
wp_version = requests.get(WP_LATEST_VERSION_URL)
tree = html.fromstring(wp_version.content)

tag = tree.xpath('//*[@id="pagebody"]/div/div[1]/table[1]/tbody/tr[1]/td[1]/text()')

wp_latestVersion = REGEX_WP_VERSION.findall(str(tag))[0]

#Get the WP version of the Website to check
website_feed = requests.get(WP_URL_TO_CHECK)

generator = REGEX_WP_GET_GENERATOR.findall(website_feed.text)[0]

website_version = REGEX_WP_VERSION.findall(generator)[0]

if website_version != wp_latestVersion:
    websiteUpToDate = 0.0
    message = "WordPress version outdated"
else:
    websiteUpToDate = 1.0
    message = "WordPress version up to date"

jsonOutputString = (
'''<prtg>
<result>
<channel>WordPress up-to-date</channel>
<Float>1</Float>
<LimitMinError>0.5</LimitMinError>
<LimitErrorMsg>Website out of date</LimitErrorMsg>
<value>''' + str(websiteUpToDate) + '''</value>
<LimitMode>1</LimitMode>
</result>
<Text>Current WordPress Verison detected: ''' + str(website_version) + ''' // Latest WordPress Version ''' + str(wp_latestVersion) + '''</Text> 
</prtg>''')

print(jsonOutputString)
