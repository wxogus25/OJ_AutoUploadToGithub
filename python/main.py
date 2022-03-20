from session import *
from github import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

list = []


def traversal(session, page, acc_counter, pre_counter):
    index = 0
    soup = bs(page.text, 'html.parser').select('#status-table > tbody > tr')
    for tr in soup:
        if pre_counter == acc_counter:
            break
        temp = tr.select('td')[2].select_one('img').get('src')
        tier = boj_tier[int(temp[temp.find('tier/')+5:temp.find('.svg')])]

        problem_number = tr.select('td')[2].select_one('a').text

        problem_name = tr.select('td')[2].select_one('a').get('title')

        # 선택한 문제의 code download 링크
        downlink = tr.select('td')[6].select_one('a').get(
            'href').replace("/source", "/source/download")

        ext = tr.select('td')[6].select_one('a').get_text()

        submitDate = tr.select('td')[8].select_one('a').get('title')
        # 문제의 code get
        # code = session.get(boj_url + downlink, verify=False)

        # print('{:14} {:7}{}'.format(
        #     f'[{tier}]', problem_number, problem_name), file=file)
        list.append({'pnumber': problem_number, 'pname': problem_name,
                    'tier': tier, 'downlink': downlink, 'ext': languages[ext], 'date': submitDate})
        pre_counter += 1
        index += 1

    if index == 20 and pre_counter != acc_counter:
        print(f'{pre_counter} / {acc_counter}')
        next_page_url = bs(page.text, 'html.parser').select_one(
            '#next_page').get('href')
        acpage = session.get(boj_url + next_page_url, verify=False)
        traversal(session, acpage, acc_counter, pre_counter)

    return None


connect_session = make_session(boj_url)

# 메인 페이지에서 username 가져오기
mainpage = connect_session.get(boj_url, verify=False)
soup = bs(mainpage.text, 'html.parser')
username = soup.find('a', {'class': 'username'}).text

# 유저_페이지 get
userpage = connect_session.get(boj_url + user_path + username, verify=False)
soup = bs(userpage.text, 'html.parser')

# 맞았습니다 개수 저장
accept_count = int(soup.select_one('#u-result-4').text)

# 맞았습니다_페이지 get
acpage = connect_session.get(boj_url + accept_path(username), verify=False)

# 마지막으로 본 counter 읽기
pre_count = 0
try:
    with open('accept_counter.txt', 'r') as f:
        pre_count = int(f.read())
except:
    pass

traversal(connect_session, acpage, accept_count, pre_count)

with open('accept_counter.txt', 'w') as f:
    f.write(str(accept_count))

print('git upload init')
list.reverse()
token = ''
try:
    with open('token.txt', 'r') as f:
        token = f.read()
except:
    print('token.txt에 토큰이 없습니다!!')
    exit(0)

git = Github(token)
repo = git.get_repo(f'{git.get_user().login}/BOJ')
content = ''
print('git upload start')
# https://code-examples.net/ko/q/24ce89d git 업로드 속도 개선
for prob in list:
    code = connect_session.get(boj_url + prob['downlink'], verify=False).text
    dirnum = int(prob['pnumber'])//1000
    dir = '{:<5}~{:>5}'.format(dirnum*1000, (dirnum+1)*1000-1)
    # print(code)
    try:
        content = repo.get_contents(f'{dir}/{prob["pnumber"]}.{prob["ext"]}')
        repo.update_file(content.path, '{:14} {:7}{}'.format(
            f'[{prob["tier"]}]', prob['pnumber'], prob['pname']), f"// {prob['date']}\n" + code, content.sha)
    except:
        content = repo.create_file(f'{dir}/{prob["pnumber"]}.{prob["ext"]}', '{:14} {:7}{}'.format(
            f'[{prob["tier"]}]', prob['pnumber'], prob['pname']), f"// {prob['date']}\n" + code)

    print('{:14} {:7}{}'.format(
        f'[{prob["tier"]}]', prob['pnumber'], prob['pname']))
