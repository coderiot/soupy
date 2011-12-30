# -*- coding: utf-8 -*-

from datetime import datetime

from lxml import etree
from lxml import html

from json import loads

import mechanize


class SoupError(Exception):
    ''' General Soup error ''' 
    def __init__(self, msg):
        self.msg = msg 

    def __str__(self):
        return self.msg 


class SoupAuthError(SoupError):
    ''' Wraps a 403 result '''
    pass


class SoupRequestError(SoupError):
    ''' Wraps a 400 result '''
    pass

LOGIN_URL = 'https://www.soup.io/login'
BLOG_URL = 'http://%s.soup.io/'
POST_URL = 'http://%s.soup.io/save'
REPOST_URL = 'http://www.soup.io/remote/repost'
TOOGLE_URL = 'http://www.soup.io/remote/toggle/frame' 


"""

    Docstring for Soup
    
"""
#TODO: Soup ist kein Account Objekt, ermöglicht aber das Einloggen über login
#TODO: catch exception 
#TODO: es muss möglich sein einen Blog komplett durchzulaufen, um alle Eintrage anzusehen
#TODO: mann muss seine eigene friends bekommen können und es möglich sein die dazugehörige timeline 
#      zu durchlaufen
class SoupAccount(object):
    """docstring for SoupAccount"""
    def __init__(self, login_name, password):
        self.login_name = login_name
        self.password = password
        self.blog_url = BLOG_URL % login_name
        self.post_url = POST_URL % login_name
        self.browser = mechanize.Browser(factory=mechanize.RobustFactory())
        
        #br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        self._authenticate = False
        # Browser options
        self.browser.set_handle_robots(False)
        # Log HTTP response bodies (ie. the HTML, most of the time).
        self.browser.set_debug_responses(False)
        # Log information about HTTP redirects and Refreshes.
        self.browser.set_debug_redirects(False)
        # Want debugging messages?
        self.browser.set_debug_http(False)

    def login(self):
        """docstring"""
        # open login page
        self.browser.open(LOGIN_URL)

        # select login form and set fields 
        self.browser.select_form(nr=0)
        self.browser.form['login'] = self.login_name
        self.browser.form['password'] = self.password

        # submit login form
        r = self.browser.submit()
        # check if login was successful
        self._check_auth(r.read())
        # go to blog frontpage after to update subdomain cookies :(
        self.browser.open(self.blog_url)

    def _check_auth(self, login_resp):
        doc = html.fromstring(login_resp)
        if doc.find_class('error'):
            self._authenticate = False
        else:
            self._authenticate = True

    def is_auth(self):
        return self._authenticate

    def logout(self):
        self.browser.open('http://www.soup.io/logout')
        self._authenticate = False

    def _create_default_request(self):
        """docstring for _create_default_request"""
        assert self._authenticate == True
        # Create an empty HTML Form. Mind the enctype!
        form = mechanize.HTMLForm(self.post_url, method='POST', enctype='multipart/form-data')

        # Put simple input types in the form. 
        form.new_control('text', 'post[title]', {'value': ''})
        form.new_control('text', 'post[body]', {'value': ''})
        form.new_control('text', 'post[tags]', {'value': ''})
        form.new_control('text', 'commit', {'value': 'Save'})
        form.new_control('text', 'post[id]', {'value': ''})
        form.new_control('text', 'post[type]', {'value': ''})
        form.new_control('text', 'post[source]', {'value': ''})
        form.new_control('text', 'post[parent_id]', {'value': ''})
        form.new_control('text', 'post[original_id]', {'value': ''})
        form.new_control('text', 'post[edited_after_repost]', {'value': ''})
        form.new_control('text', 'post[url]', {'value': ''})
        form.new_control('text', 'post[embedcode_or_url]', {'value': ''})

        return form

    def _submit(self, request):
        """docstring for _submit"""
        # Call this at the end of the creation phase.
        request.fixup()

        self.browser.form = request
        self.browser.submit()

    def post_text(self, text,  title=''):
        request = self._create_default_request()
        request['post[type]'] = "PostRegular"

        request['post[title]'] = title
        request['post[body]'] = text

        self._submit(request)

    def post_link(self, url, title = '', description = ''):
        """docstring for post_link"""
        request = self._create_default_request()
        request['post[type]'] = "PostLink"

        request['post[source]'] = url
        request['post[title]'] = title
        request['post[body]'] = description
        
        self._submit(request)

    def post_image(self, url, description=''):
        """docstring for post_image"""
        request = self._create_default_request()
        request['post[type]'] = "PostImage"

        request['post[url]'] = url
        request['post[source]'] = url
        request['post[body]'] = description
        
        self._submit(request)

    def post_quote(self, quote, source):
        """docstring for post_quote"""
        request = self._create_default_request()
        request['post[type]'] = "PostQuote"

        request['post[body]'] = quote
        request['post[title]'] = source
        
        self._submit(request)

    def post_video(self, video_link, description):
        """docstring for post_video"""
        request = self._create_default_request()
        request['post[type]'] = "PostVideo"

        request['post[embedcode_or_url]'] = video_link
        request['post[body]'] = description
        
        self._submit(request)

    def post_file(self):
        """docstring for post_file"""
        pass

    def post_review(self):
        """docstring for post_review"""
        pass

    def post_event(self):
        """docstring for post_event"""
        pass

    def _get_repost_auth(self, url):
        r =self.browser.open(url)
        self.browser.select_form(nr=0)
        return self.browser.form['auth']

    def repost(self, source_url, post_id):
        # open source
        self.browser.open(source_url)

        # find url with auth code
        toogle_url = self.browser.find_link(url_regex=TOOGLE_URL).url
        auth = self._get_repost_auth(toogle_url)
        form = mechanize.HTMLForm(REPOST_URL, method='POST', enctype='application/x-www-form-urlencoded')

        # Put simple input types in the form. 
        form.new_control('text', 'auth', {'value': auth})
        form.new_control('text', 'parent_id', {'value': post_id})

        form.fixup()

        self.browser.form = form
        self.browser.submit()


