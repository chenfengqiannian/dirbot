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
class DmozSpiderp(Spider):

    name = "ganjiershoufang"
    count = 0
    urll = 2
    COOKIES_ENABLED = False
    handle_httpstatus_list = [403, 302]

    start_urls = [



    ]

    def __init__(self, listlen=2):
        super(DmozSpiderp, self).__init__()
        self.listlen=int(listlen)

    def start_requests(self):

        for name in recity.cityname():
            item = Website()
            item["cityjx"]=name[0]
            for i in range(1, self.listlen):
                url = "http://%s.ganji.com/fang5/o%d/"% (name[0],i)

                yield scrapy.Request(url=url, callback=lambda res, b=name[0]: self.parse(res, b))
    def parse(self, response,cityname):



        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        sites = response.css('dl.f-list-item-wrap')
        items = []


        for site in sites:

            if(site.css("dd a::text").extract()):


                #item=Website()
                #item['name']=site.css("div.des>h2>a::text").extract_first().strip(),


                #item['count'] = self.count
                #items.append(item)
                url=site.css("a::attr(href)").extract_first()

                #pattern = re.compile("([0-9]{1,}x.shtml)")
                pattern = re.compile("([0-9]{1,})x.htm")
                html = pattern.findall(url)


                if(html):
                    item = Website()
                    item["cityjx"] = cityname
                    next_url="http://3g.ganji.com/jn_fang1/"+html[0]+"x"

                    item['url'] = next_url
                    img_next_url="http://jn.ganji.com"+url

                    yield scrapy.Request(url=img_next_url,callback=lambda res,b=item:self.parsedetailimg(res,b))
                    yield scrapy.Request(url=next_url, callback=lambda res, b=item: self.parsedetail2(res, b))

    def parsedetailimg(self,response,item):
        images = response.css('div.small-img > ul li')
        print images
        tu=0
        for image in images:
            if (image.css('::attr(data-image)')):
                image_url = image.css('::attr(data-image)').extract_first().strip()


                if (
                    image_url != "https://sta.ganjistatic1.com/src/image/mobile/touch/milan/house/detail_pic_default.jpg"):
                    tu=tu+1

                    yield scrapy.Request(url=image_url,
                                         callback=lambda res, b=item: self.pasre_image_url(res, b),meta={"tu":tu})


    def parsedetail2(self, response, item):

        item["title"] = response.css('#f_detail > div:nth-child(10) > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > p > i::text').extract_first().strip()
        item["price"] = float(response.css('span.price::text').extract_first().strip())
        item['rtype'] = 2
        item['cityjx'] = 'jn'
        item['community'] = response.css('#f_detail > div:nth-child(8) > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list-two.f-clear > li:nth-child(1) > span.content > a.xiaoqu.card-blue::text').extract_first().strip()

        huxing = response.css("#f_detail > div:nth-child(8) > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-child(1) > span.content::text").extract_first().strip()
        pingming=response.css("#f_detail > div:nth-child(8) > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-child(2) > span.content::text").extract_first().strip()
        print huxing
        pattern = re.compile(u"([0-9])室")
        pattern2 = re.compile(u"([0-9])厅")

        pattern3 = re.compile(u"([0-9])卫")
        pattern4 = re.compile(u"(.*?)㎡")
        if(pattern.findall(huxing)):

            item['housetype_shi'] = int(pattern.findall(huxing)[0])
        if (pattern2.findall(huxing)):
            item['housetype_ting'] = int(pattern2.findall(huxing)[0])

        if (pattern3.findall(huxing)):
            item['housetype_wei'] = int(pattern3.findall(huxing)[0])
        item['proportion'] = float(pattern4.findall(pingming)[0])

        if(response.css(
            "#f_detail > div:nth-child(8) > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-child(3) > span.content::text")):
            item['orientations'] = response.css('#f_detail > div:nth-child(8) > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-child(3) > span.content::text').extract_first().strip()
        if(response.css(
            '#f_detail > div:nth-child(8) > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-child(10) > span.content::text')):
            item['equip'] = response.css(
            '#f_detail > div:nth-child(8) > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-child(10) > span.content::text').extract_first().strip()
        item['content'] = response.css('body > div.detail-list > div:nth-child(2) > div.house-mian-info > div:nth-child(3) > div.comm-area.js-moreBox > div::text').extract_first().strip()
        item['fromWeb'] = 2
        diqu=response.css(
            'body > div.detail-list > div:nth-child(2) > div.house-xiaoqu > div.xq-addr.cont-padding > div::text').extract_first().strip()
        if (diqu):

            print diqu
            pattern4 = re.compile(u"位置:(.*?)-")

            if(pattern4.findall(diqu)):
                item['areatitle'] = pattern4.findall(diqu)[0]
            pattern5 = re.compile(r"-([\u4e00-\u9fa5]*)")
            if (pattern5.findall(diqu)):

                item['strettitle'] = pattern5.findall(diqu)[0]

            if (re.findall(r"([\u4e00-\u9fa5]*)",diqu)):
                item['housetypes'] =re.findall(r"([\u4e00-\u9fa5]*)",diqu)[-1]
        item['linkman'] = response.css('body > div.detail-list > div:nth-child(2) > div.house-broker.broker-float.js-float.active > div.broker.fl-l > div > span::text').extract_first().strip()
        item['tel'] = response.css('body > div.detail-list > div:nth-child(2) > div.house-broker.broker-float.js-float.active > a.tel.fl-l::attr(href)').extract_first().strip()
        import time
        mtime = int(time.mktime(time.strptime(a, '%Y-%m-%d')))
        item['updatetime'] = mtime
        if(response.css('body > div.detail-list > div:nth-child(2) > div.house-xiaoqu > div.map-wrap > a::attr(href)')):
            sel = response.css('body > div.detail-list > div:nth-child(2) > div.house-xiaoqu > div.map-wrap > a::attr(href)').extract_first().strip()
            print sel
            sellist=sel.split("/")
            if(sellist):
                lat = sellist[4]
                lon = sellist[5]
                print lat
                print lon


                item['ixiy'] = lat + "," + lon

        count=response.css('body > div.detail-list > div:nth-child(2) > div.house-mian-info > div:nth-child(1) > div.house-type > span:nth-child(3)::text').extract_first().strip()
        print count
        if (pattern2.findall(count)):
            item['countstorey'] = pattern2.findall(count)[0]

        item['storey_str'] = count
        if(response.css('body > div.detail-list > div:nth-child(2) > div.house-mian-info > div:nth-child(1) > div.house-price > span.price-type::text')):
            item['paytype']=response.css('body > div.detail-list > div:nth-child(2) > div.house-mian-info > div:nth-child(1) > div.house-price > span.price-type::text').extract_first().strip()
        configurelist=response.css('ul.house-icon>li')
        configure=""
        for i in configurelist:
            if i.css("gray"):
                if configure=="":

                    configure=i.css(".text::text").extract_first().strip()
                else:
                    configure=configure+"-"+i.css(".text::text").extract_first().strip()

        item['configure']=configure

        if(response.css('body > div.detail-list > div:nth-child(2) > div.house-mian-info > div:nth-child(1) > div.house-type > span:nth-child(6)::text')):

            item['equip']=response.css('body > div.detail-list > div:nth-child(2) > div.house-mian-info > div:nth-child(1) > div.house-type > span:nth-child(6)::text').extract_first().strip()






        yield item

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
            print('写入文件:%s%d' % (filename,tu))
            tu=tu-1
            if(tu<=0):

                yield item
        else:
            print response.status



                #yield scrapy.Request(url=next_url, callback=self.parsedetail)

                #print (self.count)