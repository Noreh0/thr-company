from models.item_catalogo.tenis import Tenis
from models.item_catalogo.camisas import Camisas
from models.item_catalogo.blusas import Blusas
from models.item_catalogo.acessorios import Acessorios
from models.item_catalogo.calcas import Calcas
from models.item_catalogo.avaliacao import Avaliacao
class ItemCatalogo():
    produtos = []
    def __init__(self, nome, preco, descricao, categoria):
        self._nome = nome
        self._preco = preco
        self._descricao = descricao
        self.categoria = categoria
        self._avaliacao = []

    def __str__(self):
        return f"Produto: {self.nome} - Preço: {self.preco}"

    def listar_produtos(self):
        for indice, item in enumerate(self.produtos, start=1):
            linha = f"{indice} - {item._nome} - {item._preco} - {item._descricao}"
            if isinstance(item, Acessorios):
                item.categoria = "Acessorios"
                linha += f" - {item.categoria} - {item.material}"
            elif isinstance(item, Blusas):
                item.categoria = "Blusas"
                linha += f" - {item.categoria} - {item.tipo_gola}"
            elif isinstance(item, Calcas):
                item.categoria = "Calças"
                linha += f" - {item.categoria} - {item.tipo_modelagem}"
            elif isinstance(item, Camisas):
                item.categoria = "Camisas"
                linha += f" - {item.categoria} - {item.tipo_manga}"
            elif isinstance(item, Tenis):
                item.categoria = "Tenis"
                linha += f" - {item.categoria} - {item.tipo_sola}"
            else:
                linha = "Não é um produto válido"
            print(linha)
