import pandas as pd
from bs4 import BeautifulSoup
import requests
import pickle
import random

with open("evtlst", "rb") as fp:
    allurls = pickle.load(fp)
# urls = ["https://ecpr.eu/Events/Event/PaperDetails/65996",
#         "https://ecpr.eu/Events/Event/PaperDetails/65997",
#         "https://ecpr.eu/Events/Event/PanelDetails/12379",
#         "https://ecpr.eu/Events/Event/PanelDetails/12361"]
urls = random.sample(allurls, 10)
urls = allurls
dataset = pd.DataFrame()
issues = []
for url in urls:
    try:
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        title = soup.title.text.strip()
        presdict = {}
        preslist =[]
        affpreslist = []
        for pres in soup.find("div", {"id": "PresenterCol"}).find_all("a"):
            preslist.append(pres.text.strip())
            affpreslist.append(pres.find_next("div").text.strip())
        for index in range(len(preslist)):
            presdict.update({"pres"+str(index+1) : preslist[index]})

        autdict = {}
        autlist =[]
        affautlist = []
        for aut in soup.find("div", {"id": "PresenterCol"}).find_next_sibling().find_all("a"):
            autlist.append(aut.text.strip())
            affautlist.append(aut.find_next("div").text.strip())

        for index in range(len(preslist)):
            presdict.update({"pres"+str(index+1) : preslist[index]})
        for index in range(len(affpreslist)):
            presdict.update({"affpres"+str(index+1) : affpreslist[index]})
        for index in range(len(autlist)):
            autdict.update({"author"+str(index+1) : autlist[index]})
        for index in range(len(affautlist)):
            presdict.update({"affaut"+str(index+1) : affautlist[index]})

        count = 1
        tagdict = dict()
        for tag in soup.find_all("div", {"class": "badge"}):
            tagdict.update({"tag"+str(count) : tag.text.strip()})
            count += 1

        abstract = soup.find("div", {"style":"white-space: pre-wrap;"}).text.strip()
        data = presdict | autdict | tagdict
        data.update({"abstract" : abstract,
                     "title" : title,
                     "url": url})
        dataset = pd.concat([dataset, pd.DataFrame.from_dict([data])])
    except:
        print(url)
        issues.append(url)
issues

dataset = dataset.reindex(sorted(dataset.columns), axis=1)
dataset.to_csv("dataset_sorted.csv")



### Für eine URL ###
url = "https://ecpr.eu/Events/Event/PaperDetails/65996"
url = "https://ecpr.eu/Events/AcademicProgramme/PaperList/185"
html_doc = requests.get(url).text
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())
title = soup.title.text.strip()

len(soup.find_all("a"))

for d in soup.find_all("a"):
    print(d.get('href'))

presdict = {}
preslist =[]
affpreslist = []
for pres in soup.find("div", {"id": "PresenterCol"}).find_all("a"):
    preslist.append(pres.text.strip())
    affpreslist.append(pres.find_next("div").text.strip())

for index in range(len(preslist)):
    presdict.update({"pres"+str(index+1) : preslist[index]})

autdict = {}
autlist =[]
affautlist = []
for aut in soup.find("div", {"id": "PresenterCol"}).find_next_sibling().find_all("a"):
    autlist.append(aut.text.strip())
    affautlist.append(aut.find_next("div").text.strip())

for index in range(len(preslist)):
    presdict.update({"pres"+str(index+1) : preslist[index]})
for index in range(len(affpreslist)):
    presdict.update({"affpres"+str(index+1) : affpreslist[index]})
for index in range(len(autlist)):
    autdict.update({"author"+str(index+1) : autlist[index]})
for index in range(len(affautlist)):
    presdict.update({"affaut"+str(index+1) : affautlist[index]})

count = 1
tagdict = dict()
for tag in soup.find_all("div", {"class": "badge"}):
    tagdict.update({"tag"+str(count) : tag.text.strip()})
    count += 1
    print(tag.text)

abstract = soup.find("div", {"style":"white-space: pre-wrap;"}).text.strip()

data = presdict | autdict | tagdict
data.update({"abstract" : abstract,
             "title" : title})

d2 = pd.DataFrame.from_dict([data])