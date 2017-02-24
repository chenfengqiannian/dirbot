from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy
import re
from dirbot.items import Website


class DmozSpider(Spider):
    name = "dmoz"
    count = 0
    urll=2
    COOKIES_ENABLED = False
    handle_httpstatus_list = [403,302]
    start_urls = [



    ]
    def __init__(self):
        super(DmozSpider, self).__init__()

        for i in range(1,20):
            url="http://jn.58.com/chuzu/0/pn%d/"%i
            self.start_urls.append(url)


    def parse(self, response):

        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        sites = response.css('li')
        items = []


        for site in sites:

            if(site.css("div.des>h2>a::text").extract()):
                #item=Website()
                #item['name']=site.css("div.des>h2>a::text").extract_first().strip(),

                self.count=self.count+1
                #item['count'] = self.count
                #items.append(item)
                url=site.css("div.des>h2>a::attr(href)").extract_first()

                #pattern = re.compile("([0-9]{1,}x.shtml)")
                pattern = re.compile("([0-9]{1,})x.shtml")
                html = pattern.findall(url)


                if(html):
                    '''
                    next_url="http://app.58.com/api/windex/scandetail/car/"+html[0]+"/" \
                             "?pid=799&pagetype=detail&topcate=house&list_" \
                             "name=zufang&local_name=nj&infoID=24217650909108&" \
                             "jumptype=native&title=%E8%AF%A6%E6%83%85&pid=799&fu" \
                             "ll_path=1,8&wlmode=sc&wltype=bro&wlsour=safari#app"
                             '''
                    next_url="http://m.58.com/jn/zufang/"+html[0]+"x.shtml?PGTID=0d300008-0010-9520-7e6d-95332c7b0b8d&ClickID=1&adtype=3"
                    yield scrapy.Request(url=next_url, callback=lambda res, b="jn": self.parsedetail(res, b))
                    '''
                    if(re.search("nj",response.url)):

                        yield scrapy.Request(url=next_url, callback=lambda res, b="nj": self.parsedetail(res, b))
                    if (re.search("jn", response.url)):
                        yield scrapy.Request(url=next_url, callback=lambda res, b="jn": self.parsedetail(res, b))
                        '''





                #yield scrapy.Request(url=next_url, callback=self.parsedetail)

                #print (self.count)

    def parsedetail(self, response,didian):

        if(response.css('.meta-tit').extract_first() is None):

            return
        title = response.css('.meta-tit::text').extract_first().strip()
        name=response.css('.profile-name::text').extract_first().strip()
        phone=response.css('.LinkPhone::attr(href)').extract_first().strip()
        item = Website()
        if(title or name or phone):
            item['title']=title
            item['name']=name
            item['phone']=phone
            item["didian"]=didian
            yield item






'''
class IPSpider(Spider):
    name = "IP"
    count = 0
    COOKIES_ENABLED = False



    start_urls = [
        "http://www.youdaili.net/Daili/guonei/27542.html",
        "http://www.youdaili.net/Daili/guonei/27542_2.html",
        "http://www.youdaili.net/Daili/guonei/27542_3.html",
        "http://www.youdaili.net/Daili/guonei/27542_4.html",
        "http://www.youdaili.net/Daili/guonei/27542_5.html",


    ]



    def parse(self, response):

        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        sites = response.css('p')
        items = []


        for site in sites:
            if(site.css("span::text").extract()):
                print site.css("span::text").extract()


'''

class DmozSpiderp(Spider):
    name = "dmozp"
    count = 0
    urll=2
    COOKIES_ENABLED = False
    #handle_httpstatus_list = [403]

    start_urls = [



    ]
    def __init__(self):
        super(DmozSpiderp, self).__init__()
        for i in range(1,20):
            url="http://nj.58.com/chuzu/0/pn%d/"%i
            self.start_urls.append(url)
        for i in range(1,20):
            url="http://jn.58.com/chuzu/0/pn%d/"%i
            self.start_urls.append(url)


    def parse(self, response):

        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        sites = response.css('li')
        items = []


        for site in sites:

            if(site.css("div.des>h2>a::text").extract()):
                #item=Website()
                #item['name']=site.css("div.des>h2>a::text").extract_first().strip(),

                self.count=self.count+1
                #item['count'] = self.count
                #items.append(item)
                url=site.css("div.des>h2>a::attr(href)").extract_first()

                #pattern = re.compile("([0-9]{1,}x.shtml)")
                pattern = re.compile("([0-9]{1,})x.shtml")
                html = pattern.findall(url)


                if(html):

                    next_url="http://app.58.com/api/windex/scandetail/car/"+html[0]+"/" \
                             "?pid=799&pagetype=detail&topcate=house&list_" \
                             "name=zufang&local_name=nj&infoID=24217650909108&" \
                             "jumptype=native&title=%E8%AF%A6%E6%83%85&pid=799&fu" \
                             "ll_path=1,8&wlmode=sc&wltype=bro&wlsour=safari#app"
                    if(re.search("nj",response.url)):

                        yield scrapy.Request(url=next_url, callback=lambda res, b="nj": self.parsedetail(res, b))
                    if (re.search("jn", response.url)):
                        yield scrapy.Request(url=next_url, callback=lambda res, b="jn": self.parsedetail(res, b))






                #yield scrapy.Request(url=next_url, callback=self.parsedetail)

                #print (self.count)


