import requests
import pymysql

from ConfigDB import host, user, password, db_name
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class vac(BaseModel):
    vac_title: str
    comp_name: str
    vac_salary_from: str
    vac_salary_to: str
    vac_salary_currency: str
    vac_url: str

@app.get("/vacancies")
def get_vacancies(keyword: str):
    url = "https://api.hh.ru/vacancies"
    params = {
        "area": 1,  
        "text": keyword,
        "per_page": 20,  # Кол-во объектов на странице

    }
    headers = {

        "User-Agent": "MTUCI_Practise"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        datasheets = response.json()
        vacancies = datasheets.get("items", [])
        vac_list = []
        if vacancies:  # Проверка на наличие вакансий
            for vacancy in vacancies:
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

                vac_list.append(vacancy(
                    Vacancy_title = vac_title,
                    Company_name = comp_name,
                    Vacancy_salary_from = str(vac_salary_from),
                    Vacancy_salary_to = str(vac_salary_to),
                    Vacancy_salary_currency = vac_salary_currency,
                    Vacancy_url = vac_url
                ))

            vac_to_db(vac_list)
            return vac_list
        else:
            return {"error": "Вакансий по данному запросу не найдено."}
    else:
        return {"error": f"Запрос не удался. Код ошибки: {response.status_code}"}
    

    

def vac_to_db(vacancy_list):

    try:
        connect = pymysql.connect(
            Host = host,
            Port = 3307,
            User = user,
            Password = password,
            Database = db_name,
            Cursorclass = pymysql.cursors.DictCursor
        )
        print("Подключено")
        print("#" * 20)

        try:
            with connect.cursor() as cursor:
                for vacancy in vacancy_list:
                    craete_mean = f"INSERT INTO Parsing(vacancy_title, company_name, vacancy_salary_from, vacancy_salary_to, vacancy_salary_Currency, vacancy_url) VALUES('{vacancy.vacancy_title}', '{vacancy.company_name}', '{vacancy.vacancy_salary_from}', '{vacancy.vacancy_salary_to}', '{vacancy.vacancy_salary_currency}', '{vacancy.vacancy_url}');"
                    cursor.execute(craete_mean)
                connect.commit()
                print("Успешно добавлено")

            with connect.cursor() as cursor:
                sel_all_rows = "SELECT * FROM Parsing"
                cursor.execute(sel_all_rows)
                rows = cursor.fetchall()
                for row in rows:
                    print(row) # Вывод всех записей из таблицы 

        finally:
            connect.close()

    except Exception as ex:
        print("Соединение потеряно")
        print(ex)

