import urllib3
from bs4 import BeautifulSoup 
from urllib3.util.ssl_ import create_urllib3_context
import csv

def scrap_page(url, w, year, university, wanted_courses):
    ctx = create_urllib3_context()
    ctx.load_default_certs()
    ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT

    with urllib3.PoolManager(ssl_context=ctx) as http:
        r = http.request("GET", url)
        #print(r.status)
        if r.status != 200:
            # with open(filename + "_NoData.csv", 'w', newline='',encoding='utf-8-sig') as f: 
            #     w = csv.DictWriter(f,['Course Code','Course Name','Course Type','Last Placed Candidate Grade']) 
            #     w.writeheader() 
            return

    document = BeautifulSoup(r.data, 'html.parser')

    tables = document.find_all('table', class_='caixa')

    table = tables[1]

    courses = []

    for td in table.find_all('tr'):
        data = list(td.stripped_strings)
        if data[0] not in wanted_courses:
            continue
        course = {}
        course['Course Code'] = data[0]
        course['Course Name'] = data[1]
        course['Course Type'] = data[2]
        course['Last Placed Candidate Grade'] = float(data[3].replace(',','.'))
        course['University Code'] = university
        course['Year'] = year
        courses.append(course)
        
    w.writerows(courses)

def url_maker(year,university_code):
    return "https://dges.gov.pt/coloc/" + year + "/col1listamin.asp?CodR=11&CodEstab=" + university_code

universities = ['0300']
courses = ['L221', 'L223', 'L202', 'L217', 'L209', '9119']
years = ['2021','2022','2023']
filename = 'Dataset_DETI_Courses_2021_2023.csv'

with open(filename, 'w', newline='',encoding='utf-8-sig') as f: 
        w = csv.DictWriter(f,['Course Code','Course Name','Course Type','Last Placed Candidate Grade', 'University Code', 'Year']) 
        w.writeheader() 
        for year in years:
            for university in universities:
                print(f"Year {year} university {university}")
                url = url_maker(year, university)
                print(f"url {url}")
                scrap_page(url, w, year, university, courses)