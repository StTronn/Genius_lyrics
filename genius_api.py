import requests,os
import re
from bs4 import BeautifulSoup
from string import punctuation
from urllib.parse import urlencode

class API():
    """Genius API """

    #create a session

    def __init__(self,response_format='plain'):
        self.headers={'Authorization': 'Bearer ' + 'NpBI2c-OW6zs4SCPEK21YrdSg-Yfrkp48IBRXw05CCKoOoptkBSV4ECzJe2tEKg3'}
        self.base_url='https://api.genius.com/'
        self.response_format=response_format.lower()
    
    def make_request(self,path,params=None):
        """make request to the genius api """
        url=self.base_url+path
        response=None
        response = requests.get(url, params=params,headers=self.headers)        
        return response.json()['response'] if response else None

    def get_song(self,id):
        path="songs/{id}".format(id=id)
        return self.make_request(path)

    def get_artist(self,id):
        path="artists/{id}".format(id=id)
        return self.make_request(path)
    
    def get_artist_songs(self,id,sort='popularity',per_page=10,page=1):
        path="artists/{id}".format(id=id)
        params={'sort':sort,'per_page':per_page,'page':page}
        return self.make_request(path,params=params)

    def get_search(self,term):
        path="search/"
        params={'q':term}
        return self.make_request(path,params=params)
    
    def search_web(self,term,per_page=5):
        path="search/multi"
        params={'per_page':per_page,'q':term}
        url = "https://genius.com/api/" + path + urlencode(params)
        response=requests.get(url)
        return response.json()['response'] if response else None
z=API('NpBI2c-OW6zs4SCPEK21YrdSg-Yfrkp48IBRXw05CCKoOoptkBSV4ECzJe2tEKg3')
print(z.get_artist('16775'))