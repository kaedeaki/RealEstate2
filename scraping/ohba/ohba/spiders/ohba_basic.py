# import scrapy


# class OhbaBasicSpider(scrapy.Spider):
#     name = 'ohba_basic'
#     allowed_domains = ['www.ohba.ca']
#     start_urls = ['https://www.ohba.ca/ohba_member_directory/?pages=1&association=ONTARIO&category=&q=']


#     def parse(self, response):
#         company_nodes = response.xpath('//div[@id="members"]/div[@class="supplier-unit normal"]')
        
                
#         for node in company_nodes:
#             phone_items = [line.strip() for line in node.xpath('.//div[@class="hidden-info"]/div[@class="right"]/p[3]//text()').getall() if line.strip()]
#             first_phone = phone_items[0] if phone_items else ''  # 最初の項目があればそれを取得、なければ空の文字列をセット

#             yield {
#                 'company_name': node.xpath('.//h2/text()').get(),
#                 'address_lines': [line.strip() for line in node.xpath('.//div[@class="hidden-info"]/div[@class="left"]/p[2]//text()').getall() if line.strip()],
#                 'person': node.xpath('.//div[@class="hidden-info"]/div[@class="right"]/p[2]/text()').get().strip(),
#                 'phone': first_phone,
#                 'web': node.xpath('div[@class="hidden-info"]/div[@class="right"]/p[3]/a[2]/text()').get().strip()                
#             }
            
#         next_page = response.xpath('//div[@id="pagination"]/a[1][@href]').get()
#         if next_page:
#             yield response.follow(url=next_page, callback=self.parse)



import scrapy
import json

class OHBASpider(scrapy.Spider):
    name = 'ohba'
    start_urls = ['https://www.ohba.ca/ohba_member_directory/?pages=1&association=&category=&q=']
    
    
    page_number = 1

    def parse(self, response):
        
        company_nodes = response.xpath('//div[@id="members"]/div[@class="supplier-unit normal"]')
                        
        for node in company_nodes:
            phone_items = [line.strip() for line in node.xpath('.//div[@class="hidden-info"]/div[@class="right"]/p[3]//text()').getall() if line.strip()]
            first_phone = phone_items[0] if phone_items else ''  
            
            web_element = node.xpath('.//div[@class="hidden-info"]/div[@class="right"]/p[3]/a[2]/text()').get()
            web = web_element.strip() if web_element else 'N/A'

            yield {
                'company_name': node.xpath('.//h2/text()').get(),
                'address_lines': [line.strip() for line in node.xpath('.//div[@class="hidden-info"]/div[@class="left"]/p[2]//text()').getall() if line.strip()],
                'person': node.xpath('.//div[@class="hidden-info"]/div[@class="right"]/p[2]/text()').get().strip(),
                'phone': first_phone,
                'web': web                
            }    
               

        for item in scraped_data:
            yield item    
        
        # item = {
        #     'company_name': node.xpath('.//h2/text()').get(),
        #     'address_lines': [line.strip() for line in node.xpath('.//div[@class="hidden-info"]/div[@class="left"]/p[2]//text()').getall() if line.strip()],
        #     'person': node.xpath('.//div[@class="hidden-info"]/div[@class="right"]/p[2]/text()').get().strip(),
        #     'phone': first_phone,
        #     'web': web
        # }

        #scraped_data.append(item)    
        # yield item      
         
        
        self.page_number += 1
        next_page = f'https://www.ohba.ca/ohba_member_directory/?pages={self.page_number}&association=&category=&q='
        if self.page_number <= MAX_PAGES:  
            yield response.follow(next_page, callback=self.parse)

    # def closed(self, reason):
        
    #     with open('builder_info.json', 'w') as json_file:
    #         json.dump(scraped_data, json_file)


MAX_PAGES = 388  
scraped_data = []

