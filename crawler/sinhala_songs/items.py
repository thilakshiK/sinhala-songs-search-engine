# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinhalaSongsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    song_name = scrapy.Field()
    artist = scrapy.Field()
    lyrics_writer = scrapy.Field()
    genre = scrapy.Field()
    music_by = scrapy.Field()
    lyrics = scrapy.Field()
    views = scrapy.Field()
    shares = scrapy.Field()


