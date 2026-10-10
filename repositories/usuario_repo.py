from database.db import conectar
from models.usuario import Usuario

def tabela_usuario():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS usuarios(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL,
                telefone VARCHAR(20) NOT NULL,
                senha_hash VARCHAR(255) NOT NULL,
                is_admin BOOLEAN NOT NULL DEFAULT FALSE
            )
        """
    )

def criar_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            INSERT INTO usuarios(nome, email, telefone, senha_hash, is_admin) VALUES (%s, %s, %s, %s, %s)
        """, (usuario.nome, usuario.email, usuario.telefone, usuario._senha_hash, False)
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
            SELECT id, nome, email, telefone, senha_hash, is_admin FROM usuario WHERE email = %s
        """, (email,)
    )
    resultado = cursor.fetchone()
    conexao.close()
    if resultado == None:
        return f"Usuário não encontrado!"
    id_resultado, nome_resultado, email_resultado, telefone_resultado, senha_hash, is_admin = resultado
    usuario = Usuario(nome_resultado, email_resultado, telefone_resultado, senha_hash, is_admin=bool(is_admin))
    usuario.id = id_resultado
    return usuario