from models.item_catalogo.itemCatalogo import ItemCatalogo

class Camisas(ItemCatalogo):
    def __init__(self, nome, preco, descricao, tipo_manga):
        super().__init__(nome, preco, descricao)
        self.tipo_manga = tipo_manga
