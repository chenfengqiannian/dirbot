# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'


AUTO_PROXY = {
    'download_timeout': 30,
    'test_urls': [('http://upaiyun.com', 'online'), ('http://huaban.com', '33010602001878')],
    'ban_code': [403,500, 502, 503, 504,302],
'invalid_limit':100000

}


ITEM_PIPELINES = {'dirbot.pipelines.FilterWordsPipeline': 1}


DOWNLOADER_MIDDLEWARES = {

    'dirbot.autoproxy.AutoProxyMiddleware': 3000,
'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware':None
}