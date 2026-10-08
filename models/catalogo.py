from models.item_catalogo.acessorios import Acessorios
from models.item_catalogo.blusas import Blusas
from models.item_catalogo.calcas import Calcas
from models.item_catalogo.camisas import Camisas
from models.item_catalogo.itemCatalogo import ItemCatalogo
from models.item_catalogo.tenis import Tenis

class Catalogo:
    def __init__(self):
        self._roupas = []
    def adicionar_produto(self, item):
        if isinstance(item, ItemCatalogo):
            self._roupas.append(item)
        else:
            return "O item não é uma roupa ou acessório!"
    def listar_produtos(self):
        for i,roupa in enumerate(self._roupas, start=1):
            print (f"{i}-{roupa.nome}\nR${roupa.preco}\n==================\n")
    def listar_info_produtos(self, item):
        if isinstance(item, Tenis):
            print (f"{item.nome} - {item.preco} - {item.descricao} - {item.tipo_sola} - {item.categoria}")
        elif isinstance(item, Camisas):
            print (f"{item.nome} - {item.preco} - {item.descricao} - {item.tipo_manga} - {item.categoria}")
        elif isinstance(item, Calcas):
            print (f"{item.nome} - {item.preco} - {item.descricao} - {item.tipo_modelagem} - {item.categoria}")
        elif isinstance(item, Blusas):
            print (f"{item.nome} - {item.preco} - {item.descricao} - {item.tipo_gola} - {item.categoria}")
        elif isinstance(item, Acessorios):
            print (f"{item.nome} - {item.preco} - {item.descricao} - {item.tipo_gola} - {item.categoria}")
        else:
            print(f"Não é um item")