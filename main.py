import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json

def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()

responce = requests.get('https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text=python', headers=get_headers())

hh_main = responce.text

soup = BeautifulSoup(hh_main, features='lxml')

vacancy = soup.find_all('div', class_='serp-item')

parsed_data = []

for vac in vacancy:
    text = vac.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
    if 'Django' and 'Flask' in text:
        if vac.find('span', class_='bloko-header-section-3') == None:
            print("Вакансий нет")
        else :
            item = {'name': vac.find('a', class_='bloko-link bloko-link_kind-tertiary').text,
                    'city': vac.find('div', attrs={'data-qa': "vacancy-serp__vacancy-address"}).text,
                    'link': vac.find('a', class_ = "serp-item__title")['href'],
                    'text': vac.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    }
            parsed_data.append(item)

with open('hh.json', 'w', encoding='utf-8') as file:
    json.dump(parsed_data, file, ensure_ascii=False)
            


