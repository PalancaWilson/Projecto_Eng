import mysql.connector



def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='mutombo21',
        database='ispsecurity'
    )
#if conectar.is_connected():
 #   print("Conetado com sucesso")

#cursor = conectar.cursor()

#conectar.close()
#cursor.close()

