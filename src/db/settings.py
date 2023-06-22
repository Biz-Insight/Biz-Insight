import os
import csv


def get_mysql_connection(host, user, password, database):
    import mysql.connector

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    return mydb
