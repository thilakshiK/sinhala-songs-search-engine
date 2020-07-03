import scrapy
from sinhala_songs.items import SinhalaSongsItem
from mtranslate import translate
import pickle
import re

def en_to_si(string):

    if string in dictionary:
        return dictionary[string]
    elif string.lower() == "unknown":
        return ''
    else:
        translation = translate(string, 'si', 'en')
        dictionary[string] = translation
        return translation


def translate_list(list):
    translated_array  = []
    for string in list:
        translated_array .append(en_to_si(string))

    return translated_array

dictionary = {}

class SinhalaLyrics(scrapy.Spider):
    name = 'my_scraper'

    # provide a page number in range (1,23)
    start_urls = ["https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=" + str(1) + ""]


    def parse(self, response):
        global dictionary

        try:
            dictionary = pickle.load(open('../dictionary.pickle', 'rb'))
        except (OSError, IOError):
            pickle.dump(dictionary, open('../dictionary.pickle', 'wb'))

        for href in response.xpath(
                "//main[contains(@id, 'genesis-content')]//div[contains(@class, 'entry-content')]//div[contains(@class, 'pt-cv-wrapper')]//h4[contains(@class, 'pt-cv-title')]/a/@href"):
            url = href.extract()

            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        global dictionary

        item =SinhalaSongsItem()

        # song name
        song_name = response.xpath("//div[contains(@class, 'site-inner')]//header[contains(@class, 'entry-header')]/h1/text()").extract()[0]
        item['song_name'] = re.split('\||–|-', song_name)[1].strip()

        # artist
        artist = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'su-column su-column-size-3-6')]//span[contains(@class, 'entry-categories')]/a/text()").extract()
        if len(artist) == 0:
            item['artist'] = []
        else:
            artist = translate_list(artist)
            item['artist'] = artist

        # lyrics writer
        lyrics_writer = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'su-column su-column-size-2-6')]//span[contains(@class, 'lyrics')]/a/text()").extract()
        if len(lyrics_writer) == 0:
            item['lyrics_writer'] = []
        else:
            lyrics_writer = translate_list(lyrics_writer)
            item['lyrics_writer'] = lyrics_writer

        # genre
        genre = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'su-column su-column-size-3-6')]//span[contains(@class, 'entry-tags')]/a/text()").extract()
        if len(genre) == 0:
            item['genre'] = []
        else:
            genre = translate_list(genre)
            item['genre'] = genre

        # music by
        music_by = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'su-column su-column-size-2-6')]//span[contains(@class, 'music')]/a/text()").extract()
        if len(music_by) == 0:
            item['music_by'] = []
        else:
            music_by = translate_list(music_by)
            item['music_by'] = music_by

        # views
        views = response.xpath("//div[contains(@class, 'entry-content')]/div[contains(@class, 'tptn_counter')]/text()").extract()[0]
        item['views'] = int(re.sub('[^0-9,]', "", views).replace(',', ''))

        # shares
        shares = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'nc_tweetContainer swp_share_button total_shares total_sharesalt')]/span[contains(@class, 'swp_count')]/text()").extract()[0]
        item['shares'] = int(re.sub('[^0-9,]', "", shares).replace(',', ''))

        # lyrics
        lyrics = response.xpath("//div[contains(@class, 'entry-content')]//pre/text()").extract()

        song = ''
        check = False

        for line in lyrics:
            lines = (re.sub("[\da-zA-Z\-â€”\[\]\(\)\}\{\@\_\!\#\+\$\%\^\&\*\<\>\?\|\~\:\âˆ†\/]", "", line)).split('\n')
            for line_l in lines:
                if not (line_l.isspace() or line_l == ""):
                    song += line_l.strip()
                    check = True
                else:
                    if check:
                        song += '\\n'
                        check = False

        item['lyrics'] = song

        pickle.dump(dictionary, open('../dictionary.pickle', 'wb'))

        yield item
