from database.db import conectar
from models.item_catalogo.acessorios import Acessorios
from models.item_catalogo.blusas import Blusas
from models.item_catalogo.calcas import Calcas
from models.item_catalogo.camisas import Camisas
from models.item_catalogo.tenis import Tenis

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
def criar_produto(id_catalogo, produto):
    if isinstance(produto, Acessorios):
        categoria = "acessorio"
        material = produto.material
    elif isinstance(produto, Blusas):
        categoria = "blusas"
        tipo_gola = produto.tipo_gola
    elif isinstance(produto, Calcas):
        categoria = "calcas"
        tipo_modelagem = produto.tipo_modelagem
    elif isinstance(produto, Camisas):
        categoria = "camisas"
        tipo_manga = produto.tipo_manga
    elif isinstance(produto, Tenis):
        categoria = "tenis"
        tipo_sola = produto.tipo_sola
    else:
        return f"Não é um produto!"
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            INSERT INTO item_catalogo(nome, preco, descricao, categoria, id_catalogo, tipo_sola, tipo_manga, tipo_modelagem, tipo_gola, material)
        """, (produto.nome, produto.preco, produto.descricao, categoria, id_catalogo, tipo_sola, tipo_manga, tipo_modelagem, tipo_gola, material),
    )
    conexao.commit()
    conexao.close()

def listar_itens_catalogos():
    pass