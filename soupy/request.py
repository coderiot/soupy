#!/usr/bin/env python
# encoding: utf-8

import requests

import lxml.html

urls = {
        "base": "http://%s.soup.io",
        "login": "https://www.soup.io/login",
        "logout": "http://www.soup.io/logout",
        "bookmarklet": "http://www.soup.io/bookmarklet/",
        "save": "http://www.soup.io/bookmarklet/save",
        "repost": "http://www.soup.io/remote/repost"
}


class SoupRequest(object):
    """Docstring for SoupRequest """

    def __init__(self, username, password):
        """@todo: to be defined1 """
        self.username = username
        self.blog_url = urls['base'] % username
        self.session = requests.Session()
        self.auth = self.auth(username, password)
        self.token, self.blog_id = self.get_token_and_id(username)

    def auth(self, username, password):
        """@todo: Docstring for _login

        :username: @todo
        :password: @todo
        :returns: @todo

        """
        r = self.session.get(urls['login'], verify=True)

        doc = lxml.html.fromstring(r.text)

        auth_elem = doc.cssselect('form.login input.auth')[0]
        auth = auth_elem.attrib['value']

        token_selector = 'form.login input[name="authenticity_token"]'
        token_elem = doc.cssselect(token_selector)[0]
        token = token_elem.attrib['value']

        creds = {'login': username,
                 'password': password,
                 'auth': auth,
                 'authenticity_token': token}

        l = self.session.post(urls['login'], data=creds, verify=True)

        if not l.ok:
            l.raise_for_status()

        return auth

    def logout(self):
        """@todo: Docstring for _logout

        :returns: @todo

        """
        self.session.get(urls['logout'])
        del self.session.cookies['soup_user_id']

    def get_token_and_id(self, username):
        data = {'v': 5,
                's': 'a',
                'u': urls['base'] % username,
                't': username}
        r = self.session.post(urls['bookmarklet'], data=data)

        if not r.ok:
            r.raise_for_status()

        doc = lxml.html.fromstring(r.content)

        token_elem = doc.cssselect('meta[name="csrf-token"]')[0]
        token = token_elem.attrib['content']

        blog_id_elem = doc.cssselect('input[name="post[blog_id]"]')[0]
        blog_id = blog_id_elem.attrib['value']

        return token, blog_id

    def post(self, post_data):
        """@todo: Docstring for _post

        :post_data: @todo
        :returns: @todo

        """
        data = {}
        data['authenticity_token'] = self.token
        data['post[blog_id]'] = self.blog_id
        data.update(post_data)

        post = self.session.post(urls['save'], data=data)

        if not post.ok:
            post.raise_for_status()

    def repost(self, post_id):
        """@todo: Docstring for repost

        :post_id: @todo
        :returns: @todo

        """
        data = {}
        data['auth'] = self.auth
        data['parent_id'] = post_id

        rp = self.session.post(urls['repost'],
                               data=data,
                               headers={'X-CSRF-Token': self.token})

        if not rp.ok:
            rp.raise_for_status()
