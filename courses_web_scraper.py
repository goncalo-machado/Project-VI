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

    try:
        table = tables[1]
    except:
        return

    courses = []

    for td in table.find_all('tr'):
        try:
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
        except:
            continue
        
    w.writerows(courses)

def url_maker(year,university_code):
    return "https://dges.gov.pt/coloc/" + year + "/col1listamin.asp?CodR=11&CodEstab=" + university_code

universities = ['0300', '6800', '0203', '0400', '0501','0602','1503','1307','1000','0903','1203','3023','3043','3053','3065','3064','3092','3102','3122','3138','3135','3152','3242','3163','3182','2910','2920','4375','2100','1350','2750','2410','2500','4602','4442','4530','4640','4572']
courses = ['9119']
years = ['2021','2022','2023']
filename = 'Dataset_LEI_2021_2023.csv'

with open(filename, 'w', newline='',encoding='utf-8-sig') as f: 
        w = csv.DictWriter(f,['Course Code','Course Name','Course Type','Last Placed Candidate Grade', 'University Code', 'Year']) 
        w.writeheader() 
        for year in years:
            for university in universities:
                print(f"Year {year} university {university}")
                url = url_maker(year, university)
                print(f"url {url}")
                scrap_page(url, w, year, university, courses)