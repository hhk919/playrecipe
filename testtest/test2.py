# import requests
#
# client_id = "55516dbf091346a4b1c201e04c2f0f5d"
# redirect_uri = 'http://localhost:8000/playlist/callback/'
# scope = 'playlist-read-private playlist-read-collaborative'
# payload = {'client_id': client_id, 'response_type': 'token', 'redirect_uri': redirect_uri,
#                    'scope': scope}
# r = requests.get('https://accounts.spotify.com/authorize',params=payload)
# for resp in r.history :
#     print(resp.url)

from datetime import datetime
from time import sleep

n1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
sleep(1)
n2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
print(n1, type(n1))
n3 = datetime.strptime(n1,'%Y-%m-%d %H:%M:%S.%f')
print(n3, type(n3))