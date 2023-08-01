import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class Books_Crawler(scrapy.Spider):
    name = "books_crawler"
    def start_requests(self):
        url = "http://books.toscrape.com/"
        yield scrapy.Request(url = url,
                             callback = self.parse_front)
    
    # parses the book titles and price
    def parse_front(self, response):
        book_divs = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')
        titles_list = book_divs.xpath('.//h3/a/@title').extract()
        price_list = book_divs.xpath('.//p[@class="price_color"]/text()').extract()
        final_df['book_titles']=titles_list
        final_df['book_prices']=price_list
        url_list = book_divs.xpath('.//h3/a/@href').extract()
        for webpage in url_list:
            yield response.follow(url = webpage, callback = self.parse_back)

    # parses the books' description
    def parse_back(self, response):
        book_desc = response.xpath('//div[@id="content_inner"]/article/p/text()').extract()
        book_desc_list.append(book_desc)

book_desc_list = list()
final_df = pd.DataFrame()

process = CrawlerProcess()
process.crawl(Books_Crawler)
process.start()    

final_df['book_descs'] = book_desc_list
final_df.to_csv('test_books_scraping.csv', index=False)
