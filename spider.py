from newspaper_spider import ExtractArticles
from blog_update import BlogUpdate
import time


def spider_run():
    pool = ExtractArticles().build_sources()
    result = ExtractArticles().parse_articles(pool)
    result = ExtractArticles().remove_invalid_articles(result)
    result = result[::-1]
    return result

def check_post(result):
    # can only check published posts, not scheduled posts
    if len(result) > 0:
        posts = BlogUpdate().get_posts()
        print('Current posts: {}'.format(len(posts)))
        post_list = []
        for post in posts:
            post_list.append(post['title'])
        index = 0
        for article in result:
            if article['title'] in post_list:
                print('Blog has article [{}] already'.format(article['title']))
                result.pop(index)
            index += 1
        print('New posts: {}'.format(len(result)))
    else:
        print('No new article check')
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
    result = check_post(result)
    post_to_blog(result)
