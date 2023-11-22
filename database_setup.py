import mysql.connector

def create_database():
    # З'єднання з MySQL-сервером
    db_connection = mysql.connector.connect(
        host="localhost",
        user="xsolo",
        password="19812009"
    )
    db_cursor = db_connection.cursor()

    # Створення бази даних
    db_cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")

    # Використання створеної бази даних
    db_cursor.execute("USE mydatabase")

    # Створення таблиці для користувачів
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    # Закриття курсора та з'єднання з базою даних
    db_cursor.close()
    db_connection.close()

def register(username, password):
    db_connection = mysql.connector.connect(
        host="ваш_хост",
        user="ваш_користувач",
        password="ваш_пароль",
        database="mydatabase"
    )
    db_cursor = db_connection.cursor()

    # Додавання нового користувача
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    values = (username, password)
    db_cursor.execute(query, values)

    db_connection.commit()

    db_cursor.close()
    db_connection.close()

def login(username, password):
    db_connection = mysql.connector.connect(
        host="ваш_хост",
        user="ваш_користувач",
        password="ваш_пароль",
        database="mydatabase"
    )
    db_cursor = db_connection.cursor()

    # Пошук користувача за ім'ям та паролем
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    values = (username, password)
    db_cursor.execute(query, values)

    user = db_cursor.fetchone()

    db_cursor.close()
    db_connection.close()

    return user

if __name__ == "__main__":
    create_database()
    print("База даних та таблиці створено.")
