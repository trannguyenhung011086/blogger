import newspaper
from newspaper import news_pool, Source
from settings import Settings


class ExtractArticles():

    def __init__(self):
        self.sources = []
        self.papers = []
        self.pool = []
        self.categories = []
        self.category = None
        self.paper = None
        self.articles = []
        self.article = None
        self.newspaper = newspaper
        self.news_pool = news_pool

    def build_sources(self):
        try:
            for domain in Settings.domain:
                source = 'http://%s' % domain
                self.sources.append(source)
            for source in self.sources:
                self.paper = Source(source)
                self.paper = self.newspaper.build(
                    source, memoize_articles=False, keep_article_html=True, verbose=True)
                print('Source: {} - Size: {}'.format(source, self.paper.size()))
                self.papers.append(self.paper)
            # (3*2) = 6 threads total
            self.news_pool.set(self.papers, threads_per_source=2)
            self.news_pool.join()
            return self.papers
        except:
            raise Exception

    def parse_article(self, paper, order=0):
        self.paper = paper
        try:
            self.article = paper.articles[order]
            article = self.article
            article.download()
            article.parse()
            brand = paper.brand
            url = article.url
            text = article.text
            html = article.article_html
            title = article.title
            images = article.images
            video = article.movies
            date = article.publish_date
            result = {
                'paper': brand,
                'article_url': url,
                'title': title,
                'text': text,
                'content': html,
                'video': video,
                'images': images,
                'publish_time': date
            }
            return result
        except:
            raise Exception

    def parse_articles(self, pool):
        index = 0
        try:
            for paper in pool:
                size = paper.size()
                brand = paper.brand
                while index < size:
                    article = self.parse_article(paper, index)
                    self.articles.append(article)
                    index += 1
                if size == 0:
                    pass
                print('Paper [{}] has new [{}] articles'.format(brand, size))
            return self.articles
        except:
            raise Exception

    def remove_invalid_articles(self, pool):
        try:
            index = 0
            for article in pool:
                title = article['title']
                if title is None or len(title) == 0:
                    print(
                        'Found article with invalid title [{}] at index [{}]'.format(title, index))
                    pool.pop(index)
                index += 1
            return pool
        except:
            raise Exception
