from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
import webbrowser

def get_credentials():
    scope = 'https://www.googleapis.com/auth/blogger'
    flow = flow_from_clientsecrets(
        'credentials.json', scope,
        redirect_uri='http://freewebgame360.blogspot.com/oauth2callback')
    storage = Storage('credentials.dat')
    credentials = storage.get()

    if  not credentials or credentials.invalid:
        auth_uri = flow.step1_get_authorize_url()
        # webbrowser.open(auth_uri)
        # auth_code = raw_input('Enter the auth code: ')
        credentials = flow.step2_exchange('4/UuEtUZaS0WXcZd9mkPUJg3b1VkA7GzECgdUzm7YP3II')
        storage.put(credentials)
        # credentials = run_flow(flow, storage)
    return credentials

def get_service():
    """Returns an authorised blogger api service."""
    credentials = get_credentials()
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('blogger', 'v3', http=http)
    return service

if __name__ == '__main__':
    served = get_service()
    blogs = served.blogs()
    blog_get_obj = blogs.get(blogId='8721173840693810465')
    details = blog_get_obj.execute()
    print(details)


# The results of print will look like:

# {u'description': u'Look far and wide. There are worlds to conquer.',
#  u'id': u'8087466742945672359',
#  u'kind': u'blogger#blog',
#  u'locale': {u'country': u'', u'language': u'en', u'variant': u''},
#  u'name': u'The World Around us',
#  u'pages': {u'selfLink': u'https://www.googleapis.com/blogger/v3/blogs/1234567897894569/pages',
#             u'totalItems': 2},
#  u'posts': {u'selfLink': u'https://www.googleapis.com/blogger/v3/blogs/1245678992359/posts',
#             u'totalItems': 26},
#  u'published': u'2015-11-02T18:47:02+05:30',
#  u'selfLink': u'https://www.googleapis.com/blogger/v3/blogs/9874652945672359',
#  u'updated': u'2017-06-29T19:41:00+05:30',
#  u'url': u'http://www.safarnuma.com/'}