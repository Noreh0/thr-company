from models.item_catalogo.avaliacao import Avaliacao
class ItemCatalogo():
    def __init__(self, nome, preco, descricao):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self._avaliacao = []

    def __str__(self):
        return f"Produto: {self.nome} - Preço: {self.preco}"