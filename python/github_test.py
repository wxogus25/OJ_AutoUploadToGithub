# import requests
# from bs4 import BeautifulSoup as bs
# from variables import *
# import hashlib
# import base64

# # https://storycompiler.tistory.com/7 : 깃 설명
# # https://www.thepythoncode.com/article/using-github-api-in-python : 깃 조작
# # https://gist.github.com/MartinHeinz/739b24f0b94dfb4a0dbea53efa61e04e#file-update_file_in_repo-py : 예시 2

# header = {'Accept': 'application/vnd.github.v3+json', 'Authorization': ''}
# session = requests.Session()
# session.headers.update(header)

# receive = session.get(git_url + '/repos/wxogus25/BOJ/branches/main')
# print(receive.json()['commit']['sha'])

# text = base64.b64encode('test'.encode('ascii')).decode('ascii')
# data = {"content": text, "encoding": "base64"}
# receive = session.post(git_url + '/repos/wxogus25/BOJ/git/blobs', data=data, headers=header)
# base64_blob_sha = receive.json()
# print(data)
# print(base64_blob_sha)
# print(receive.status_code)


# # sha = hashlib.new('sha1')
# # text = ''
# # with open('testfile.txt','r') as f:
# #     text = f.read()

# # text = base64.b64encode('test'.encode('ascii'))
# # sha.update(text)
# # message = 'test push'

# # data = {'content': text, 'message': message}
# # print(data)

# # # receive = session.get(git_url + '/repos/wxogus25/BOJ/contents/testfile.txt')
# # receive = session.post(git_url + '/repos/wxogus25/BOJ/contents/testfile.txt', data = data)
# # print(receive.status_code)
# # soup = bs(receive.text, 'html.parser')


# # print(soup)

from github import *
token = ''
try:
    with open('token.txt', 'r') as f:
        token = f.read()
except:
    pass

git = Github(token)
print(token)
repo = git.get_repo(f'{git.get_user().login}/BOJ')
content = repo.get_contents('')
for file in content:
    repo.delete_file(file.path, "remove", file.sha)
# try:
#     content = repo.get_contents("test.txt")
# except:
#     content = repo.create_file("test.txt", "make test.txt", "test")

# print(content.name)
