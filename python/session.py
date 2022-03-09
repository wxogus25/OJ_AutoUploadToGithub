import requests
from bs4 import BeautifulSoup as bs
from cookie import *
import urllib3

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

def make_session(url):
    while True:
        running = connect(url)
        if running == False : continue
        break
    return running

def connect(url):
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(all_cookies(url))

    # verify=False ssl 인증서 검증 패스
    soup = bs(session.get(url, verify=False).text, 'html.parser')
    if soup.find('a', {'class': 'username'}) is None:
        print('sad')
        session.close()
        first_load(url + path)
        return False # connect 재실행
    else:
        print('lol')
        return session


if __name__ == '__main__':
    url = 'https://acmicpc.net'
    # ssl 패스 경고메세지 무시
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    make_session(url)
