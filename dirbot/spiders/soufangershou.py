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

    name = "soufangershou"
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
            item["cityjx"] = name[0]
            for i in range(1, self.listlen):
                url = "http://esf.%s.fang.com/house/i3%d/" % (name[0], i)

                yield scrapy.Request(url=url, callback=lambda res, b=name[0]: self.parse(res, b))

    def parse(self, response, cityname):



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


                html = "http://esf.jn.fang.com"+url
                pattern = re.compile("_([0-9]{1,})_")
                htmlpeitao = pattern.findall(url)

                if(html):
                    item = Website()
                    item["cityjx"] = cityname

                    item['url'] =html
                    #next_peitao="https://m.fang.com/zf/jn/JX_"+htmlpeitao[0]+".html"
                    #print next_peitao

                    #yield scrapy.Request(url=next_peitao, callback=lambda res, b=item: self.parsedetailpeitao(res, b))
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

        item["title"] =response.css("div.title h1::text").extract_first().strip()
        item["price"] = float(response.css(".zongjia1 span.red20b::text").extract_first().strip())
        item['rtype'] = 2
        item['cityjx'] = 'jn'
        if (response.css('#agantesfxq_B02_08::text')):
            item['community'] = response.css('#agantesfxq_B02_08::text').extract_first().strip()

        huxing =  response.css("div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(1) > dd:nth-child(4)::text").extract_first().strip()
        pingmi=response.css('div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(1) > dd:nth-child(5) > span::text').extract_first().strip()


        item['orientations']= response.css('body > div:nth-child(11) > div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(2)::text').extract()[-1]
        if(response.css("div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(6)::text").extract()):
            item['housetypes'] = response.css("div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(6)::text").extract()
        item['storey_str']=response.css("body > div:nth-child(11) > div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(3)::text").extract()[-1]

        cengshu=response.css("div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(3)::text").extract()[-1]

        pattern = re.compile(u"([0-9])室")
        pattern2 = re.compile(u"([0-9])厅")

        pattern3 = re.compile(u"([0-9])卫")
        pattern4 = re.compile(u"(.*)㎡")
        pattern5=re.compile(u"(.*装修)")
        pattern6=re.compile(u"共([0-9]+)层")
        if(pattern.findall(huxing)):

            item['housetype_shi'] = int(pattern.findall(huxing)[0])
        if (pattern2.findall(huxing)):
            item['housetype_ting'] = int(pattern2.findall(huxing)[0])

        if (pattern3.findall(huxing)):
            item['housetype_wei'] = int(pattern3.findall(huxing)[0])

        if (pattern4.findall(pingmi)):
            item['proportion'] = float(pattern4.findall(pingmi)[0])

        item['equip']=response.css("div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(5)::text").extract()[-1]
        if(pattern6.findall(cengshu)):
            item["countstorey"]=pattern6.findall(cengshu)[0]




        if(response.css("div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(2)::text").extract()):
            item['orientations'] = response.css("div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(2)::text").extract()[-1]
        if(response.css(
            'div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(5)::text')):
            item['equip'] = response.css(
            'div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(5)::text').extract()[-1]
        item['content'] = "".join(response.css("#hsPro-pos span::text").extract())
        item['fromWeb'] = 3





        item['areatitle'] =response.css('#agantesfxq_B02_09::text').extract_first().strip()



        item['strettitle'] = response.css("#agantesfxq_B02_10::text").extract_first().strip()

        item['adr']=response.css('#agantesfxq_B02_08::text').extract_first().strip()

        item['linkman'] = response.css('#Span3::text').extract_first().strip()
        item['tel'] = response.css('#mobilecode::text').extract_first().strip()
        '''
        if(response.css('body > script:nth-child(3)')):
            sel = response.css('body > script:nth-child(3)::text')[-1].extract().strip()

            latpattern = re.compile(r'Baidu_coord_x=(.+?)&')
            lonpattern = re.compile(r'Baidu_coord_y=(.+?)&')
            if(latpattern.findall(sel)):
                lon =latpattern.findall(sel)[0]
                lat = lonpattern.findall(sel)[0]



                item['ixiy'] = lat + "," + lon

        '''
        #item['buildingstructure']=response.css('div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(4)::text').extract()[-1]
        #item['propertyright']=response.css('div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(8)::text').extract()[-1]
        #item['tradingnature'] = response.css('div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(8)::text').extract()[-1]
        #item['builddate'] = response.css(' div.main.clearfix > div.mainBoxL > div.houseInfor.clearfix > div.inforTxt > dl:nth-child(4) > dd:nth-child(1)::text').extract()[1]

        images = response.css('#esfjnxq_116 img')
        tu = 0
        if(images):
            for image in images:
                if (image.css('::attr(src)')):

                    image_url = image.css('::attr(src)').extract_first().strip()
                    tu = tu + 1
                    if (image_url):
                        yield scrapy.Request(url=image_url,
                                             callback=lambda res, b=item: self.pasre_image_url(res, b),meta={"tu":tu})
        images = response.css('#esfjnxq_117 img')

        if (images):

            for image in images:
                if (image.css('::attr(src)')):
                    image_url = image.css('::attr(src)').extract_first().strip()
                    if(image_url):

                        tu=tu+1
                        yield scrapy.Request(url=image_url,
                                         callback=lambda res, b=item: self.pasre_image_url(res, b),meta={"tu":tu})

        #yield item

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
            print('写入文件:%s' % filename)
            tu = tu - 1
            if (tu <= 0):
                yield item
        else:
            print response.status



                #yield scrapy.Request(url=next_url, callback=self.parsedetail)

                #print (self.count)