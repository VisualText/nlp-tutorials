import urllib.request
import os
import codecs
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from pathlib import Path
import re

wordsfile = os.path.join(os.path.dirname(__file__), "urls.txt")
file1 = codecs.open(wordsfile, "r", "utf-8")
lines = file1.readlines()

urlbase = "https://state.1keydata.com/"
  
count = 0
for url in lines:
    url = url.strip()
    pieces = url.split("/")
    state = pieces[len(pieces)-1]
    filepath = state.replace(" ","_").replace(".php","")
    htmlDir = os.path.join(os.path.dirname(__file__),"html")
    if not os.path.exists(htmlDir):
        os.makedirs(htmlDir)
    statefile = os.path.join(htmlDir,filepath + ".html")
    print(statefile, end =" ")

    if os.path.exists(statefile):
        print (' exists')
        continue
    
    found = False

    try:
        page = urllib.request.urlopen(url)
    except HTTPError as e:
        print(' Error code: ', e.code)
        file1 = open(os.path.join(os.path.dirname(__file__), "urlorphans.txt"), "a")
        file1.write(url + "\n")
        file1.close()
    except URLError as e:
        print('Reason: ', e.reason)
    else:
        found = True
    
    if found == True:
        pagehtml = page.read()
        soup = BeautifulSoup(pagehtml, 'html.parser')
        body = soup.find('body')

        if body:
            print(' DOWNLOADED')
            file = codecs.open(statefile, "w", "utf-8")
            file.write(url + '\n' + str(body))
            file.close()
        else:
            print(' no defs')
            file2 = open(os.path.join("input","nobody.txt"), "a")
            file2.write(url + "\n")
            file2.close()