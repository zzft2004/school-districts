import scrapy
from ..items import FtxSchoolItem
from scrapy.loader import ItemLoader
from scrapy import Request
import re


class SchoolSpider(scrapy.Spider):
    name = 'school'
    allowed_domains = ['esf.sh.fang.com']
    start_urls = ['http://esf.sh.fang.com/school']
    domain = 'http://esf.sh.fang.com'

    # def parse(self, response):
    #     filename = "test.html"
    #     open(filename, 'wb').write(response.body)
    
    def parse(self, response):
        list_a = response.xpath('//div[@class = "qxName"]/a')
        for a in list_a:
            href = a.xpath('@href').extract()[0]
            region_name = a.xpath('text()').extract()[0]
            if region_name in ('浦东',):
                region_url = self.domain + href
                yield Request(url=region_url, callback=self.city_region)
    
    def city_region(self, response):
        region_name = response.xpath('//div[@class = "qxName"]/a[@class="org selected"]/text()').extract()[0]
        dinfo = {'region_name': region_name}
        res = response.xpath('//p[@class = "title"]/a')
        try:
            for a in res:
                if a:
                    href = a.xpath('@href').extract()[0]
                    house_info = self.domain + href
                    yield Request(house_info, meta=dinfo, callback=self.get_house_info)
        except Exception as e:
            print('error', e)
        
        nextpages = response.xpath('//div[@class="fanye gray6"]/a/@href').extract()
        for nextpage in nextpages:
            if nextpage:
                nexturl = house_info = self.domain + nextpage
                yield Request(url=nexturl, callback=self.city_region)

    def getinfobyre(self, instr, restr):
        m = re.search(restr, instr, re.S)

        if m:
            info = m.groups()[0]
        else:
            info = ''

        return info

    def make_district_info(self, restr):
        districts_list = []
        district_info = ''
        re_info = re.compile(r'<div class="houseInfo">.*?target="_blank">(.*?)</a>'
                            r'.*?rel="nofollow"><strong>(\d+)</strong>'
                            r'.*?<strong class="red">(\d+?)</strong>'
                            r'.*?</span>(.*?)<span class="gray6 ml30">', re.S)
        districts = re_info.findall(restr)
        for d in districts:
            if len(d) == 4:
                temp = '{0}-{1}套-{2}元-{3}'.format(d[0], d[1], d[2], d[3])
            else:
                temp = ['-'.join(d) ]
            districts_list.append(temp)
        district_info = '\"' + '\r\n'.join(districts_list) + '\"'

        return district_info
        
    def get_house_info(self, response):
        dinfo = response.meta
        iteml = ItemLoader(item=FtxSchoolItem(), response=response)
        iteml.add_value('region_name', dinfo['region_name'])
        iteml.add_xpath('school_name', '//p[@class="schoolname"]/span[@class="title"]/text()')

        a = response.xpath('//p[@class="schoolname"]/span[@class="info gray9 ml10"]/text()').extract()[0].split('   ')[0].split('|')
        iteml.add_value('school_type', a[0][1:])
        iteml.add_value('school_level', a[1])
        iteml.add_value('public_private', a[2])
        iteml.add_xpath('aver_price_m2', '//div[@class="info floatr"]//span[@class="red ft30A pr5"]/text()')
        school_address = self.getinfobyre(response.text, r'学校地址：</span>(.+?)</li>')
        iteml.add_value('school_address', school_address)
        xiaoqushu = self.getinfobyre(response.text, r'周边小区：</span>.+?>(\d.+?)</span>')
        iteml.add_value('xiaoqushu', xiaoqushu)
        xiaoqu_info = self.make_district_info(response.text)
        #iteml.add_xpath('xiaoqu', '//div[@class="houseInfo"]//a[1]/text()')
        iteml.add_value('xiaoqu', xiaoqu_info)
        school_advantage = response.xpath('//div[@class="info floatr"]//li[5]/span/text()').extract()
        iteml.add_value('school_advantage', school_advantage[1:])
        iteml.add_xpath('house_onsale', '//li[@class="buttonLi"]//span/strong/text()')
        return iteml.load_item()
