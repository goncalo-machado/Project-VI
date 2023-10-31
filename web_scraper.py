import urllib3
from bs4 import BeautifulSoup 
from urllib3.util.ssl_ import create_urllib3_context
import csv

def scrap_page(url, filename):
    ctx = create_urllib3_context()
    ctx.load_default_certs()
    ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT

    with urllib3.PoolManager(ssl_context=ctx) as http:
        r = http.request("GET", url)
        #print(r.status)
        if (r.status != 200):
            with open(filename + "_NoData", 'w', newline='',encoding='utf-8-sig') as f: 
                w = csv.DictWriter(f,['Order Number','Parcial Identification Number','Name','Applicant Grade','Option Number','Entrance Test Grade','12th year grade','Average of 11th and 10th grades']) 
                w.writeheader() 
            return

    document = BeautifulSoup(r.data, 'html.parser')

    tables = document.find_all('table', class_='caixa')

    table = tables[2]

    candidates = []

    for td in table.find_all('tr'):
        data = list(td.stripped_strings)
        candidate = {}
        candidate['Order Number'] = data[0]
        candidate['Parcial Identification Number'] = data[1]
        candidate['Name'] = data[2]
        candidate['Applicant Grade'] = data[3]
        candidate['Option Number'] = data[4]
        candidate['Entrance Test Grade'] = data[5]
        candidate['12th year grade'] = data[6]
        candidate['Average of 11th and 10th grades'] = data[7]
        candidates.append(candidate)

    with open(filename, 'w', newline='',encoding='utf-8-sig') as f: 
        w = csv.DictWriter(f,['Order Number','Parcial Identification Number','Name','Applicant Grade','Option Number','Entrance Test Grade','12th year grade','Average of 11th and 10th grades']) 
        w.writeheader() 
        
        w.writerows(candidates)

def url_maker(year,university_code, course_code):
    return "https://dges.gov.pt/coloc/" + year + "/col1listaser.asp?CodEstab=" + university_code + "&CodCurso=" + course_code + "&ids=0&ide=10000&Mx=10000"


university_course_dict = {}

# university_course_dict['L221'] = ['0300']
# #university_course_dict['L221'] = ['0300', '1518', '1000']
# university_course_dict['L223'] = ['0300']
# university_course_dict['L202'] = ['0300']
# university_course_dict['L217'] = ['0300']
# #university_course_dict['L209'] = ['0300', '0501', '1518', '0903', '1105', '1203', '3064', '3083']
# university_course_dict['L209'] = ['0300']
university_course_dict['9119 '] = ['6800', '0203', '0400', '0501','0602','1503','1307','1000','0903','1203','3023','3043','3053','3065','3064','3092','3102','3122','3138','3135','3152','3242','3163','3182','2910','2920','4375','2100','1350','2750','2410','2500','4602','4442','4530','4640','4572']
#university_course_dict['9119 '] = ['0300']
years = ['2021','2022','2023']

for year in years:
    for course in university_course_dict.keys():
        for university in university_course_dict[course]:
            print(f"Year {year} course {course} university {university}")
            url = url_maker(year, university, course)
            print(f"url {url}")
            filename = year + "_" + course + "_" + university
            print(f"filename {filename}")
            scrap_page(url, filename)