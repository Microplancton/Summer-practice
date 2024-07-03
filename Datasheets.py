import pymysql

from ConfigDB import host, user, password, db_name

def connect_to_db():
    """
    Подключение к базе данных MySQL.
    """
    try:
        connection = pymysql.connect(
            host = host,
            port = 3307,
            user = user,
            password = password,
            database = db_name,
            cursorclass = pymysql.cursors.DictCursor
        )

        print("Подключение к базе данных установлено!")
        return connection
    
    except Exception as ex:
        print("Ошибка подключения к базе данных!")
        print(ex)
        return None


def create_table(connect):
    """
    Создаем таблицу 'parsing' в базе данных.
    """
    try:
        with connect.cursor() as cursor:
            craete_table_query = """
                CREATE TABLE parsing (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    Vacancy VARCHAR(32),
                    Company VARCHAR(32),
                    salary VARCHAR(32),
                    url VARCHAR(52)
                )
            """
            cursor.execute(craete_table_query)
            print("Таблица 'parsing' успешно создана!")

    except Exception as ex:
        print("Ошибка создания таблицы!")
        print(ex)

    finally:
        connect.close()
