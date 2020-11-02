'''
네이버 블로그 이메일 수집 모듈 (카테고리 탭)
'''
import time
import csv
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from chrome_driver import get_driver
from category_list import category_list


class CategoryCrawler:
    '''Crawler Class'''
    def __init__(self):
        self.url = "https://section.blog.naver.com/ThemePost.nhn?\
                    activeDirectorySeq=%s&directoryNo=%s&currentPage=%s"
        self.category_list = category_list

    def process(self, max_idx=5):
        '''All Process'''
        email_list = []
        for dir_num, category in tqdm(self.category_list):
            for idx in range(1, max_idx + 1):
                sub_list = self.get_user_list(dir_num, idx, category)
                email_list.extend(sub_list)
        return email_list

    def _get_url(self, dir_num, currentPage):
        '''네이버 블로그 카테고리 url 포맷 변환'''
        return self.url % (dir_num[0], dir_num[1], currentPage)

    def get_user_list(self, dir_num, idx, category):
        '''해당 페이지의 각 블로거의 이메일 수집'''
        user_list = []
        for _ in range(10):
            try:
                driver = get_driver()
                driver.get(self._get_url(dir_num, idx))
                time.sleep(3)
                # WebDriverWait(driver, 100).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, "a.author")))
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

    def export_csv(self, user_list):
        f = open("email.csv", 'w', newline='')
        wr = csv.writer(f)
        email_set = set()
        for user in user_list:
            if user['email'] not in email_set:
                wr.writerow([user['name'], user['email'], user['category']])
                email_set.add(user['email'])
        f.close()


if __name__ == '__main__':
    crawler = CategoryCrawler()
    result = crawler.process()
    crawler.export_csv(result)