import pymysql.cursors

from settings.confidential_data import host, user, password, db_name

try:
    connections = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected...")
except Exception as ex:
    print("Connection refused...")
    print(ex)