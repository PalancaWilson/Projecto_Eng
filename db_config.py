import mysql.connector



conexao = mysql.connector.connect (
        host='localhost',
        user='root',
        password='mutombo21',
        database='ispsecurity'
    )

if conexao.is_connected():
    print("Conetado com sucesso")

cursor = conexao.cursor()

conexao.close()
cursor.close()

