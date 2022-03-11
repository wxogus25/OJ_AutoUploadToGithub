import requests
from bs4 import BeautifulSoup as bs
from cookie import *
import urllib3

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

# 먼저 쿠키를 통해 로그인이 가능한지(세션이 연결돼있는지) 확인하고 아니면 connect(url) 재실행 후 반환
def make_session(url):
    while True:
        running = connect(url)
        if running == False : continue
        break
    return running

# url과 세션 연결, 실패하면 False, 성공하면 연결된 세션 반환
def connect(url):
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(boj_cookie(url))

    # verify=False ssl 인증서 검증 패스
    receive = session.get(url, verify=False)
    # print(receive.cookies)
    # print(receive.headers)
    soup = bs(receive.text, 'html.parser')
    username = soup.find('a', {'class': 'username'})
    if username is None:
        print('sad')
        session.close()
        first_load(url + login_path)
        return False # connect 재실행
    else:
        print('lol')
        # cookie_update(session.cookies.get_dict())
        return session


if __name__ == '__main__':
    # ssl 패스 경고메세지 무시
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session= make_session(boj_url)
    # print(username)
