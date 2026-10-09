from database.db import conectar
from models.usuario import Usuario

def tabela_usuario():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS usuario(
                id INT AUTO_INCREMENT PRYMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL,
                senha_hash VARCHAR(255) NOT NULL
            )
        """
    )

def criar_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            INSERT INTO usuarios VALUES (%s, %s, %s)
        """, (usuario.nome, usuario.email, usuario._senha_hash)
    )
    conexao.commit()
    id_resultado = cursor.lastrowid
    conexao.close()

    usuario.id = id_resultado
    return id_resultado

def verificar_email(email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT * FROM usuario WHERE email = %s
        """, (email,)
    )
    resultado = cursor.fetchone
    conexao.close()
    if resultado == None:
        return f"Usuário não encontrado!"
    id_resultado, nome_resultado, email_resultado, senha_hash = resultado
    usuario = Usuario(nome_resultado, email_resultado, senha_hash)
    usuario.id = id_resultado
    return usuario