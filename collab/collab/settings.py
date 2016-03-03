# Scrapy settings for collab project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import os

BOT_NAME = 'collab'

SPIDER_MODULES = ['collab.spiders']
NEWSPIDER_MODULE = 'collab.spiders'

DOWNLOADER_MIDDLEWARES = {
    'collab.middleware.CustomHttpProxyMiddleware': 543,
    'collab.middleware.CustomUserAgentMiddleware': 545,
}

########### Item pipeline
ITEM_PIPELINES = [
                  "collab.pipelines.MongoDBPipeline",
]

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapy-test'
MONGODB_COLLECTION = 'person_profiles'
MONGODB_UNIQ_KEY = '_id'
###########

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'

# Enable auto throttle
AUTOTHROTTLE_ENABLED = True

COOKIES_ENABLED = False

# Set your own download folder
DOWNLOAD_FILE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "download_file")