RSS_SUFFIX = '/rss'
FRIENDS_SUFFIX = '/friends'

"""

    Docstring for Blog
    
"""
#TODO entweder Blog und Group in verschiedenen Klassen und versuchen zu mergen
#       muss auf jeden Fall unterschieden werden
class SoupBlog(object):
    def __init__(self, url):
        self.url = url

    def post_iterator(self):
        """docstring for post_iterator"""
        return SoupIterator(self.url)

    def get_friends(self):
        """docstring for get_friends"""            
        doc = html.parse(self.url + FRIENDS_SUFFIX).getroot()
        return [link.get('href') for link in doc.cssselect('li.vcard a')]

    def info(self):
        """docstring for info"""
        doc = etree.parse(self.url + RSS_SUFFIX)
        info = dict()
        info['title'] = doc.xpath('/rss/channel/title')[0].text
        info['url'] = doc.xpath('//channel/link')[0].text
        info['description'] = doc.xpath('//description')[0].text
        
        # extract username from url 
        info['username'] = info['url'].replace('http://', '').split('.', 1)[0]
        # get timestamp of last update
        date_str = doc.xpath('/rss/channel/item/pubDate')[0].text
        info['updated'] = pubDate2unixtime(date_str)

        return info

    def avatar(self):
        """Return the URL of an avatar"""
        doc = etree.parse(self.url + RSS_SUFFIX)
        avatar = dict()
        avatar['url'] = doc.xpath('//image/url')[0].text
        size = dict()
        size['width'] = int(doc.xpath('//image/width')[0].text)
        size['height'] = int(doc.xpath('//image/height')[0].text)
        avatar['size'] = size

        return avatar

    #TODO repost_info dictionary entry with is_repost, from and via keys
    def recent_posts(self):
        """Return the ~40 of the recent posts from the blog."""
        doc = etree.parse(self.url + RSS_SUFFIX)
 
        posts = list()
        for item in doc.xpath('/rss/channel/item'):
            post = dict()
            post['title'] = item.xpath('title')[0].text
            link = item.xpath('link')[0].text
            # remove title in url 
            post['link'] = link.rsplit('/', 1)[0]
            post['guid'] = item.xpath('guid')[0].text
            pubDate =  item.xpath('pubDate')[0].text
            post['date'] = pubDate2unixtime(pubDate)
            attrs =  item.xpath('soup:attributes', namespaces={'soup': 'http://www.soup.io/rss'})[0].text
            attrs = loads(attrs)

            post['tags'] = attrs['tags']
            post['source'] = attrs['source']
            post['body'] = attrs['body']
            post['type'] =attrs['type']
            posts.append(post)

        return posts

    # TODO
    def stalkers(self):
        """Returns a list of the followers of a blog 
        with name url and recent post"""
        pass


