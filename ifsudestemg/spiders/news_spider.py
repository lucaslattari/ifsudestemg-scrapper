import scrapy, re

class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = [
            'https://www.ifsudestemg.edu.br/noticias/reitoria'
        ]
        for i in range(20, 220, 20):
            urls.append('https://www.ifsudestemg.edu.br/noticias/reitoria?b_start:int=' + str(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article in response.css("article.tileItem.visualIEFloatFix.tile-collective-nitf-content"):
            imgUrl = ""
            if article.css("img").attrib:
                imgUrl = article.css("img").attrib["data-src"]

            dList = article.css("span.summary-view-icon::text").getall()
            for d in dList:
                match = re.search(r'(\d+/\d+/\d+)', d)
                if match is not None:
                    date = match.group(1)

                match = re.search(r'(\d+h\d+)', d)
                if match is not None:
                    time = match.group(1)

            yield {
                'headline': article.css("a.summary.url::text").get(),
                'imgUrl': imgUrl,
                'url': article.css("a.summary.url").attrib["href"],
                'description': article.css("span.description::text").get(),
                'date': date,
                'time': time,
            }
        #if nextPage is not None:
        #    yield response.follow(nextPage, callback=self.parse)
            '''
            headline = article.css("a.summary.url::text").get()
            if article.css("img").attrib:
                imgUrl = article.css("img").attrib["data-src"]
            url = article.css("a.summary.url").attrib["href"]
            description = article.css("span.description::text").get()
            dList = article.css("span.summary-view-icon::text").getall()
            for d in dList:
                match = re.search(r'(\d+/\d+/\d+)', d)
                if match is not None:
                    date = match.group(1)

                match = re.search(r'(\d+h\d+)', d)
                if match is not None:
                    time = match.group(1)

            print(headline, imgUrl, url, description, date, time)
            '''
        '''
        for a in response.css("ul.paginacao li a::attr(href)"):
            print(a.get())
            input()
        '''

        '''
        page = response.url.split("/")[-2]
        filename = 'news-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        '''
