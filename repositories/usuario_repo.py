from database.db import conectar

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
            INSERT INTO usuarios VALUES %s, %s, %s
        """, (usuario.nome, usuario.email, usuario._senha_hash)
    )
    conexao.commit()
    conexao.close()

