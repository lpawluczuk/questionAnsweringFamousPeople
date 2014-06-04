# Scrapy settings for dates project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dates'

SPIDER_MODULES = ['dates.spiders']
NEWSPIDER_MODULE = 'dates.spiders'
ITEM_PIPELINES = ['dates.pipelines.DatesPipeline']

DOWNLOAD_DELAY = 0.5 
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'dates (+http://www.yourdomain.com)'
