from session import *
# from boj import *
from github import *
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

connect_session, username = make_session(boj_url)
receive = connect_session.get(boj_url + user_path + username, verify=False)
soup = bs(receive.text, 'html.parser')

accept_count = int(soup.select_one('#u-result-4').text)

receive = connect_session.get(boj_url + accept_path(username), verify=False)
soup = bs(receive.text, 'html.parser').select('#status-table > tbody > tr')
for tr in soup:
    temp = tr.select('td')[6].select_one('a').get('href').replace("/source","/source/download")
    receive = connect_session.get(boj_url + temp, verify=False)
    print(receive.text)
    break;
    
# print(soup)