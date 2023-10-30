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

url = "https://dges.gov.pt/coloc/2023/col1listaser.asp?CodEstab=0300&CodCurso=9119&ids=0&ide=2&Mx=10000"
filename = 'ttt.csv'

scrap_page(url, filename)