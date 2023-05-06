from requests_html import HTMLSession
import os
import json

def main():
  vacancies_search_url = 'https://hh.ru/search/vacancy/'

  msk_search_area_id = 1
  spb_search_area_id = 2
  vacancies_search_params = {
    'text': 'Python',
    'area': [msk_search_area_id, spb_search_area_id],
    'only_with_salary': 'true'
  }

  html_session = HTMLSession()

  vacancies_search_req = html_session.get(
    url=vacancies_search_url,
    params=vacancies_search_params
  )

  vacancies_divs = vacancies_search_req.html.find('.serp-item')

  found_vacancies = []
  for vacancy_div in vacancies_divs:
    salary_span =\
      vacancy_div.find(
        selector='span[data-qa="vacancy-serp__vacancy-compensation"]',
        first=True
      )
    if salary_span and 'USD' in salary_span.text:
      vacancy_href =\
        vacancy_div.find('.serp-item__title', first=True)\
        .attrs['href']\
        .split(sep='?')[0]
      
      vacancy_req = html_session.get(url=vacancy_href)

      vacancy_descr_div =\
        vacancy_req.html.find(selector='.vacancy-section', first=True)
      if (vacancy_descr_div.find(containing='Django') or
          vacancy_descr_div.find(containing='Flask')):
        vacancy = dict()

        vacancy['href'] = vacancy_href

        vacancy['salary'] = salary_span.text
        
        company_name =\
          vacancy_div.find(
            selector='a[data-qa="vacancy-serp__vacancy-employer"]',
            first=True
          ).text
        vacancy['company_name'] = company_name

        address_div =\
          vacancy_div.find(
            selector='div[data-qa="vacancy-serp__vacancy-address"]',
            first=True
          )
        city_name = address_div.text.split(sep=',')[0]
        vacancy['city_name'] = city_name

        found_vacancies.append(vacancy)
  
  json_file_dir_name = os.path.dirname(__file__)
  json_file_name = 'found_vacancies.json'
  json_file_path = os.path.join(json_file_dir_name, json_file_name)
  with open(json_file_path, 'w') as json_file:
    json.dump(found_vacancies, json_file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
