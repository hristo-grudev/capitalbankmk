import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import CapitalbankmkItem
from itemloaders.processors import TakeFirst


class CapitalbankmkSpider(scrapy.Spider):
	name = 'capitalbankmk'
	start_urls = ['http://www.capitalbank.com.mk/NewsList.aspx?IdLanguage=1&IdRoot=1&IdType=1']

	def parse(self, response):
		post_links = response.xpath('//div[@class="section-left"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//ul[@class="paging_ul"]/li/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="head_top_news"]/h1/text()').get()
		description = response.xpath('//div[@style="margin-top: 350px;"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="box_news_slider1"]//text()[normalize-space()]').getall()
		date = [p.strip() for p in date]
		date = ' '.join(date).strip()
		date = re.sub('/', '', date)

		item = ItemLoader(item=CapitalbankmkItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
