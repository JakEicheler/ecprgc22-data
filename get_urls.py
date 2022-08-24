import pandas as pd
from bs4 import BeautifulSoup
import requests


evtlst = []
for index in range(1, 19):
    print(index)
    with open("pages/Paper List - ECPR General Conference, University of Innsbruck, 22 – 26 August 2022_"+str(index)+".htm") as f:
        soup = BeautifulSoup(f, 'html.parser')
    for d in soup.find_all("a"):
        print(d.get('href'))
        if d.get('href') is not None and d.get('href').startswith("https://ecpr.eu/Events/PaperDetails.aspx?PaperID="):
            evtlst.append(d.get('href'))

len(evtlst)

import pickle
with open("evtlst", "wb") as fp:
    pickle.dump(evtlst, fp)

with open("evtlst", "rb") as fp:
    b = pickle.load(fp)