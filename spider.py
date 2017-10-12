from newspaper_spider import ExtractArticles

def spider_run():
    pool = ExtractArticles().build_sources()
    result = ExtractArticles().parse_articles(pool)
    return result

def add_post(result):
    try:
        for item in result:
            print('test')
        # call to blogger api
    except:
        raise Exception
