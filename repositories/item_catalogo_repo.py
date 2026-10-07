from database.db import conectar

def tabela_itens_catalogo():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS item_catalogo(
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL,
                preco FLOAT(6,2) NOT NULL,
                descricao TEXT NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                id_avaliacao INT,
                id_catalogo INT,
                tipo_sola VARCHAR(100),
                tipo_manga VARCHAR(100),
                tipo_modelagem VARCHAR(100),
                tipo_gola VARCHAR(100),
                material VARCHAR(100),
                FOREIGN KEY (id_avaliacao) REFERENCES avaliacoes(id),
                FOREIGN KEY (id_catalogo) REFERENCES catalogo(id)
            )
        """
    )
    conexao.commit()
    conexao.close()