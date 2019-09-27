from bs4 import BeautifulSoup
import requests, sys, webbrowser

print ('Googling')

res =requests.get("http://www.google.com/search?q="+' '.join(sys.argv[1:]))
res.raise_for_status

