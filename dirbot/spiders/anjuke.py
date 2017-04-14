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

    name = "anjuke"
    count = 0
    urll = 2
    COOKIES_ENABLED = False
    handle_httpstatus_list = [404]

    start_urls = [



    ]
    def __init__(self,listlen=2):
        super(DmozSpiderp, self).__init__()
        '''
        for i in range(1,2):
            url="http://jn.zu.anjuke.com/fangyuan/p2/"
            self.start_urls.append(url)

    '''
    def start_requests(self):

        for name in recity.cityname():

            for i in range(1, 2):
                url = "http://%s.zu.anjuke.com/fangyuan/l2-p%d/" % (name[0], i)

                yield scrapy.Request(url=url, callback=lambda res, b=name[0]: self.parse(res, b))

    def parse(self, response, cityname):

        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """



        sites = response.css('div.zu-info > h3 ')
        items = []


        for site in sites:

            if(site.css("::text").extract()):


                #item=Website()
                #item['name']=site.css("div.des>h2>a::text").extract_first().strip(),


                #item['count'] = self.count
                #items.append(item)
                url=site.css("a::attr(href)").extract_first()


                html = url
                #pattern = re.compile("_([0-9]{1,})_")
                #htmlpeitao = pattern.findall(url)

                if(html):




                    #next_peitao="https://m.fang.com/zf/jn/JX_"+htmlpeitao[0]+".html"
                    ##print next_peitao
                    item = Website()
                    item['url'] = html
                    item["cityjx"] = cityname
                    #yield scrapy.Request(url=next_peitao, callback=lambda res, b=item: self.parsedetailpeitao(res, b))
                    headers = [
                        {
                            "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"},
                        {
                            "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)"},
                        {
                            "User-Agent": "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.0.9.2372 Mobile Safari/537.10+"},
                        {
                            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/JDQ39) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36"}
                    ]
                    yield scrapy.Request(url=html, callback=lambda res, b=item: self.parsedetail2(res, b),headers=headers[1])







    def parsedetail2(self, response, item):



        item["title"] = response.css('#content > div.wrapper > div.tit.cf > h3::text').extract_first().strip()
        item["price"] = float(response.css('#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.litem.fl > dl:nth-child(1) > dd > strong > span::text').extract_first().strip())
        item['rtype'] = 1
        item['cityjx'] = 'jn'
        if (response.css('#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.litem.fl > dl:nth-child(5) > dd > a::text')):
            item['community'] = response.css('#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.litem.fl > dl:nth-child(5) > dd > a::text').extract_first().strip()

        huxing =  response.css("#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.litem.fl > dl:nth-child(3) > dd::text").extract_first().strip()
        pingmi=response.css("#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.ritem.fr > dl:nth-child(3) > dd::text").extract_first().strip()


        item['orientations']=huxing[4]
        item['housetypes'] = huxing[0]
        item['storey_str']=huxing[3]



        pattern = re.compile(u"([0-9])室")
        pattern2 = re.compile(u"([0-9])厅")

        pattern3 = re.compile(u"([0-9])卫")
        pattern4 = re.compile(u"(.*)平米")
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
        if (response.css("#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.ritem.fr > dl:nth-child(2) > dd::text")):
            item['equip']=response.css("#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.ritem.fr > dl:nth-child(2) > dd::text").extract_first().strip()
        if(response.css("#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.ritem.fr > dl:nth-child(5) > dd::text")):
            item["countstorey"]=int(response.css("#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.ritem.fr > dl:nth-child(5) > dd::text").extract_first().split("/")[1])
            item['storey']=int(response.css("#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.ritem.fr > dl:nth-child(5) > dd::text").extract_first().split("/")[0])


        item['send_mode']=u'整租'
        if(response.css(
            "#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.ritem.fr > dl:nth-child(4) > dd::text")):
            item['orientations'] = response.css(
            "#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.ritem.fr > dl:nth-child(4) > dd::text").extract_first().strip()
        item['content'] = response.css('#propContent > div::text').extract_first()
        item['fromWeb'] = 4






        item['areatitle'] =response.css('#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.litem.fl > dl:nth-child(6) > dd > a:nth-child(1)::text').extract_first().strip()



        item['strettitle'] = response.css("#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.litem.fl > dl:nth-child(6) > dd > a:nth-child(2)::text").extract_first().strip()

        item['adr']=item['community']

        item['linkman'] = response.css('#broker_true_name::text').extract_first().strip()
        item['tel'] = response.css("div.broker_tel::text").extract_first()




        pay=response.css('#content > div.wrapper > div.mainbox.cf > div.lbox > div.pinfo > div.box > div.phraseobox.cf > div.litem.fl > dl:nth-child(2) > dd::text').extract_first()
        item['paytype']=pay





        images = response.css('#photoSlide > div > div.tabscon.tnow > div.bigps.photoslide.cf > div > ul li')
        if(images):
            tu=0
            for image in images:
                if (image.css('::attr(src)')):

                    image_url = image.css('::attr(src)').extract_first().strip()
                    tu=tu+1

                    yield scrapy.Request(url=image_url,
                                             callback=lambda res, b=item: self.pasre_image_url(res, b),meta={"tu":tu})




    def pasre_image_url(self, response, item):
        if response.status == 200:

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
            tu=response.meta['tu']
            tu=tu-1
            #print tu
            if(tu<=0):
                yield item
            #yield item




                #yield scrapy.Request(url=next_url, callback=self.parsedetail)

                ##print (self.count)