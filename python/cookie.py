import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

path = '/login'

def cookie_update(CookieJar):
    with open("all_cookies.txt", 'rw') as f:
        if json.loads(f.read()) != CookieJar:
            print('server serve new cookies!')
            f.write(json.dumps(CookieJar))
        else:
            print("CookieJar isn't changed")
    return None

def first_load(url):
    options = webdriver.ChromeOptions();
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.implicitly_wait(60)

    WebDriverWait(driver, timeout=60).until(EC.title_is('Baekjoon Online Judge'))

    cookies = driver.get_cookies()

    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']

    with open("all_cookies.txt", 'w') as f:
        f.write(json.dumps(cookies_dict))

    driver.quit()
    return cookies_dict


def all_cookies(url):
    try:
        with open('all_cookies.txt', 'r') as f:
            return json.loads(f.read())
    except:
        return first_load(url + path)


if __name__ == '__main__':
    url = 'https://acmicpc.net/login'
    result = all_cookies(url)
    print(f'{result} 쿠키 추출 완료')