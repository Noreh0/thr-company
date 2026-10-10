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
                tipo_sola VARCHAR(100),
                tipo_manga VARCHAR(100),
                tipo_modelagem VARCHAR(100),
                tipo_gola VARCHAR(100),
                material VARCHAR(100),
            )
        """
    )
    conexao.commit()
    conexao.close()
def criar_produto(id_catalogo, produto):
    if isinstance(produto, Acessorios):
        categoria = "acessorio"
        material = produto.material
        tipo_gola, tipo_modelagem, tipo_manga, tipo_sola = None
    elif isinstance(produto, Blusas):
        categoria = "blusas"
        tipo_gola = produto.tipo_gola
        material, tipo_modelagem, tipo_manga, tipo_sola = None
    elif isinstance(produto, Calcas):
        categoria = "calcas"
        tipo_modelagem = produto.tipo_modelagem
        material, tipo_gola, tipo_manga, tipo_sola = None
    elif isinstance(produto, Camisas):
        categoria = "camisas"
        tipo_manga = produto.tipo_manga
        material, tipo_gola, tipo_modelagem, tipo_sola = None
    elif isinstance(produto, Tenis):
        categoria = "tenis"
        tipo_sola = produto.tipo_sola
        material, tipo_gola, tipo_manga, tipo_manga = None
    else:
        return f"Não é um produto!"
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            INSERT INTO item_catalogo(nome, preco, descricao, categoria, tipo_sola, tipo_manga, tipo_modelagem, tipo_gola, material) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (produto.nome, produto.preco, produto.descricao, categoria, tipo_sola, tipo_manga, tipo_modelagem, tipo_gola, material),
    )
    conexao.commit()
    conexao.close()

def listar_itens_catalogos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT * FROM item_catalogo
        """
    )
    resultado = cursor.fetchall()
    conexao.close()
    itens_encontrados = []
    for item in resultado:
        itens_encontrados.append(item)
    return itens_encontrados

def listar_categoria(categoria):
    if categoria == 'acessorio':
        categoria_search = 'acessorio'
    elif categoria == 'blusas':
        categoria_search = 'blusas'
    elif categoria == 'calcas':
        categoria_search = 'calcas'
    elif categoria == 'camisas':
        categoria_search = 'camisas'
    elif categoria == 'tenis':
        categoria_search = 'tenis'
    else:
        return f"Categoria não encontrada"

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT * FROM item_catalogo WHERE categoria = %s
        """,
        (categoria_search,)
    )
    resultado = cursor.fetchall()
    conexao.close()
    itens_econtrados = []
    for item in resultado:
        itens_econtrados.append(item)
    return itens_econtrados