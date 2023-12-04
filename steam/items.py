# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

# getting multiple platform information per game
def get_platforms(one_class):
    platforms = []

    #for item in one_class: -> this line gives multiples of platform
    platform = one_class.split(" ")[-1] #-1 represents to add vr-supported since it doesn't follows the format of ["platform","win"], etc
    if platform == 'win':
        platforms.append("Windows")
    if platform == 'mac':
        platforms.append("Mac OS")
    if platform == 'linux':
        platforms.append("Linux")
    if platform == 'vr_supported':
        platforms.append("VR Supported")
        
    return platforms
        

# to read reviews from tooltips also
def remove_html(review_summary):
    cleaned_review_summary = ''
    try:
        cleaned_review_summary = remove_tags(review_summary)
    except TypeError:
        cleaned_review_summary = 'No Reviews'
        
    return cleaned_review_summary

class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    game_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    img_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor = TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor = TakeFirst()
    )

    platforms = scrapy.Field(
        input_processor = MapCompose(get_platforms)
    )

    reviews_summary = scrapy.Field(
        input_processor = MapCompose(remove_html),
        output_processor = TakeFirst()
    )
    original_price = scrapy.Field(
        output_processor = TakeFirst()
    )
    discounted_price = scrapy.Field(
        output_processor = TakeFirst()
    )
    discount_rate = scrapy.Field(
        output_processor = TakeFirst()
    )
