# naver_email_crawler
네이버 블로그 이메일 수집기

# Dependency
```
$ pip install -r requirements.txt
```

# Get Started
```python
>>> from crawler import Crawler
>>> crawler = Crawler()
>>> result = crawler.process()
>>> result
[
    "aaa@naver.com",
    "bbb@naver.com",
    "ccc@naver.com",
    ...
]
```