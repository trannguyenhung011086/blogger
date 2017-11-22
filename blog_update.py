from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from oauth2client.file import Storage
import httplib2
from apiclient.discovery import build
import webbrowser
from settings import Settings
import re


class BlogUpdate():

    def __init__(self):
        self.labels = []

    def get_credentials(self):
        """Get credentials from Google Console API. 'credentials.json' is loaded from local."""
        scope = 'https://www.googleapis.com/auth/blogger'
        redirect_uri = 'http://localhost:8080/'
        flow = flow_from_clientsecrets(
            'credentials.json', scope,
            redirect_uri=redirect_uri)
        flow.params['access_type'] = 'offline'         # offline access
        flow.params['include_granted_scopes'] = 'true'   # incremental auth
        storage = Storage('credentials.dat')
        credentials = storage.get()

        if not credentials or credentials.invalid:
            # auth_uri = flow.step1_get_authorize_url()
            # webbrowser.open(auth_uri)
            # auth_code = raw_input('Enter the auth code: ')
            # credentials = flow.step2_exchange(auth_code)
            # storage.put(credentials)
            credentials = run_flow(flow, storage)

        return credentials

    def get_service(self):
        """Returns an authorised blogger api service."""
        credentials = self.get_credentials()
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('blogger', 'v3', http=http)
        return service

    def get_blog_info(self, blog_id):
        served = self.get_service()
        blogs = served.blogs()
        blog_get_obj = blogs.get(blogId=blog_id)
        details = blog_get_obj.execute()
        return details

    def get_posts(self, blog_id):
        served = self.get_service()
        posts = served.posts()
        post_get_obj = posts.list(blogId=blog_id)
        details = post_get_obj.execute()
        details = details['items']
        return details

    def add_post(self, body, blog_id):
        served = self.get_service()
        posts = served.posts()
        add_post = posts.insert(blogId=blog_id,
                                body=body, isDraft=False, fetchImages=True, fetchBody=True)
        details = add_post.execute()
        return details

    def set_labels(self, article_url, article_title):
        """Put scraped articles into categories based on keywords in url"""
        reg = re.compile('(//|//\w+\.)(.+\.\w+)(.*)')
        match = reg.search(article_url)
        base = match.group(2)
        base = base.replace('www.', '')
        cat = match.group(3)
        cat_keywords = cat.split('/')
        genre_list = ['rpg', 'strategy', 'tactic', 'action', 'card',
                      'sport', 'moba', 'simulation', 'sim', 'casual', 'platform']
        preview_list = ['quick look', 'first look', 'preview', 'hands-on']
        review_list = ['review']
        news_list = ['news', 'available', 'arriving', 'soon', 'update', 'upgrade', 'interview', 'information', 'confirm', 'gets', 'become', 'roll-out', 'might', 'concern', 'launch', 'invest', 'stop', 'pause', 'announce', 'reveal', 'debut', 'release', 'new', 'giveaway',
                     'gift', 'dlc', 'expansion', 'start', 'this month', 'this week', 'this year', 'goes live', 'upcoming', 'exhibit', 'showcase', 'open beta', 'closed beta', 'alpha', 'early version', 'shuts down', 'brief', 'introduce', 'singup', 'register']
        console_list = ['ps1', 'ps2', 'ps3', 'ps4', '3ds', 'gamecube',
                        'switch', 'wiiu',  'dreamcast', 'xbox', 'pc', 'mac', 'steam', 'gog', 'sony', 'nintendo', 'atlus', 'sega', 'tecmo', 'koei', 'spike', 'falcom', 'rockstar', 'EA', 'ubisoft']
        brand_list = ['apple', 'samsung', 'sony', 'htc',
                      'mediatek', 'logitech', 'LG', 'nokia', 'microsoft']
        os_list = ['windows', 'mac', 'ios', 'android', 'blackberry',
                   'ubuntu', 'linux', 'iphone', 'ipad', 'smartwatch']
        self.labels = []

        if base in Settings.mmogame_domain or base in Settings.retrogame_domain:
            for keyword in cat_keywords:
                for item in news_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append('News')
                for item in preview_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append('Preview')
                for item in review_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append('Review')
                for item in genre_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append(item.title())
                for item in console_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append(item.title())

        elif base in Settings.jp_domain:
            self.labels = ['Culture']
            for keyword in cat_keywords:
                if ('anime' in keyword) or ('anime' in article_title):
                    self.labels.append('Anime')
                if ('manga' in keyword) or ('manga' in article_title):
                    self.labels.append('Manga')
                if ('book' in keyword) or ('book' in article_title):
                    self.labels.append('Book')
                if ('cheat sheet' in keyword) or ('cheat sheet' in article_title):
                    self.labels.append('Cheat Sheet')
                if ('hobby' in keyword) or ('hobby' in article_title):
                    self.labels.append('Hobby')
                if ('toy' in keyword) or ('toy' in article_title):
                    self.labels.append('Toy')
                if ('travel' in keyword) or ('travel' in article_title):
                    self.labels.append('Tour')
                if 'study' in keyword or 'learn' in keyword or 'read' in keyword or 'listen' in keyword:
                    self.labels.append('Learning')

        elif base in Settings.tech_domain:
            self.labels = ['doi-song']
            for keyword in cat_keywords:
                if 'camera' in keyword:
                    self.labels.append('camera')
                if 'phone' in keyword or 'dien-thoai' in keyword or 'snapdragon' in keyword or 'mediatek' in keyword:
                    self.labels.append('phone')
                if 'crypto' in keyword or 'bitcoin' in keyword or 'etherium' in keyword:
                    self.labels.append('crypto')
                for item in brand_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append(item.title())
                for item in os_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append(item.title())

        self.labels = list(set(self.labels))

        return self.labels
