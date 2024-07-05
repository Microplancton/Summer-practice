import requests
import pymysql

from ConfigDB import host, user, password, db_name


def get_vacancies(keyword):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": keyword,
        "area": [],  # Все зоны
        "per_page": 1,  # # Кол-во объектов на странице
    }
    headers = {
        "User-Agent": "Practica_MTUCI", 
    }

    response = requests.get(url, params=params, headers=headers) #запрос

    if response.status_code == 200: # 200 - успех запроса
        data = response.json()
        vacancies = data.get("items", [])
        for vacancy in vacancies:
            global comp_name       
            global vac_salary_from
            global vac_salary_to
            global vac_title
            global vac_url 
            global vac_salary_currency
            vac_salary = vacancy.get('salary')
            vac_title = vacancy.get('name')
            comp_name = vacancy.get('employer', {}).get("name")
            if vac_salary:
                vac_salary_from = vac_salary.get("from")
                vac_salary_to = vac_salary.get("to")
                vac_salary_currency = vac_salary.get("currency")
            else:
                vac_salary_from = None
                vac_salary_to = None
                vac_salary_currency = None

            vac_url = vacancy.get('alternate_url')
            
            print(f"Вакансия : {vac_title}\nКомпания : {comp_name}\nsalary_from : {vac_salary_from}\nsalary_to : {vac_salary_to}\n Salary Curr : {vac_salary_currency}\nURL-адресс: {vacancy_url}\n")
            
    else:
        print(f"Запрос не удался. Код ошибки: {response.status_code}") # Валидация ошибки, а также сообщение о ней клиенту



get_vacancies(input()):

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
        # Создадим таймер в 15 сек на очищение таблицы
        with connection.cursor() as cursor:
            query = "CREATE EVENT delete_all_rows ON SCHEDULE EVERY 15 SECOND DO BEGIN DELETE FROM Parsing; END"
            cursor.execute(query)

            # Запустим обработчик событий 
            cursor.execute("SET GLOBAL event_scheduler = ON")
            
        with connection.cursor() as cursors:
            create_meaning = f"INSERT INTO Parsing(vacancy_title, company_name, 
            vacancy_salary_from, vacancy_salary_to, vacancy_salary_Currency, 
            vacancy_url) VALUES('{vac_title}', '{comp_name}',
            '{vac_salary_from}', '{vac_salary_to}', '{vac_salary_currency}',
            '{vac_url}');"

            cursors.execute(create_meaning)
            connection.commit()

            print("Успешно добавлено")

    finally:
        connection.close()
    

except Exception as ex: 
    print("Соединение потеряно")
    print(ex)


print(vac_title, comp_name, vac_salary_from, vac_salary_to, vac_salary_currency, vac_url)