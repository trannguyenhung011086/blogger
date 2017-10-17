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

    def set_labels(self, article_url):
        reg = re.compile('(//|//\w+\.)(.+\.\w+)(.*)')     
        match = reg.search(article_url)
        base = match.group(2)
        base = base.replace('www.', '')
        cat = match.group(3)
        cat_keywords = cat.split('/')
        if base in Settings.mmogame_domain:
            self.labels = ['News']
            for keyword in cat_keywords:
                if 'preview' in keyword:
                    self.labels.append('Preview')
                    self.labels.remove('News')
                elif 'review' in keyword:
                    self.labels.append('Review')
                    self.labels.remove('News')
                if 'rpg' in keyword:
                    self.labels.append('RPG')
                if 'strategy' in keyword or 'tactic' in keyword:
                    self.labels.append('Strategy')
                if 'action' in keyword:
                    self.labels.append('Action')
                if 'card' in keyword:
                    self.labels.append('Card')
                if 'sport' in keyword:
                    self.labels.append('Sport')
                if 'moba' in keyword:
                    self.labels.append('MOBA')
                if 'simulation' in keyword or 'sim' in keyword:
                    self.labels.append('Simulation')
                if 'casual' in keyword:
                    self.labels.append('Casual')
        elif base in Settings.retrogame_domain:
            self.labels = ['Console']
            for keyword in cat_keywords:
                if 'ps1' in keyword:
                    self.labels.append('PS1')
                if 'ps2' in keyword:
                    self.labels.append('PS2')
                if 'ps3' in keyword:
                    self.labels.append('PS3')
                if 'ps4' in keyword:
                    self.labels.append('PS4')
                if '3ds' in keyword:
                    self.labels.append('3DS')
                if 'gamecube' in keyword:
                    self.labels.append('Gamecube')
                if 'dreamcast' in keyword:
                    self.labels.append('Dreamcast')
                if 'xbox' in keyword:
                    self.labels.append('Xbox')
                if 'pc' in keyword or 'windows' in keyword or 'steam' in keyword or 'gog' in keyword:
                    self.labels.append('PC')
                    self.labels.remove('Console')
                if 'rpg' in keyword:
                    self.labels.append('RPG')
                if 'strategy' in keyword or 'tactic' in keyword:
                    self.labels.append('Strategy')
                if 'action' in keyword:
                    self.labels.append('Action')
                if 'platform' in keyword:
                    self.labels.append('Platform')
                if 'sport' in keyword:
                    self.labels.append('Sport')
                if 'simulation' in keyword or 'sim' in keyword:
                    self.labels.append('Simulation')
                if 'adventure' in keyword:
                    self.labels.append('Adventure')
                if 'news' in keyword or 'now' in keyword or 'available' in keyword or 'reveal' in keyword:
                    self.labels.append('News')
        elif base in Settings.tech_domain:
            self.labels = ['doi-song']
            for keyword in cat_keywords:
                if 'camera' in keyword:
                    self.labels.append('camera')
                if 'phone' in keyword or 'dien-thoai' in keyword or 'snapdragon' in keyword or 'mediatek' in keyword:
                    self.labels.append('phone')
                if 'crypto' in keyword or 'bitcoin' in keyword or 'etherium' in keyword:
                    self.labels.append('crypto')
                if 'ios' in keyword or 'iphone' in keyword or 'ipad' in keyword:
                    self.labels.append('ios')
                if 'android' in keyword:
                    self.labels.append('android')
        elif base in Settings.jp_domain:
            self.labels = ['Culture']
            for keyword in cat_keywords:
                if 'anime' in keyword:
                    self.labels.append('Anime')
                if 'manga' in keyword:
                    self.labels.append('Manga')
                if 'book' in keyword:
                    self.labels.append('Book')
                if 'cheat sheet' in keyword:
                    self.labels.append('Cheat Sheet')
                if 'console' in keyword:
                    self.labels.append('Console')
                if 'game' in keyword:
                    self.labels.append('Game')
                if 'hobby' in keyword or 'hobbies' in keyword:
                    self.labels.append('Hobby')
                if 'toy' in keyword:
                    self.labels.append('Toy')
                if 'travel' in keyword or 'tour' in keyword:
                    self.labels.append('Tour')
                if 'study' in keyword or 'learn' in keyword or 'read' in keyword or 'listen' in keyword:
                    self.labels.append('Learning')
        return self.labels
