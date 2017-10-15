from newspaper_spider import ExtractArticles
from blog_update import BlogUpdate
from settings import Settings
import time


def spider_run(source):
    pool = ExtractArticles().build_sources(source)
    result = ExtractArticles().parse_articles(pool)
    result = ExtractArticles().remove_invalid_articles(result)
    result = result[::-1]
    return result


def check_post(result, blog_id):
    # can only check published posts, not scheduled posts
    if len(result) > 0:
        blog = BlogUpdate().get_blog_info(blog_id)
        print('Blog name: {}'.format(blog['name']))
        posts = BlogUpdate().get_posts(blog_id)
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


def post_to_blog(result, blog_id):
    if len(result) > 0:
        current = time.time()
        labels = None
        if blog_id == Settings.blog_web360:
            labels = ['News']
        elif blog_id == Settings.blog_gog360:
            labels = ['Console']
        elif blog_id == Settings.blog_digi360:
            labels == ['doi-song']
        elif blog_id == Settings.blog_jp:
            labels == ['Culture']
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
                'labels': labels
            }
            BlogUpdate().add_post(body, blog_id)
            print('Added post with title [{}]'.format(title))
            current += 21600
    else:
        print('No new article add')


def update_blog(site):
    if site == 'mmo':
        blog = Settings.blog_web360
        source = Settings.mmogame_domain
    elif site == 'retro':
        blog = Settings.blog_gog360
        source = Settings.retrogame_domain
    elif site == 'jp':
        blog = Settings.blog_jp
        source = Settings.jp_domain
    elif site == 'digital':
        blog = Settings.blog_digi360
        source = Settings.tech_domain
    result = spider_run(source)
    result = check_post(result, blog)
    # post_to_blog(result, blog)


if __name__ == '__main__':
    update_blog('mmo')
    update_blog('retro')
    update_blog('jp')
    update_blog('digital')
