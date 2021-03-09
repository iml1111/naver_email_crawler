'''
Selenium Chrome Driver Management Module
'''
from platform import system
from selenium import webdriver

DRIVER_PATH = "./webdriver/chromedriver.%s.%s"
PLATFORM = {
    'Windows':'win',
    'Darwin': 'mac',
    "Linux": 'linux'
}
WAIT_SEC = 5


def get_driver(version):
    '''
    Get Selenium Chrome Webdriver function

    Return
    ---------
    Selenium Chrome Webdriver > Object
    '''
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
                    AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;\
                    q=0.9,imgwebp,*/*;q=0.8"}

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("headless")
    options.add_argument('--log-level=5')
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=" + header['User-Agent'])
    options.add_argument("lang=ko_KR")

    driver = webdriver.Chrome(
        DRIVER_PATH % (PLATFORM[system()], version), 
        chrome_options=options
    )
    driver.implicitly_wait(3)

    return driver