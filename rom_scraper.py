import requests, os
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from clint.textui import progress

def get_url_paths(url, ext=''):
    response = requests.get(url)

    if response.ok:
            response_text = response.text
            
    else:
            return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    parent = [url + str(node.get('href')) for node in soup.find_all('a') if str(node.get('href')).endswith(ext)]
    return parent
   
def main():
    url = 'https://archive.org/download/efgamecubeusa/Game%20Cube%20USA/'
    ext = '.iso'
    result = get_url_paths(url, ext)
          
    for file in result:
        f_name = file.split('/')[-1]
        req = requests.get(file, stream=True)
        total_length = int(req.headers.get('content-length'))
        with open(f'F:/gc_games/{f_name}', 'wb') as f:
             for chunk in progress.bar(req.iter_content(chunk_size=1024), expected_size=(total_length)+1):
                if chunk:
                  f.write(chunk)
                  f.flush()

main()