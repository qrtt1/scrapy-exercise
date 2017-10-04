import scrapy
from scrapy.selector import Selector
import re


class PttWebSpider(scrapy.Spider):
    name = "pttweb"
    page_template = 'https://www.ptt.cc/bbs/%s/index%d.html'

    def __init(self, board='', max_fetch_page=10):
        if not board:
            raise ValueError('[board] is required')
        self.board = board
        self.max_fetch_page = max_fetch_page

    def start_requests(self):
        url = 'https://www.ptt.cc/bbs/%s/index.html' % (self.board)
        yield scrapy.Request(url=url, callback=self.parse_page_list)

    def parse_page_list(self, response):
        for url in response.css('.btn-group-paging a::attr(href)').extract():
            page_number = re.findall('index(\d+).html', url)
            if page_number:
                number = int(page_number[0])
                if number > 1:
                    for page in range(number - self.max_fetch_page, number):
                        url = self.page_template % (self.board, page)
                        yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        print "parse_list", response.url
        for x in response.css('.r-list-container div a::attr(href)'):
            yield response.follow(x, self.save_text)

    def save_text(self, response):
        result = {}
        main_content = response.css("#main-content").extract_first()
        result.update({'text': re.sub(r'<[^>]+/?>', '', main_content)})
        yield result

    def save_page(self, response):
        author, board, title, publish_datetime = response.css(
            "#main-content span.article-meta-value::text").extract()
        result = {
            'author': author,
            'board': board,
            'title': title,
            'publish_datetime': publish_datetime}

        content = []
        for x in response.css(
                "#main-content::text, #main-content > div.push, #main-content > span.f2, #main-content span.f6").extract():
            if x.startswith('<div') and x.endswith('</div>'):
                sel = Selector(text=x)
                content += ["".join(sel.css('div.push > span::text').extract())]
            elif x.startswith('<span') and x.endswith('</span>'):
                sel = Selector(text=x)
                if sel.css('span.f6::text').extract():
                    content += [">> %s" %
                                sel.css('span.f6::text').extract()[0]]
                else:
                    content += ["".join(sel.css('span.f2::text').extract())]
            else:
                content += [x]

        result.update({'url': response.url, 'content': content})
        yield result
