# coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy
import re
from PIL import Image
from dirbot.items import Website
from StringIO import StringIO
from datetime import datetime
import json
import os
from imagedown import imagedown
import recity


class DmozSpider(Spider):
    name = "58ershoufang"
    count = 0
    urll=2
    COOKIES_ENABLED = False
    handle_httpstatus_list = [403,302]
    start_urls = [



    ]

    def __init__(self, listlen=2):
        super(DmozSpider, self).__init__()
        self.listlen=int(listlen)
        '''
        for i in range(1,2):
            url="http://jn.58.com/ershoufang/0/pn%d/?PGTID=0d30000c-0010-960d-8108-c95d0e93ceeb&ClickID=5"%i
            self.start_urls.append(url)

    '''

    def start_requests(self):

        for name in recity.cityname():

            for i in range(1, self.listlen):
                url = "http://%s.58.com/ershoufang/0/pn%d/?PGTID=0d30000c-0010-960d-8108-c95d0e93ceeb&ClickID=5" % (name[0],i)

                yield scrapy.Request(url=url, callback=lambda res, b=name[0]: self.parse(res, b))
    def parse(self, response,cityname):





        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        sites = response.css('.bthead')
        items = []


        for site in sites:


            url=site.css('a::attr(href)').extract_first().strip()

            pattern = re.compile("([0-9]{1,})x.shtml")
            html = pattern.findall(url)


            if(html):

                next_url_get_phone="http://wap.58.com/jn/ershoufang/"+html[0]+"x.shtml?device=wap&PGTID=0d40000c-0078-06d8-1615-5d61c34fad4e&ClickID=5"
                next_url="http://jn.58.com/ershoufang/"+html[0]+"x.shtml"

                item = Website()
                item["cityjx"] = cityname
                #print next_url
                item['url']=next_url
                yield scrapy.Request(url=next_url_get_phone, callback=lambda res, b=item: self.parsedetail(res, b))
                yield scrapy.Request(url=next_url, callback=lambda res, b=item: self.parsedetail2(res, b))









    def parsedetail(self, response,item):


        #title = response.css('.meta-tit::text').extract_first().strip()
        #name=response.css('.profile-name::text').extract_first().strip()

        if(response.css('body > div > font')):

            phone=response.css('body > div > font::text').extract_first().strip()
            #print "$$#$#$#$#"
            #print phone
            count=response.xpath('/html/body/div/text()[13]').extract_first().strip()

            pattern = re.compile(u"第([0-9]{1,})层")
            pattern2=re.compile(u"共([0-9]{1,})层")
            if(pattern.findall(count)):
                item['storey']=pattern.findall(count)[0]
            if(pattern2.findall(count)):
                item['countstorey']=pattern2.findall(count)[0]


            item['storey_str'] =count



            item['tel']=phone

            #yield item
    def parsedetail2(self,response,item):


        item["title"]=response.css('.house-title h1::text').extract_first().strip()
        item["price"]=float(response.css('p.house-basic-item1 span.price::text').extract_first().strip())
        item['rtype']=2

        item['community']=response.css('span.c_000.mr_10 > a::text').extract_first().strip()



        huxing=response.css('#main > div.col.detailPrimary.mb15 > div.col_sub.maintop.mb30.clearfix > div.col_sub.sumary > ul > li:nth-child(4) > div.su_con::text').extract_first().strip()

        pattern = re.compile(u"([0-9])室")
        pattern2=re.compile(u"([0-9])厅")

        pattern3=re.compile(u"([0-9])卫")
        pattern4=re.compile(u"(.*)㎡")
        item['housetype_shi'] = int(pattern.findall(huxing)[0])


        item['housetype_ting']=int(pattern2.findall(huxing)[0])
        item['housetype_wei']=int(pattern3.findall(huxing)[0])
        item['proportion']=float(pattern4.findall(huxing)[0])


        item['housetype']=response.css('#fyms > div:nth-child(1) > div > ul > li:nth-child(2) > ul > li:nth-child(2)::text').extract_first().strip()
        item['orientations']=response.css("#fyms > div:nth-child(1) > div > ul > li:nth-child(4) > ul > li:nth-child(4)::text").extract_first().strip()
        item['equip']=response.css('#fyms > div:nth-child(1) > div > ul > li:nth-child(1) > ul > li:nth-child(4)::text').extract_first().strip()
        item['content']=response.css('.description_con p::text').extract_first().strip()
        item['propertyright']=response.css("#fyms > div:nth-child(1) > div > ul > li:nth-child(4) > ul > li:nth-child(2)::text").extract_first().strip()
        item['salehousetype']=response.css('#fyms > div:nth-child(1) > div > ul > li:nth-child(2) > ul > li:nth-child(2)::text').extract_first().strip()
        item['builddate']=response.css('#fyms > div:nth-child(1) > div > ul > li:nth-child(3) > ul > li:nth-child(2)::text').extract_first().strip()
        item['fromWeb']=1
        if(response.css('.su_tit+a::text').extract_first()):
            item['areatitle']=response.css('.su_tit+a::text').extract_first().strip()
        if(response.css('.su_tit+a+a::text').extract_first()):
            item['strettitle']= response.css('.su_tit+a+a::text').extract_first().strip()

        item['buildingstructure']=response.css('#fyms > div:nth-child(1) > div > ul > li:nth-child(2) > ul > li:nth-child(4)::text').extract_first().strip()
        item['tradingnature']=response.css('#fyms > div:nth-child(1) > div > ul > li:nth-child(2) > ul > li:nth-child(2)::text').extract_first().strip()
        item['housetypes']=item['tradingnature']

        item['linkman']=response.css('.su_tit+div a[rel=nofollow]::text').extract_first().strip()

        sel = response.css('script::text')[0].extract()
        #print sel
        latpattern = re.compile(r'"baidulat":(.*?),')
        lonpattern=re.compile(r'"baidulon":(.*?),')
        timepattern=re.compile(r'"I":"9773","V":"(\d)*"')
        lat=latpattern.findall(sel)[0]
        lon=lonpattern.findall(sel)[0]
        timestring=timepattern.findall(sel)[0]
        #print lat
        #print lon

        import time
        mtime = int(time.mktime(time.strptime(timestring, '%Y%m%d%H%M%S')))

        item['updatetime'] = mtime

        if(lat!='null'):
            lon=lon.replace("}","")
            item['ixiy']=lat+","+lon




        images=response.css('.descriptionImg')
        tu=0
        for image in images:

            image_url=image.css('img::attr(src)').extract_first().strip()
            tu=tu+1
            yield scrapy.Request(url=image_url, callback=lambda res, b=item: self.pasre_image_url(res, b),meta={"tu":tu})






    def pasre_image_url(self, response, item):
        if response.status == 200:
            tu=response.meta['tu']
            im = Image.open(StringIO(response.body))
            des_dir = 'images' + os.sep
            if (not os.path.exists(des_dir)):
                os.mkdir(des_dir)

            filename = ''.join([des_dir, datetime.today().__str__(), '.', im.format])

            if ('img' in item.keys()):
                item["img"] = item["img"] + "," + filename

            else:
                item['img'] = filename

            im.save(filename)
            #print('写入文件:%s%d' % (filename,tu))
            tu=tu-1

            if(tu<=0):
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
                #print site.css("span::text").extract()


'''





