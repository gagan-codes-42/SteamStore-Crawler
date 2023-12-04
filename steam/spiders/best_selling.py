import scrapy
import inspect
from scrapy.loader import ItemLoader
#from scrapy.ItemLoader.processors import Join, MapCompose, TakeFirst
from ..items import SteamItem



class BestSellingSpider(scrapy.Spider):
    name = "best_selling"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?filter=topsellers"]

    # I have shifted the classes for better arch. through ItemLoader
    
    # def clean_discount_rate(self,discount_rate): -> No need of this function, implemented in-line
    #     if discount_rate:
    #         return discount_rate.lstrip('.')
    #     return discount_rate
    
    # def get_original_price(self, selector_obj): -> better fields exist : no need of this code also
    #     original_price = ''
    #     div_with_discount = selector_obj.xpath(".//div[contains(@class, 'discount_prices')]")
    #     if len(div_with_discount) > 0:
    #         original_price = div_with_discount(".//div/discount_original_price/text()").get()
    #     else:
    #         original_price = selector_obj.xpath(".//div[contains(@class,'discount_original_price')]/text()").get()
        
    #     return original_price

    def parse(self, response):
        games = response.xpath("//div[@id='search_resultsRows']/a")
        for game in games:
            loader = ItemLoader(item=SteamItem(),selector=game,response=response)
            loader.add_xpath("game_url",".//@href")
            loader.add_xpath("img_url",".//div[@class='col search_capsule']/img/@src")
            loader.add_xpath("game_name",".//span[@class='title']/text()")
            loader.add_xpath("release_date",".//div[@class='col search_released responsive_secondrow']/text()")
            loader.add_xpath("platforms",".//span[contains(@class, 'platform_img') or @class='vr_supported']/@class")
            loader.add_xpath("reviews_summary",".//span[contains(@class,'search_review_summary')]/@data-tooltip-html")
            loader.add_xpath("discount_rate",".//div[contains(@class,'discount_pct')]/text()")
            loader.add_xpath("original_price",".//div[contains(@class,'discount_original_price')]/text()")
            loader.add_xpath("discounted_price",".//div[contains(@class,'discount_final_price')]/text()")
            # modifying below string because it has a lot of whitespaces and unwanted characters -> lstrip and rstrip
            # tip -> don't forget . in xpath
            # steam_item['release_date'] = game.xpath().get().lstrip().rstrip()
            # steam_item['platform'] = game.xpath("//span[contains(@class, 'platform_img') or @class='vr_supported']/@class") -> this is suboptimal way of reading platform : using class approach
            #steam_item['platforms'] = self.get_platforms(game.xpath().getall()) # -> this is optimal way of reading platform
            #steam_item['reviews_summary'] = self.remove_html(game.xpath().get()) # -> calling remove_html for cleaning html and reading tooltips
            
            yield loader.load_item()
        
        next_page = response.xpath(".//a[@class='pagebtn' and text()='>']/@href").get()
        if next_page:
            yield scrapy.Request(
                url = next_page,
                callback = self.parse
            )