#!/usr/bin/env python
# encoding: utf-8

import request


class User(object):
    """
    Api for posting stuff on your soup.io blog.
    """

    def __init__(self, username, password):
        """
        Login the user on soup.io.
        """
        self.username = username
        self.blog_url = "http://%s.soup.io" % self.username
        self.request = request.SoupRequest(username, password)

    def post_link(self, title, link, tags=[]):
        """
        Post a link on the blog of the user.

        :title: string, title of the link
        :link: string, url for the link you want to post
        :tags: list of string, tags you use to describe the link
        :returns:

        """
        data = {}
        data['post[tags]'] = ",".join(tags)
        data['post[source]'] = link
        data['post[title]'] = title
        data['post[type]'] = 'link'

        self.request.post(data)

    def post_text(self, title, body, tags=[]):
        """
        Post a text entry on the blog of the user.

        :title: string, title of the text
        :body: string, the document you want to post
        :tags: list of string, tags you use to describe the text
        :returns:

        """
        data = {}
        data['post[tags]'] = ",".join(tags)
        data['post[title]'] = title
        data['post[body]'] = body
        data['post[type]'] = 'regular'

        self.request.post(data)

    def post_image(self, url, source="", description="", tags=[]):
        """
        Post an image on the blog of the user.

        :url: string, url that contains the location of the image
        :source: string, link of the source of the image
        :description: string, description for the image
        :tags: list of string, tags you use to describe the image
        :returns:

        """
        data = {}
        data['post[tags]'] = ",".join(tags)
        data['post[source]'] = source
        data['post[body]'] = description
        data['post[url]'] = url
        data['post[type]'] = 'image'
        self.request.post(data)

    def post_video(self, url_or_embed, description="", source="", tags=[]):
        """
        Post a video link on the blog of the user.

        :url_or_embed: string, url or embed code of the video
        :description: string, description for the video
        :source: string, the source the video is from
        :tags: list of string, tags you use to describe the video
        :returns:

        """
        data = {}
        data['post[tags]'] = ",".join(tags)
        data['post[source]'] = source
        data['post[embedcode_or_url]'] = url_or_embed
        data['post[type]'] = 'video'
        data['post[body]'] = description

        self.request.post(data)

    def post_quote(self, title, quote):
        raise NotImplementedError('not implemented yet.')

    def repost(self, post_id):
        """Repost a post from another blog on you blog.

        :post_id: int/string, the id of the post you want to repost
        :returns:

        """
        self.request.repost(post_id)
