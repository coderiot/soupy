#!/usr/bin/env python
# encoding: utf-8

import request


class User(object):
    """Docstring for Client """

    def __init__(self, username, password):
        """@todo: to be defined1 """
        self.username = username
        self.blog_url = "http://%s.soup.io" % self.username
        self.request = request.SoupRequest(username, password)

    def post_link(self, title, link, tags=[]):
        """@todo: Docstring for post

        :title: @todo
        :body: @todo
        :returns: @todo

        """
        data = {}
        data['post[tags]'] = ",".join(tags)
        data['post[source]'] = link
        data['post[title]'] = title
        data['post[type]'] = 'link'

        self.request.post(data)

    def post_text(self, title, body, tags=[]):
        """@todo: Docstring for post

        :title: @todo
        :body: @todo
        :returns: @todo

        """
        data = {}
        data['post[tags]'] = ",".join(tags)
        data['post[title]'] = title
        data['post[body]'] = body
        data['post[type]'] = 'regular'

        self.request.post(data)

    def post_image(self, url, source="", description="", tags=[]):
        data = {}
        data['post[tags]'] = ",".join(tags)
        data['post[source]'] = source
        data['post[body]'] = description
        data['post[url]'] = url
        data['post[type]'] = 'image'
        self.request.post(data)

    def post_video(self, url, description="", source="", tags=[]):
        data = {}
        data['post[tags]'] = ",".join(tags)
        data['post[source]'] = source
        data['post[embedcode_or_url]'] = url
        data['post[type]'] = 'video'
        data['post[body]'] = description

        self.request.post(data)

    def post_quote(self, title, quote):
        raise NotImplementedError('not implemented yet.')

    def repost(self, post_id):
        """@todo: Docstring for repost

        :post_id: @todo
        :returns: @todo

        """
        self.request.repost(post_id)
