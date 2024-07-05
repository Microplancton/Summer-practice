import requests
import pymysql

from ConfigDB import host, user, password, db_name


def get_vacancies(keyword):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": keyword,
        "area": 1,  
        "per_page": 20,  # Кол-во объектов на странице
    }
    headers = {
        "User-Agent": "Practica_MTUCI",
    }

    response = requests.get(url, params=params, headers=headers)  # Запрос

    if response.status_code == 200: 
        data = response.json()
        vac = data.get("items", [])
        vac_list = []  
        for vacancy in vac:
            vac_title = vacancy.get('name')
            comp_name = vacancy.get('employer', {}).get("name")
            vac_salary = vacancy.get('salary')
            if vac_salary:
                vac_salary_from = vac_salary.get("from")
                vac_salary_to = vac_salary.get("to")
                vac_salary_currency = vac_salary.get("currency")
            else:
                vac_salary_from = None
                vac_salary_to = None
                vac_salary_currency = None
                vac_url = vacancy.get('alternate_url')

            # Добавляем вакансию в список
            vac_list.append({
                "vacancy_title": vac_title,
                "company_name": comp_name,
                "vacancy_salary_from": vac_salary_from,
                "vacancy_salary_to": vac_salary_to,
                "vacancy_salary_currency": vac_salary_currency,
                "vacancy_url": vac_url
            })

        # Добавляем вакансии в базу данных
        add_vac_to_db(vac_list)

    else:
        print(f"Запрос не удался. Код ошибки: {response.status_code}")  # Валидация ошибки, а также сообщение о ней клиенту


def add_vac_to_db(vacancy_list):
    try:
        connection = pymysql.connect(
            host = host,
            port = 3307,
            user = user,
            password = password,
            database = db_name,
            cursorclass = pymysql.cursors.DictCursor
        )
        print("Подключено")
        print("#" * 20)

        try:
            with connection.cursor() as cursor:
                for vacancy in vacancy_list:
                    create_meaning = f"INSERT INTO Parsing(vacancy_title, company_name,
                    vacancy_salary_from, vacancy_salary_to,
                    vacancy_salary_Currency, vacancy_url) VALUES('{vacancy['vacancy_title']}',
                    '{vacancy['company_name']}', '{vacancy['vacancy_salary_from']}', 
                    '{vacancy['vacancy_salary_to']}', '{vacancy['vacancy_salary_currency']}',
                    '{vacancy['vacancy_url']}');"

                    cursor.execute(create_meaning)
                connection.commit()

                print("Успешно добавлено")

            with connection.cursor() as cursor:
                select_all_rows = "SELECT * FROM Parsing"
                cursor.execute(select_all_rows)
                rows = cursor.fetchall()

                for row in rows:
                    print(row)

        finally:
            connection.close()

    except Exception as ex:
        print("Соединение потеряно")
        print(ex)