"""

    Docstring for SoupIterator
    
"""
class SoupIterator(object):
    """docstring for SoupIterator"""
    def __init__(self, url):
        # remove trailing '/'
        self.url = url.rstrip('/')
        self.browser = mechanize.Browser(factory=mechanize.RobustFactory())
        
        self.browser.set_handle_robots(False)
        self.has_more = True
        self.next_page = self.url

    def __iter__(self):
        """docstring for __iter__"""
        return self

    #TODO nur durch ein post typ iterieren
    def next(self):
        """docstring for next"""
        if self.has_more:
            return self.get_posts(self.next_page)
        else:
            raise StopIteration

    def get_posts(self, url):
        """docstring for iter"""
        self.browser.open(url)

        r = self.browser.open(url)
        doc = html.fromstring(r.read())
        
        posts = list() 
        for c in doc.cssselect('div.content-container'):
            posts.append(self._get_post_details(c))

        try:
            more = self.browser.find_link(text='more posts')
            self.next_page =  more.absolute_url
        except Exception, e:
            self.has_more = False

        return posts

    #TODO last page is empty :(
    #TODO use iterparse
    def _get_post_details(self, c):
        parent = c.getparent()
        post = dict()
        # get permalink to post
        link = c.cssselect("li.'first permalink' a")[0].get("href")
        #remove title from link
        #post['link'] = link.rsplit('/', 1)[0]

        # get post type 
        post['type'] = self._get_post_type(parent.get('class'))

        #TODO get tags
        post['tags'] = []

        #TODO format of content
        post['format'] = 'some'

        #TODO get reactions
        post['reaction'] = []

        # image specific attributes
        if post['type'] == 'image':
            img = c.cssselect('div.imagecontainer img')[0]
            post['size'] = dict({'height': img.get('height'), 'width': img.get('width')})

            caption = c.cssselect('div.caption a')
            if caption:
                post['caption'] = caption[0].get('href')

        # video specific attributes
        if post['type'] == 'video':
            video_src = c.cssselect('div.embed iframe')
            if video_src:
                post['video_src'] = video_src[0].get('src')
            
            video_src_alt = c.xpath('//embed')
            if video_src_alt:
                post['video_src'] = video_src_alt[0].get('src')

            body = c.cssselect('div.body')
            if body:
                post['body'] = body[0].text_content()

        # text specific attributes
        if post['type'] == 'text':
            post['body'] = c.cssselect('div.body')[0].text_content()

        # quote specific attributes
        if post['type'] == 'quote':
            cite_src = c.xpath('//cite/a')

            if cite_src:
                post['cite'] = cite_src[0].get('href')
            else:
                post['cite'] = c.xpath('//cite')[0].text

            post['body'] = c.cssselect('span.body')[0].text_content()

        #get reposters
        post['reposters'] = [l.get('href') for l in c.cssselect("div.'source reposted_by' a")]

        source = [s.get('href') for s in c.cssselect("div.source a.'url avatarlink'")]

        post['reposted'] = dict(zip(['from', 'via'], source))

        meta =  parent.cssselect("span.'time' abbr")
        if meta:
            post['published'] = meta[0].get('title')

        return post

    # TODO ugly
    def _get_post_type(self, type_string):
        """docstring for _get_post_type"""
        if 'post_regular' in type_string:
            return 'text'
        elif 'post_image' in type_string:
            return 'image'
        elif 'post_quote' in type_string:
            return 'quote'
        elif 'post_video' in type_string:
            return 'video'
        elif 'post_event' in type_string:
            return 'event'
        elif 'post_review' in type_string:
            return 'review'
        else:
             return 'file'

def pubDate2unixtime(pubDate):
    """Convert the soup.io published Date to unix timestamp """
    dt = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S %Z') 
    return long(dt.strftime('%s'))
