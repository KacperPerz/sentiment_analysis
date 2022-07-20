import scrapy
from time import sleep
from scrapy.http import Request
from selenium import webdriver
from scrapy import Selector
from lubimy_czyt.items import LubimyCzytItem
from scrapy.loader import ItemLoader
from selenium.webdriver.common.by import By

class OpinionsSpider(scrapy.Spider):
    name = 'opinions'
    allowed_domains = ['lubimyczytac.pl']
    # start_urls = ['https://lubimyczytac.pl/ksiazka/3937616/gra-o-tron-edycja-ilustrowana']

    def start_requests(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://lubimyczytac.pl/ksiazka/3937616/gra-o-tron-edycja-ilustrowana')
        sleep(5)
        
        cookies_button = self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        if cookies_button:
            cookies_button.click()

        next_page_button = self.driver.find_element(By.XPATH, '//*[@class="page-item next-page "]/a[@class="page-link ml-0 stdPaginator btn"]')
        
        while next_page_button:
            sleep(1)
            next_page_button = self.driver.find_element(By.XPATH, '//*[@class="page-item next-page "]/a[@class="page-link ml-0 stdPaginator btn"]')
            comments = self.driver.find_elements(By.XPATH, '//form[@class="btn-link formToHref"]')
            comments = [comment.get_attribute('action') for comment in comments]

            for comment in comments:
                yield Request(comment, callback=self.parse_comment)
            
            sleep(1)
            self.driver.execute_script("arguments[0].click();", next_page_button)

        self.driver.quit()
        
    def parse_comment(self, response):
        rating_field = response.xpath('//div[@class="rating-value ml-auto p-2"]')
        rating = 'unknown'
        if rating_field:
            rating = rating_field.xpath('.//span[@class="big-number"]/text()').extract_first().strip()
        
        
        text = response.xpath('//*[@class="expandTextNoJS p-expanded js-expanded mb-0"]/text()').extract()
        text = ' '.join(text).replace('\n', '').replace('  ', ' ')

        yield {
            'text': text,
            'rating': rating
        }
        

        

