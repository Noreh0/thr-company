from database.db import conectar

def tabela_catalogo():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS catalogo(
            id PRIMARY KEY AUTO_INCREMENT,
            id_produto INT,
            FOREIGN KEY (id_produto) REFERENCES produto(id)
        )
    """)
    conexao.commit()
    conexao.close(
        
    )

def adicionar_item_ao_catalogo(item):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            INSERT INTO catalogo(id_produto) VALUES (%s)
        """,
        (item.id,)
    )
    conexao.commit()
    conexao.close()