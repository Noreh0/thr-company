import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'company'
    )
    return conexao