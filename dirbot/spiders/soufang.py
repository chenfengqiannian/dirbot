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

    name = "soufang"
    count = 0
    urll = 2
    COOKIES_ENABLED = False
    handle_httpstatus_list = [403, 302]



    def __init__(self, listlen=2):
        super(DmozSpiderp, self).__init__()

        self.listlen=int(listlen)

    def start_requests(self):

        for name in recity.cityname():
            item = Website()
            item["cityjx"]=name[0]
            for i in range(1, self.listlen):
                url = "http://zu.%s.fang.com/house/a21-n3%d/"%(name[0],i)

                yield scrapy.Request(url=url, callback=lambda res, b=name[0]: self.parse(res, b))
    def parse(self, response,cityname):



        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """

        sites = response.css('.houseList dl')
        items = []


        for site in sites:

            if(site.css("p.title a::text").extract()):


                #item=Website()
                #item['name']=site.css("div.des>h2>a::text").extract_first().strip(),


                #item['count'] = self.count
                #items.append(item)
                url=site.css("a::attr(href)").extract_first()


                html = "http://zu.jn.fang.com"+url
                pattern = re.compile("_([0-9]{1,})_")
                htmlpeitao = pattern.findall(url)

                if(html):
                    item = Website()
                    item["cityjx"] = cityname


                    item['url'] =html
                    next_peitao="https://m.fang.com/zf/jn/JX_"+htmlpeitao[0]+".html"
                    #print next_peitao

                    yield scrapy.Request(url=next_peitao, callback=lambda res, b=item: self.parsedetailpeitao(res, b))
                    yield scrapy.Request(url=html, callback=lambda res, b=item: self.parsedetail2(res, b))


    def parsedetailpeitao(self, response, item):

        p=response.css("body > div.main > div.xqMain > section.xqBox.mb8 > div.ptss-zf.pdY14 > div.mt10 > span.on")

        configure=""
        for i in p:

            if configure == "":

                configure = i.css("::text").extract_first().strip()
            else:
                configure = configure + "-" + i.css("::text").extract_first().strip()

        item['configure']=configure





    def parsedetail2(self, response, item):

        item["title"] = response.css('div.h1-tit.rel > h1::text').extract_first().strip()
        item["price"] = float(response.css('div.houseInfor strong.red.price.bold::text').extract_first().strip())
        item['rtype'] = 1
        item['cityjx'] = 'jn'
        if (response.css('#gerenzfxq_C02_06::text')):
            item['community'] = response.css('#gerenzfxq_C02_06::text').extract_first().strip()

        timestring=response.css('body > div:nth-child(15) > div.h1-tit.rel > p.gray9 > span:nth-child(2)::text').extract_first().strip()
        timestring=timestring.split("：")[1].strip()

        import time
        mtime = int(time.mktime(time.strptime(timestring, '%Y/%m/%d %H:%M:%S')))
        item['updatetime'] = mtime

        huxing =  response.css("ul.house-info li:nth-child(2)::text").extract()
        item['orientations']=huxing[4]
        item['housetypes'] = huxing[0]
        item['storey_str']=huxing[3]
        for i in huxing:


            pattern = re.compile(u"([0-9])室")
            pattern2 = re.compile(u"([0-9])厅")

            pattern3 = re.compile(u"([0-9])卫")
            pattern4 = re.compile(u"(.*)㎡")
            pattern5=re.compile(u"(.*装修)")
            pattern6=re.compile(u"共([0-9]+)层")
            if(pattern.findall(i)):

                item['housetype_shi'] = int(pattern.findall(i)[0])
            if (pattern2.findall(i)):
                item['housetype_ting'] = int(pattern2.findall(i)[0])

            if (pattern3.findall(i)):
                item['housetype_wei'] = int(pattern3.findall(i)[0])
            if (pattern4.findall(i)):
                item['proportion'] = float(pattern4.findall(i)[0])
            if (pattern5.findall(i)):
                item['equip']=pattern5.findall(i)[0]
            if(pattern6.findall(i)):
                item["countstorey"]=pattern6.findall(i)[0]



        item['send_mode']=u'整租'
        if(response.css(
            "body > div.detail-list > div:nth-child(2) > div.house-mian-info > div:nth-child(1) > div.house-type > span:nth-child(4)::text")):
            item['orientations'] = response.css(
            "body > div.detail-list > div:nth-child(2) > div.house-mian-info > div:nth-child(1) > div.house-type > span:nth-child(4)::text").extract_first().strip()
        item['content'] = response.css('#fypj-pos > div > div > div.info.clearfix > div.agent-txt.agent-txt-per.floatl::text').extract_first().strip()
        item['fromWeb'] = 3






        item['areatitle'] =response.css('#gerenzfxq_B04_03::text').extract_first().strip()



        item['strettitle'] = response.css("#gerenzfxq_C02_08::text").extract_first().strip()

        item['adr']=response.css('body > div:nth-child(14) > div.houseInfor.mt15.clearfix > div.floatr.house-info-wrap > ul.house-info > li:nth-child(4) > span:nth-child(2)::text').extract_first().strip()

        item['linkman'] = response.css('div.floatr.house-info-wrap > div.phonewrap.clearfix > span.floatl.name::text').extract_first().strip()
        item['tel'] = response.css('div.floatr.house-info-wrap > div.phonewrap.clearfix > span.phoneicon.floatl::text').extract_first().strip()
        if(response.css('#rentid_208::attr(src)')):
            sel = response.css('#rentid_208::attr(src)').extract_first().strip()

            latpattern = re.compile(r'Baidu_coord_x=(.+?)&')
            lonpattern = re.compile(r'Baidu_coord_y=(.+?)&')
            if(latpattern.findall(sel)):
                lon =latpattern.findall(sel)[0]
                lat = lonpattern.findall(sel)[0]



                item['ixiy'] = lat + "," + lon



        pay=response.css('div.floatr.house-info-wrap > ul.house-info > li:nth-child(1)::text').extract_first()
        item['paytype']=pay.split(u"月")[1]





        images = response.css('#fytp-pos > div.alingC.mt20.fy-img > img')
        if(images):
            tu=0
            for image in images:
                if (image.css('::attr(data-src)')):

                    image_url = image.css('::attr(data-src)').extract_first().strip()
                    tu=tu+1

                    yield scrapy.Request(url=image_url,
                                             callback=lambda res, b=item: self.pasre_image_url(res, b),meta={"tu":tu})


       # yield item

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
            #print('写入文件:%s' % filename)
            tu = tu - 1
            if (tu <= 0):
                yield item




                #yield scrapy.Request(url=next_url, callback=self.parsedetail)

                ##print (self.count)