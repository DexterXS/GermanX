

import pymysql

# Подключение к базе данных
connection = pymysql.connect(
    host='host',
    user='user',
    password='password',
    database='db_name',
    port=3306
)

try:
    # Создание курсора
    with connection.cursor() as cursor:
        # Пример создания таблицы (если её нет)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS example_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT
        )
        """
        cursor.execute(create_table_query)

        # Пример добавления данных
        insert_query = "INSERT INTO example_table (name, age) VALUES (%s, %s)"
        data_to_insert = ("Иванов", 25)
        cursor.execute(insert_query, data_to_insert)

        # Применение изменений
        connection.commit()

        # Пример чтения данных
        select_query = "SELECT * FROM example_table"
        cursor.execute(select_query)
        result = cursor.fetchall()

        # Вывод результатов
        print("Результаты запроса:")
        for row in result:
            print(row)

finally:
    # Закрытие соединения
    connection.close()
