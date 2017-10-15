from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from oauth2client.file import Storage
import httplib2
from apiclient.discovery import build
import webbrowser
from settings import Settings


class BlogUpdate():

    def __init__(self):
        self.blog_id = Settings.blogID

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

    def get_blog_info(self):
        served = self.get_service()
        blogs = served.blogs()
        blog_get_obj = blogs.get(blogId=self.blog_id)
        details = blog_get_obj.execute()
        return details

    def get_posts(self):
        served = self.get_service()
        posts = served.posts()
        post_get_obj = posts.list(blogId=self.blog_id)
        details = post_get_obj.execute()
        details = details['items']
        return details

    def add_post(self, body):
        served = self.get_service()
        posts = served.posts()
        add_post = posts.insert(blogId=self.blog_id,
                                body=body, isDraft=False, fetchImages=True, fetchBody=True)
        details = add_post.execute()
        return details
