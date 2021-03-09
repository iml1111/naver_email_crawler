# naver_email_crawler
네이버 블로그 이메일 수집기

# Dependency
```
$ pip install -r requirements.txt
```

# Get Started
```bash
$ python crawler.py --help

Usage: crawler.py [OPTIONS]

Options:
  --mode [search|category]  [default: search]
  --min-idx INTEGER         최소 인덱스 페이지  [default: 1]
  --max-idx INTEGER         최대 인덱스 페이지  [required]
  --keyword TEXT            search mode일 경우, 입력되어야 함.  [default: <None>]
  --order [sim]             search mode일 경우, 검색 결과 순서 결정.  [default: sim]
  --driver-version INTEGER  크롬드라이버 버전 입력.  [required]
  --output TEXT             출력할 파일 경로.  [required]
```

## Example
```bash
# Search Mode
$ python crawler.py --mode=search --max-idx=100 --keyword=과학 --driver-version=89 --output ./output.csv

# Category Mode
$ python crawler.py --mode=category --max-idx=100 --driver-version=89 --output ./asd.xlsx
```

## Search Mode
keyword로 검색한 결과에 대하여 지정된 idx만큼까지의 이메일 정보를 수집합니다.

## Category Mode
카테고리별 블로그 목록에서 모든 카테고리별 목록에서 각 idx만큼까지의 이메일 정보를 수집합니다.