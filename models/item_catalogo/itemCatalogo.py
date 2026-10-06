from models.item_catalogo.avaliacao import Avaliacao
class ItemCatalogo():
    def __init__(self, nome, preco, descricao, categoria):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria
        self._avaliacao = []

    def __str__(self):
        return f"Produto: {self.nome} - Preço: {self.preco}"