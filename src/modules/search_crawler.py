'''
네이버 블로그 이메일 수집 모듈 (검색 탭)
'''
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from chrome_driver import get_driver


class SearchCrawler:
    '''crawler Class'''
    def __init__(
        self, 
        keyword, 
        min_idx, 
        max_idx, 
        order,
        driver_version,
        output,
    ):
        self.keyword = keyword
        self.min_idx = min_idx
        self.max_idx = max_idx
        self.order = order
        self.driver_version = driver_version
        self.output = output
        self.url = "https://section.blog.naver.com/Search/Post.nhn?pageNo=%s&rangeType=ALL&orderBy=%s&keyword=%s"

    def process(self):
        email_list = []
        for idx in tqdm(list(range(self.min_idx, self.max_idx + 1))):
            url = self._get_url(idx)
            sub_list = self.get_user_list(url)
            email_list.extend(sub_list)
        self.export(email_list)
        return email_list

    def _get_url(self, idx):
        '''네이버 블로그 검색 url 포맷 변환'''
        return self.url % (idx, self.order, self.keyword)

    def get_user_list(self, url):
        '''해당 페이지의 각 블로거의 이메일 수집'''
        user_list = []
        for _ in range(5):
            try:
                driver = get_driver(self.driver_version)
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

    def export(self, email_list):
        df = pd.DataFrame(email_list)
        if self.output.endswith('csv'):
            df.to_csv(self.output, index=False)
        elif self.output.endswith('xlsx'):
            df.to_excel(self.output, index=False)
