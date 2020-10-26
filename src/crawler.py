'''
네이버 블로그 이메일 수집 모듈
'''
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from chrome_driver import get_driver


class Crawler:
    '''Crawler Class'''
    def __init__(self):
        self.url = "https://section.blog.naver.com/ThemePost.nhn?\
                    activeDirectorySeq=%s&directoryNo=%s&currentPage=%s"
        self.category_list = [
            # 엔터테인먼트, 예술
            (1, 5),
            (1, 6),
            (1, 7),
            (1, 8),
            (1, 9),
            (1, 10),
            (1, 11),
            (1, 12),
            (1, 13),
            
            # 생활, 노하우, 쇼핑
            (2, 14),
            (2, 15),
            (2, 16),
            (2, 17),
            (2, 18),
            (2, 19),
            (2, 20),
            (2, 21),
            (2, 36),
            
            # 취미, 여가, 여행
            (3, 22),
            (3, 23),
            (3, 24),
            (3, 25),
            (3, 26),
            (3, 27),
            (3, 28),
            (3, 29),

            # 지식, 동향
            (4, 30),
            (4, 31),
            (4, 32),
            (4, 33),
            (4, 34),
            (4, 35),
        ]

    def process(self, max_idx=5):
        '''All Process'''
        email_list = []
        for category in tqdm(self.category_list):
            for idx in range(1, max_idx + 1):
                sub_list = self.get_email_list(category, idx)
                email_list.extend(sub_list)
        return list(set(email_list))

    def _get_url(self, dir_num, currentPage):
        '''네이버 블로그 카테고리 url 포맷 변환'''
        return self.url % (dir_num[0], dir_num[1], currentPage)

    def get_email_list(self, dir_num, idx):
        '''해당 페이지의 각 블로거의 이메일 수집'''
        email_list = []
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
            ng_href = a_tag['ng-href']
            naver_id = ng_href.split("/")[-1]
            email_list.append(naver_id + "@naver.com")

        driver.close()
        return email_list


if __name__ == '__main__':
    crawler = Crawler()
    result = crawler.process()