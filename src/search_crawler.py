'''
네이버 블로그 이메일 수집 모듈 (검색 탭)
'''
import time
import csv
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from chrome_driver import get_driver


class SearchCrawler:
    '''crawler Class'''
    def __init__(self):
        self.url = "https://section.blog.naver.com/Search/Post.nhn?pageNo=%s&rangeType=ALL&orderBy=%s&keyword=%s"

    def process(self, keyword, min_idx=1, max_idx=571, order_by="sim"):
        email_list = []
        for idx in tqdm(list(range(min_idx, max_idx + 1))[:]):
            url = self._get_url(keyword, idx, order_by)
            sub_list = self.get_user_list(url)
            email_list.extend(sub_list)
        return email_list

    def _get_url(self, keyword, idx, order_by):
        '''네이버 블로그 검색 url 포맷 변환'''
        return self.url % (idx, order_by, keyword)

    def get_user_list(self, url):
        '''해당 페이지의 각 블로거의 이메일 수집'''
        user_list = []
        for _ in range(5):
            try:
                driver = get_driver()
                driver.get(url)
                time.sleep(3)
                soup = bs(driver.page_source, "html.parser")
                break
            except:
                print("page 접근 실패...")
        a_tags = soup.select("a.author")

        for a_tag in a_tags:
            # 유저 이메일
            ng_href = a_tag['ng-href']
            naver_id = ng_href.split("/")[-1]
            email = naver_id + "@naver.com"
            # 유저 닉네임
            em_tag = a_tag.select_one("em.name_author")
            name = em_tag.get_text().strip()

            user_list.append(
                {
                    "email": email,
                    "name": name
                }
            )
        driver.close()
        return user_list

    def export_csv(self, user_list):
        f = open("email.csv", 'w', newline='')
        wr = csv.writer(f)
        email_set = set()
        for user in user_list:
            if user['email'] not in email_set:
                wr.writerow([user['name'], user['email']])
                email_set.add(user['email'])
        f.close()


if __name__ == '__main__':
    crawler = SearchCrawler()
    result = []
    result.extend(crawler.process(keyword="운동", max_idx=573))
    result.extend(crawler.process(keyword="건강", max_idx=573))
    result.extend(crawler.process(keyword="라이프스타일", max_idx=573))
    result.extend(crawler.process(keyword="음료", max_idx=573))
    result.extend(crawler.process(keyword="요리", max_idx=573))
    result.extend(crawler.process(keyword="미술", max_idx=573))
    result.extend(crawler.process(keyword="커리어", max_idx=573))
    result.extend(crawler.process(keyword="공예", max_idx=573))
    result.extend(crawler.process(keyword="사진", max_idx=573))
    result.extend(crawler.process(keyword="영상", max_idx=573))
    result.extend(crawler.process(keyword="음악", max_idx=573))
    crawler.export_csv(result)