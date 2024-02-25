import psycopg2
from psycopg2 import OperationalError
import requests


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    return connection

# Replace these with your actual database credentials
db_name = "database"
db_user = "username"
db_password = "password"
db_host = "localhost"  # or your database host
db_port = "5432"  # default PostgreSQL port

connection = create_connection(db_name, db_user, db_password, db_host, db_port)
cur = connection.cursor()
checked = set()
cur.execute('select * from cars;')
res = cur.fetchall()
for car in res:
    carinfo = car[1] + car[2] + str(car[3])
    print(carinfo)
    if carinfo not in checked:
        checked.add(carinfo)

        url = 'https://api.carsxe.com/images'
        params = {
            'key': 'qpipo8mtu_9g31d22xw_doqu6p7t0',
            'make': 'toyota',
            'model': 'tacoma',
            'year': '2018',
            'color': 'blue',
            'format': 'json'
        }
        response = requests.get(url, params=params)
        data = response.json()
        print(data)

print(res)
print(len(res))

