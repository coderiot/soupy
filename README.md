# Soupy
*soupy* - Python Bindings for soup.io

## Requirements

 - [requests](http://docs.python-requests.org/en/latest/)
 - [lxml](http://lxml.de/)
 - cssselect

## Installation
```sh
$ pip install -e git+https://github.com/coderiot/soupy.git#egg=soupy
```

## Usage

### blog methods
#### list recent posts
```python
>>> b = soupy.SoupBlog('http://cats.soup.io')
>>> b.recent_posts()
```

Result:

```python
[{'body': None,
  'date': datetime.datetime(2013, 8, 17, 22, 43, 7),
  'post_id': 205499522,
  'link': 'http://cats.soup.io/post/205499522',
  'source': None,
  'tags': [],
  'title': '[seksgrupowy] (Bild)',
  'type': u'image'},
  ...
]
```

#### list friends of blog
```python
>>> soupy.blog.friends('http://cats.soup.io')
```
Result:

```python
['http://pralina.soup.io',
'http://noirpoulet.soup.io',
'http://MyDarknessPony.soup.io',
'http://SzulcArt.soup.io',
'http://zoozia.soup.io',
'http://longvomiting.soup.io',
'http://beargrylls.soup.io',
'http://Nosoypuntual.soup.io',
'http://ingenuidad.soup.io',
'http://szmaragdowykot.soup.io',
'http://autumnalcrush.soup.io',
'http://KaylaWolfie.soup.io',
'http://straycat.soup.io',
'http://supe.soup.io']
```

#### get blog infos
```python
>>> b = soupy.blog.info('http://cats.soup.io/')
```
Result:

```python
{'description': None,
 'title': "cats's soup",
 'updated': datetime.datetime(2013, 9, 13, 13, 27, 34),
 'url': 'http://cats.soup.io/',
 'username': 'cats'}
```

#### getting avatar of the blog
```python
>>> soupy.blog.avatar('http://cats.soup.io')
```
Result:

```python
{'size': {'height': 59, 'width': 59},
 'url': 'http://f.asset.soup.io/asset/0218/7823_abdf.jpeg'}
```

### user methods
#### creating an user object

```python
>>> user_blog = soupy.User(<USERNAME>, <PASSWORD>)
```

#### post link

```python
>>> user_blog.post_video('<LINK TITLE>', '<URL FOR LINK>')
```
#### post text

```python
>>> user_blog.post_text('<TEXT TITLE>', '<TEXT BODY>')
```
#### post quote (not implented yet)

```python
>>> user_blog.post_quote('<QUOTE>', '<SOURCE>')
```
#### post link to an image

```python
>>> user_blog.post_image('<IMAGE URL>')
```
#### post link to a video

```python
>>> user_blog.post_video('<URL OR EMBED_CODE OF VIDEO>')
```
#### repost stuff from soup.io

```python
>>> user_blog.repost('<SOUP_POST_ID>')
```

### Changelog

**0.1**
 - initial release

**0.2**
 - using python requests instead mechanize
 - create soupy package
 - split soupy.py to soupy.blog, soupy.user, soupy.request
 - changing api in general
 - removing Postiterator
