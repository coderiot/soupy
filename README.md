Soupy
====
*soupy* - Python Bindings for soup.io

Requirements
------------

 - mechanize (http://wwwsearch.sourceforge.net/mechanize/)
 - lxml (http://lxml.de/)


Usage
-----

### Post on your soup.io account

#### login/logout

```python
>>> acc = soupy.SoupAccount(<USERNAME>, <PASSWORD>)
>>> acc.login()
>>> acc.is_auth()
True
>>> acc.logout()
>>> acc.is_auth()
False
```

#### post link

```python
>>> acc = soupy.SoupAccount('<USERNAME>', '<PASSWORD>')
>>> acc.post_link('<LINK>', '<TITLE>', '<DESCRIPTION>')
```
#### post text

```python
>>> acc = soupy.SoupAccount('<USERNAME>', '<PASSWORD>')
>>> acc.post_text('this is the body', 'and the title')
```
#### post quote

```python
>>> acc = soupy.SoupAccount('<USERNAME>', '<PASSWORD>')
>>> acc.post_quote('<QUOTE>', '<SOURCE>')
```
#### post link to an image

```python
>>> acc = soupy.SoupAccount('<USERNAME>', '<PASSWORD>')
>>> acc.post_image('<LINK>', '<DESCRIPTION>')
```
#### post link to a video

```python
>>> acc = soupy.SoupAccount('<USERNAME>', '<PASSWORD>')
>>> acc.post_video('<LINK TO VIDEO>', '<DESCRIPTION>')
```
#### repost stuff from soup.io

```python
>>> acc = soupy.SoupAccount('<USERNAME>', '<PASSWORD>')
>>> acc.repost('<SOUP_SOURCE_URL>', '<SOUP_POST_ID>')
```
### read blog posts

#### Recent Posts

```python
>>> b = soupy.SoupBlog('http://cats.soup.io')
>>> b.recent_posts()
```

Result:

```python
[{'body': None,
  'date': 1325185210L,
  'guid': 'urn:www-soup-io:1:205499522',
  'link': 'http://cats.soup.io/post/205499522',
  'source': None,
  'tags': [],
  'title': '[seksgrupowy] (Bild)',
  'type': u'image'},
  ...
]
```
#### iterate over all blog posts
```python
>>> b = soupy.SoupBlog('http://cats.soup.io')
>>> for p in b.post_iterator():
...     print p
```

Result:

```python
[{'format': 'some',
  'reaction': [],
  'reposted': {'from': 'http://proof.soup.io/post/139187574/Image'},
  'reposters': [],
  'size': {'height': '307', 'width': '500'},
  'tags': [],
  'type': 'image'},
 {'caption': 'http://24.media.tumblr.com/tumblr_lwvu0equXU1r40kt5o1_500.jpg',
  'format': 'some',
  'reaction': [],
  'reposted': {},
  'reposters': ['http://gjktptd.soup.io',
                'http://nothingmore.soup.io',
                'http://lejdimagbet.soup.io',
                'http://toc.soup.io',
                'http://lmn.soup.io',
                'http://straycat.soup.io',
                'http://abl.soup.io',
                'http://my-dirty-litte-secret.soup.io',
                'http://judyta.soup.io',
                'http://beawesome.soup.io',
                'http://flowerose.soup.io',
                 'http://butterfly94.soup.io'],
  'size': {'height': '500', 'width': '500'},
  'tags': [],
  'type': 'image'},
 ...
}
```

### informations about a soup.io Blog

#### Friends
```python
>>> b = soupy.SoupBlog('http://cats.soup.io')
>>> b.get_friends()
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
>>> b = soupy.SoupBlog('http://cats.soup.io/')
>>> b.info()
```
Result:

```python
{'description': None,
 'title': "cats's soup",
 'updated': 1325185210L,
 'url': 'http://cats.soup.io/',
 'username': 'cats'}
```
#### user avatar
```python
>>> b = soupy.SoupBlog('http://cats.soup.io')
>>> b.avatar()
```
Result:

```python
{'size': {'height': 59, 'width': 59},
 'url': 'http://f.asset.soup.io/asset/0218/7823_abdf.jpeg'}
```

### Changelog

**0.1**
 - initial release
