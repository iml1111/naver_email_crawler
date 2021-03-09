'''
네이버 블로그 이메일 수집 모듈 (카테고리 탭)
'''
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from chrome_driver import get_driver
from modules.category_list import category_list


class CategoryCrawler:
    '''Crawler Class'''
    def __init__(self, min_idx, max_idx, driver_version, output):
        self.min_idx = min_idx
        self.max_idx = max_idx
        self.driver_version = driver_version
        self.output = output
        self.url = "https://section.blog.naver.com/ThemePost.nhn?\
                    activeDirectorySeq=%s&directoryNo=%s&currentPage=%s"
        self.category_list = category_list

    def process(self):
        '''All Process'''
        email_list = []
        for dir_num, category in tqdm(self.category_list):
            for idx in range(self.min_idx, self.max_idx + 1):
                sub_list = self.get_user_list(dir_num, idx, category)
                email_list.extend(sub_list)
        self.export(email_list)
        return email_list

    def _get_url(self, dir_num, currentPage):
        '''네이버 블로그 카테고리 url 포맷 변환'''
        return self.url % (dir_num[0], dir_num[1], currentPage)

    def get_user_list(self, dir_num, idx, category):
        '''해당 페이지의 각 블로거의 이메일 수집'''
        user_list = []
        for _ in range(10):
            try:
                driver = get_driver(self.driver_version)
                driver.get(self._get_url(dir_num, idx))
                time.sleep(3)
                soup = bs(driver.page_source, "html.parser")
                break
            except:
                print("Page 접근 실패...")
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
                    "category": category,
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
