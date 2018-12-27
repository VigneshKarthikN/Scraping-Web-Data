from requests import get
from bs4 import BeautifulSoup 
import json

url = 'http://www.medeor247dubai.com/en.html'
response = get(url)

finaldata = {}
data = {}

def clean(text):
    text = text.replace('\n','')
    text = text.replace('\t','')
    text = text.replace('\u00a0','')
    return text

html_soup = BeautifulSoup(response.text, 'html.parser')
counter = 1
movie_containers = html_soup.find_all('ul', class_ = 'sublist')
movie_container = movie_containers[0].find_all('a')
for i in movie_container:
    new_url= i['href'] 
    response1 = get(new_url)
    html_soup1 = BeautifulSoup(response1.text, 'html.parser')
    profiles = html_soup1.find_all('div', class_ = 'row row-centered')
    if(profiles):
        profile = profiles[0].find_all('div', class_= 'col-sm-4 col-centered doc-list ')
        for prof in profile:
            p=(prof.find('a', class_ = 'view-prof-btn'))
            spec_prof = p['href']
            response2 = get(spec_prof)
            html_soup2 = BeautifulSoup(response2.text, 'html.parser')
            ind_profiles = html_soup2.find_all('div', class_ = 'col-sm-12 doc-list first')
            img = ind_profiles[0].find_all('img')[0]['src']
            detail1 = html_soup2.find_all('div', class_ = 'col-sm-8')
            name = detail1[0].h4.text
            speciality = detail1[0].h6.text
            location = []
            experience = []
            locns = detail1[0].find_all('div', class_ = 'doc_desc')[0].find_all('ul')
            exps = locns[-1].find_all('li')
            lcns = locns[0].find_all('li')
            for exp in exps:
                e = clean(exp.text)
                experience.append(e)
            for l in lcns:
                lo = clean(l.text)
                location.append(lo)
            data = {"1)Name" : name, "2)Image" : img , "3)Speciality" : speciality , "4)Location" : location, "5)Experience":experience}
            finaldata[counter]=data
            counter += 1
           
with open('dataop.txt', 'w') as outfile:  
    json.dump(finaldata, outfile, indent = 4)