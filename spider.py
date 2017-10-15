from newspaper_spider import ExtractArticles
from blog_update import BlogUpdate
import time


def spider_run():
    pool = ExtractArticles().build_sources()
    result = ExtractArticles().parse_articles(pool)
    result = ExtractArticles().remove_invalid_articles(result)
    result = result[::-1]
    return result


def post_to_blog(result):
    if len(result) > 0:
        current = time.time()
        for article in result:
            convert_current = time.strftime(
                "%Y-%m-%dT%H:%M:%S+07:00", time.localtime(current))
            title = article['title']
            content = article['content']
            body = {
                'kind': 'blogger#postList',
                'published': convert_current,
                'title': title,
                'content': content,
                'labels': ['News']
            }
            BlogUpdate().add_post(body)
            print('Added post with title [{}]'.format(title))
            current += 21600
    else:
        print('No new article add')


if __name__ == '__main__':
    result = spider_run()
    post_to_blog(result)
