Usage
=====

Post on your soup.io account
-------

### post link to an image

### post text

### post link to an video

### repost stuff from soup.io

read blog posts
--------------

### Recent Posts

### Read all posts

information about a soup.io Blog
--------------

### Friends
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
### get blog infos
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
### user avatar
```python
>>> b = soupy.SoupBlog('http://cats.soup.io')
>>> b.avatar()
```
Result:
```python
{'size': {'height': 59, 'width': 59},
 'url': 'http://f.asset.soup.io/asset/0218/7823_abdf.jpeg'}
```

Changelog
---------

**0.1**
 - initial release
