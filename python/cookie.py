import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from variables import *

def accept_path(username):
    return f'/status?user_id={username}&result_id=4'

# To Do 새로운 쿠키 받으면 쿠키 세션과 파일의 쿠키 업데이트하기
# def cookie_update(CookieJar):


def first_load(url):
    options = webdriver.ChromeOptions();
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(60)

    # To Do 나중에 속도 개선하기
    WebDriverWait(driver, timeout=60).until(EC.title_is('Baekjoon Online Judge'))

    cookies = driver.get_cookies()

    # To Do 여러명의 유저를 받기위해 리스트로 변경하기
    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']

    with open("boj_cookie.txt", 'w') as f:
        json.dump(cookies_dict, f, indent=4)

    driver.quit()
    return cookies_dict


def boj_cookie(url):
    try:
        with open('boj_cookie.txt', 'r') as f:
            return json.loads(f.read())
    except:
        return first_load(url + login_path)


if __name__ == '__main__':
    result = boj_cookie(boj_url)
    print(f'{result} 쿠키 추출 완료')