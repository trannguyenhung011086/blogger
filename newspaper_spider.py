import newspaper
from newspaper import news_pool, Article

class ExtractArticles():
    
    def __init__(self):   
        self.sources = [
            'https://mmoculture.com/',
            'http://www.mmogames.com/'
        ]
        self.papers = []  
        self.pool = []
        self.paper = None
        self.articles = []
        self.newspaper = newspaper
        self.news_pool = news_pool

    def build_sources(self):
        try:
            for source in self.sources:
                self.paper = self.newspaper.build(source, memoize_articles = True, keep_article_html=True, verbose=True)
                self.papers.append(self.paper)
            self.news_pool.set(self.papers, threads_per_source=2) # (3*2) = 6 threads total
            self.news_pool.join()
            return self.papers
        except:
            raise Exception

    def parse_article(self,paper,order=0):
        self.paper = paper
        try:
            article = paper.articles[order]
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

    def parse_articles(self,pool):
        index = 0
        try:
            for paper in pool:
                size = paper.size()
                while index < size:
                    article = self.parse_article(paper,index)
                    self.articles.append(article)
                    index += 1
                if size == 0:
                    print('No new article for paper: {}!'.format(paper.brand))
            return self.articles
        except:
            raise Exception
