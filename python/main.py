from session import *
from github import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

connect_session = make_session(boj_url)

# 메인 페이지에서 username 가져오기
mainpage = connect_session.get(boj_url, verify=False)
soup = bs(mainpage.text, 'html.parser')
username = soup.find('a', {'class': 'username'})

# 유저_페이지 get
userpage = connect_session.get(boj_url + user_path + username, verify=False)
soup = bs(userpage.text, 'html.parser')

# 맞았습니다 개수 저장
accept_count = int(soup.select_one('#u-result-4').text)

# 맞았습니다_페이지 get
acpage = connect_session.get(boj_url + accept_path(username), verify=False)
# 상태가 '맞았습니다'인 문제들만 보기
soup = bs(acpage.text, 'html.parser').select('#status-table > tbody > tr')
pre_count = 0

# 마지막으로 본 counter 읽기
try:
    with open('accept_counter.txt', 'r') as f:
        pre_count = int(f.read())
except:
    pass

for tr in soup:
    if pre_count == accept_count:
        break

    temp = tr.select('td')[3].select_one('img').get('src')
    tier = boj_tier[int(temp[temp.find('temp/')+5:temp.find('.svg')])]

    problem_number = 


    # 선택한 문제의 code download 링크
    downlink = tr.select('td')[6].select_one('a').get('href').replace("/source","/source/download")
    # 문제의 code get
    code = connect_session.get(boj_url + downlink, verify=False)
    break;

