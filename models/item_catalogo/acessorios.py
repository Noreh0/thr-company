from models.item_catalogo.itemCatalogo import ItemCatalogo

class Acessorios(ItemCatalogo):
    def __init__(self, nome, preco, descricao, categoria, material):
        super().__init__(nome, preco, descricao, categoria)
        self.material = material