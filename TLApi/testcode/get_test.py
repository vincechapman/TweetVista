import requests

url = 'http://192.168.1.11:8000/'
session = requests.session()
r=session.get(url+'common/user_login/')
print (r.text)
