from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from oauth2client.file import Storage
import httplib2
from apiclient.discovery import build
import webbrowser


def get_credentials():
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


def get_service():
    """Returns an authorised blogger api service."""
    credentials = get_credentials()
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('blogger', 'v3', http=http)
    return service


if __name__ == '__main__':
    served = get_service()
    # get blog info
    blogs = served.blogs()
    blog_get_obj = blogs.get(blogId='8721173840693810465')
    details = blog_get_obj.execute()
    print(details)
    # get post list
    posts = served.posts()
    post_get_obj = posts.list(blogId='8721173840693810465')
    details = post_get_obj.execute()
    print(details)
    # body = {
    #     'kind': 'blogger#postList',
    #     'published': '2017-10-13T17:49:00+07:00',
    #     'title': 'Arena of Valor – Garena prepares to launch mobile MOBA in remaining SEA countries',
    #     'content': '<div>\n<img alt="" class="entry-thumb" src="http://mmoculture.com/wp-content/uploads/2017/10/Arena-of-Valor-696x344.jpg" height="344" title="Arena of Valor" width="696" /><br />\n[<a href="https://www.facebook.com/garena.aov/" rel="noop ener" target="_blank">Facebook page</a>] After launching separate servers in Indonesia and Thailand, Garena is finally preparing to launch Arena of Valor (AOV) in the remaining Southeast Asia countries, mainly <str ong="">Singapore</str></div>\n, <strong>Malaysia</strong>, and <strong>the Philippines</strong>, which will share a server. Known as 王者荣耀, the top downloaded and grossing mobile game in China, Arena of Val\nor is facing serious competition in Southeast Asia from the popular (but IP-infringing) Mobile Legends.\n<br />\n<div class="td-all-devices">\n</div>\n',
    #     'labels': ['Arena of Valor', 'mobile', 'News']
    # }
    # add_post = posts.insert(blogId='8721173840693810465', body=body, isDraft=True, fetchImages=True, fetchBody=True)
    # details = add_post.execute()
    # print(details)
