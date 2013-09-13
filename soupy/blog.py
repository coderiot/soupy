#!/usr/bin/env python
# encoding: utf-8

import datetime
import json
import re

import lxml.etree
import lxml.html

rss = '%s/rss'
friends = '%s/friends'


def friends(blog_url):
    """@todo: Docstring for friends

    :blog: @todo
    :returns: @todo

    """
    doc = lxml.html.parse(friends % blog_url).getroot()
    return [link.get('href') for link in doc.cssselect('li.vcard a')]


def info(blog_url):
    """@todo: Docstring for friends

    :blog: @todo
    :returns: @todo

    """
    doc = lxml.etree.parse(rss % blog_url)
    info = dict()

    # TODO: replace html special chars
    info['title'] = doc.find('/channel/title').text
    info['url'] = doc.find('/channel/link').text
    info['description'] = doc.find('/channel/description').text

    # extract username from url
    _, name, _, _ = re.split('\.|//', info['url'])
    info['name'] = name

    # get timestamp of last update
    date_str = doc.find('/channel/item/pubDate').text
    info['updated'] = _parse_date(date_str)

    return info


def avatar(blog_url):
    """@todo: Docstring for avatar

    :blog: @todo
    :returns: @todo

    """
    doc = lxml.etree.parse(rss % blog_url)

    avatar = dict()
    avatar['url'] = doc.find('/channel/image/url').text

    size = dict()
    size['width'] = int(doc.find('/channel/image/width').text)
    size['height'] = int(doc.find('/channel/image/height').text)
    avatar['size'] = size

    return avatar


def recent_posts(blog_url):
    """@todo: Docstring for recent_posts

    :blog: @todo
    :returns: @todo

    """
    doc = lxml.etree.parse(rss % blog_url)

    posts = list()
    for item in doc.findall('/channel/item'):
        post = dict()
        post['title'] = item.find('title').text
        post['link'] = item.find('link').text

        _, post_id = item.find('guid').text.rsplit(':', 1)
        post['post_id'] = int(post_id)

        pubDate = item.find('pubDate').text
        post['date'] = _parse_date(pubDate)

        attrs = item.find('soup:attributes',
                          namespaces={'soup': 'http://www.soup.io/rss'})
        attrs = json.loads(attrs.text)

        post['tags'] = attrs['tags']
        post['source'] = attrs['source']
        post['body'] = attrs['body']
        post['type'] = attrs['type']
        posts.append(post)

    return posts


# TODO
def followers(blog_url):
    """Returns a list of the followers of a blog
    with name url and recent post"""
    raise NotImplementedError('not implemented yet.')


def _parse_date(date_str):
    """Convert the soup.io published Date to python datetime object.

    :date_str: string of date in soup.io format.
    :returns: python datetime object.

    """
    dt = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
    return dt
