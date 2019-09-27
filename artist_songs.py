import requests,os
import re
from bs4 import BeautifulSoup
from string import punctuation
from urllib.parse import urlencode

class song:
    def __init__(self,song_id):
        response = get_song(song_id)["song"]
        try:
            self.title=response["title"]  
            self.url=response["url"]     
            if response["album"]!=None:
                self.album_name=response["album"]["name"] 
                self.album_id=response["album"]["id"]  
            else:
                self.album_name="undifined"            
                self.album_id="0000"  
        except (KeyError,TypeError) as k:
            print(k)



base_url = 'https://api.genius.com/'
headers = {'Authorization': 'Bearer ' + 'Jd2legv5bhOgJlvA_OJjYArjckyA771GSOi-CLXtUGp0D-tGUBqUeu01Azo1qvtO'}

def clean(s):
    return s.translate(str.maketrans('', '', punctuation)).replace('\u200b', " ").strip().lower()

def clean_text(text):
    text = text.replace(u"\u2019", "'") #right quotation mark
    text = text.replace(u"\u2018", "'") #left quotation mark
    text = text.replace(u"\u02bc", "'") #a with dots on top
    text = text.replace(u"\xe9", "e") #e with an accent
    text = text.replace(u"\xe8", "e") #e with an backwards accent
    text = text.replace(u"\xe0", "a") #a with an accent
    text = text.replace(u"\u2026", "...") #ellipsis apparently
    text = text.replace(u"\u2012", "-") #hyphen or dash
    text = text.replace(u"\u2013", "-") #other type of hyphen or dash
    text = text.replace(u"\u2014", "-") #other type of hyphen or dash
    text = text.replace(u"\u201c", '"') #left double quote
    text = text.replace(u"\u201d", '"') #right double quote
    text = text.replace(u"\u200b", ' ') #zero width space ?
    text = text.replace(u"\x92", "'") #different quote
    text = text.replace(u"\x91", "'") #still different quote
    text = text.replace(u"\xf1", "n") #n with tilde!
    text = text.replace(u"\xed", "i") #i with accent
    text = text.replace(u"\xe1", "a") #a with accent
    text = text.replace(u"\xea", "e") #e with circumflex
    text = text.replace(u"\xf3", "o") #o with accent
    text = text.replace(u"\xb4", "") #just an accent, so remove
    text = text.replace(u"\xeb", "e") #e with dots on top
    text = text.replace(u"\xe4", "a") #a with dots on top
    text = text.replace(u"\xe7", "c") #c with squigly bottom
    return text


def scrape_lyrics(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    div=soup.find("div",class_="lyrics")
    lyrics=div.get_text()
    lyrics = re.sub('(\[.*?\])*', '', lyrics)
    lyrics = re.sub('\n{2}', '\n', lyrics)
    return lyrics.strip("\n")

def scrape_album_name(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    span=soup.find_all("span",class_="metadata_unit-info")[1]
    album=span.text
    return album.strip("\n")

def make_request(path,params=None):
    uri=base_url+path
    response = requests.get(uri, params=params, headers=headers)
    return response.json()['response'] if response else None

def search(search_term):
    endpoint="search/"
    params={'q':search_term}
    return make_request(endpoint,params)

def search_artist(artist_id):
    endpoint="artists/{id}".format(id=artist_id)
    return make_request(endpoint)

def search_artist_songs(artist_id,sort='popularity',page_length=10,page=1):
    endpoint="artists/{id}/songs".format(id=artist_id)
    params={'sort':sort,'per_page':page_length,'page':page}
    return make_request(endpoint,params)

def get_song(song_id):
    endpoint="songs/{id}".format(id=song_id)
    return make_request(endpoint)

def scrape_song(song_id):
    s=song(song_id)
    lyrics=scrape_lyrics(s.url)
    return lyrics 

def scrape_artist_songs(artist_id,albums=[],all_song=False,max=200):
    """ scrape song of artist on given albums if all_songs is False otherwise all songs upto first max songs"""
    #check if artist folder already created or not
    count=1
    while count*10<max:
        response=search_artist_songs(artist_id,page=count)
        next_page=response["next_page"]
        songs=response["songs"]

        for i in range(0,len(songs)):
            song_id=songs[i]["id"]
            s=song(song_id)
            #title
            title=clean(s.title.strip("\\"))
            print(title)
            #get lyrics   
            lyrics=scrape_lyrics(s.url)
            #get album
            album=s.album_name
            if album =="undefined":
                #get album thorugh scraping
                album=scrape_album_name(s.url)
                if not album:
                    album ="unknown"
            album=clean(album.strip("\n"))
            try:
                if album in albums:
                    os.makedirs("{a}".format(a=album),exist_ok=True)
                    file=open(os.path.join(album,title),"w")
                    file.write(clean_text(lyrics))
            except (OSError,UnicodeEncodeError) as e:
                print(e)       
    
        if next_page==None:
            break
        else:
            count+=1

scrape_artist_songs(1177,albums=["Red","1989"])

