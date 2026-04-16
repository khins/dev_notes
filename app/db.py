import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="dev_notes",
        user="kevin",
        password="Co597oms!",
        host="localhost",
        port="5432"
    )