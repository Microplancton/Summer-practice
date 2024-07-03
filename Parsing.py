import requests

def get_vacancies(keyword):
    """
    Функция для получения вакансий с сайта hh.ru
    """
    url = "https://api.hh.ru/vacancies"
    params = {
        "area": [],  # Все зоны
        "text": keyword,
        "per_page": 20,  # Кол-во объектов на странице

    }
    headers = {

        "User-Agent": "MTUCI_Practise"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200: # 200 - успешность запроса
        datasheets = response.json()
        vacancies = datasheets.get("items", [])

        if vacancies:
            for vacancy in vacancies:
                vacancy_url = vacancy.get("alternative_url")
                vacancy_title = vacancy.get("name")
                company_name = vacancy.get("employer", {}).get("name")
                print(f"Вакансия: {vacancy_title}\nКомпания: {company_name}\nURL-адрес: {vacancy_url}\n")
        else:
            print("Вакансий по данному запросу не найдено(")
    else:
        print(f"Запрос не удался. Код ошибки: {response.status_code}")
