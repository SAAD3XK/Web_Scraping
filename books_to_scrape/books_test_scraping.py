import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class Books_Crawler(scrapy.Spider):
    name = "books_crawler"

    def start_requests(self):
        for i in range(1, 51):
            temp_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            yield scrapy.Request(url = temp_url,
                                callback = self.parse_front)
    
    # parses the book titles and price
    def parse_front(self, response):
        book_divs = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]')
        titles_list = book_divs.xpath('.//h3/a/@title').extract()
        price_list = book_divs.xpath('.//p[@class="price_color"]/text()').extract()
        url_list = book_divs.xpath('.//h3/a/@href').extract()
        for title, price, url in zip(titles_list, price_list, url_list):
            yield response.follow(url=url, callback=self.parse_back,
                                  cb_kwargs={'title': title, 'price': price, 'url': url})

    def parse_back(self, response, title, price, url):
        book_desc = response.xpath('//div[@id="content_inner"]/article/p/text()').extract()
        if book_desc:
            book_desc_list.append(book_desc[0])  # Take only the first description if available
        else:
            book_desc_list.append(-1)  # Use -1 to represent missing description
        book_titles_list.append(title)
        book_prices_list.append(price)
        base_url = 'https://books.toscrape.com/catalogue/'
        book_page_links_list.append(base_url + url)


book_titles_list = list()
book_prices_list = list()
book_desc_list = list()
book_page_links_list = list()

process = CrawlerProcess()
process.crawl(Books_Crawler)
process.start()    

data = {
    "book_titles": book_titles_list,
    "book_prices": book_prices_list,
    "book_descs": book_desc_list,
    "page_links": book_page_links_list
}

final_df = pd.DataFrame(data)
final_df.to_csv('test_books_scraping.csv', index=False)
