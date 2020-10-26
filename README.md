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
# max_idx: 최대 탐색 페이지 인덱스
>>> result = crawler.process(max_idx=5)
>>> result
[
    "aaa@naver.com",
    "bbb@naver.com",
    "ccc@naver.com",
    ...
]
```
