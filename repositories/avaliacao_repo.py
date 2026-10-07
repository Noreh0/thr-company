from database.db import conectar

def tabela_avaliacao():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes(
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_produto INT,
            id_usuario INT,
            nome VARCHAR(255) NOT NULL,
            nota DECIMAL(2,1) NOT NULL,
            descricao TEXT,
            FOREIGN KEY (id_produto) REFERENCES produto(id),
            FOREIGN KEY (id_usuario) REFERENCES usuario(id)
        )
    """)
    conexao.commit()
    conexao.close()

