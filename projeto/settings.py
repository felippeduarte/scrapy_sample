# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'tutorial'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline', 'tutorial.pipelines.MySQLStorePipeline']

IMAGES_STORE = 'C:\Users\Felippe\Documents\Projetos\comprasargentina\imagens'
IMAGES_EXPIRES = 90
IMAGES_THUMBS = {
    'small': (80, 80),
    'big': (270, 270),
}