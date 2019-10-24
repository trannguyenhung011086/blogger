from settings import Settings
import re
import os
import requests


class BlogUpdate():

    def __init__(self):
        self.labels = []

    def get_blog_info(self, blog_id):
        url = "https://www.googleapis.com/blogger/v3/blogs/" + blog_id
        querystring = {"key": os.environ["API_KEY"]}
        response = requests.request("GET", url, params=querystring)
        return response.json()

    def get_posts(self, blog_id):
        url = "https://www.googleapis.com/blogger/v3/blogs/" + blog_id + "/posts"
        querystring = {"key": os.environ["API_KEY"]}
        response = requests.request("GET", url, params=querystring)
        return response.json()["items"]

    def add_post(self, body, blog_id):
        url = "https://www.googleapis.com/blogger/v3/blogs/" + blog_id + "/posts"
        payload = body
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + os.environ["ACCESS_TOKEN"],
        }
        response = requests.request(
            "POST", url, data=payload, headers=headers)
        return response.json()

    def set_labels(self, article_url, article_title):
        """Put scraped articles into categories based on keywords in url"""
        reg = re.compile('(//|//\w+\.)(.+\.\w+)(.*)')
        match = reg.search(article_url)
        base = match.group(2)
        base = base.replace('www.', '')
        cat = match.group(3)
        cat_keywords = cat.split('/')
        genre_list = ['rpg', 'strategy', 'tactic', 'action', 'card', 'adventure', 'sport', 'moba',
                      'MOBA', 'simulation', 'sim', 'casual', 'platform', 'horror', 'survival', 'mmo', 'MMO', 'puzzle']
        preview_list = ['quick look', 'first look',
                        'preview', 'hands-on', 'peek', 'trailer', 'spot']
        review_list = ['review']
        news_list = ['news', 'available', 'arriving', 'soon', 'update', 'upgrade', 'interview', 'information', 'confirm', 'gets', 'become', 'roll-out', 'might', 'concern', 'launch', 'invest', 'stop', 'pause', 'announce', 'reveal', 'debut', 'release', 'new', 'giveaway',
                     'gift', 'dlc', 'expansion', 'start', 'this month', 'this week', 'this year', 'goes live', 'upcoming', 'exhibit', 'showcase', 'open beta', 'closed beta', 'alpha', 'early version', 'shuts down', 'brief', 'introduce', 'singup', 'register']
        console_list = ['ps1', 'ps2', 'ps3', 'ps4', '3ds', 'gamecube',
                        'switch', 'wiiu',  'dreamcast', 'xbox', 'pc', 'mac', 'steam', 'gog']
        brand_list = ['apple', 'samsung', 'sony', 'htc', 'mediatek', 'logitech', 'LG', 'nokia', 'microsoft',
                      'sony', 'nintendo', 'atlus', 'sega', 'tecmo', 'koei', 'spike', 'falcom', 'rockstar', 'EA', 'ubisoft']
        os_list = ['windows', 'mac', 'ios', 'android', 'blackberry', 'ubuntu',
                   'linux', 'iphone', 'ipad', 'smartwatch', 'mobile', 'smartphone']
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
                        self.labels.append(item)
                for item in brand_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append(item.title())
                for item in os_list:
                    if (item in keyword) or (item in article_title):
                        self.labels.append(item)

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
                        self.labels.append(item)

        self.labels = list(set(self.labels))

        return self.labels
