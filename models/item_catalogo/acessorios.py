from models.item_catalogo.itemCatalogo import ItemCatalogo

class Acessorios(ItemCatalogo):
    def __init__(self, nome, preco, descricao, material):
        super().__init__(nome, preco, descricao)
        self.material = material