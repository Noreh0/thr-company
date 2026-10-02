from models.item_catalogo.itemCatalogo import ItemCatalogo

class Blusas(ItemCatalogo):
    def __init__(self, nome, preco, descricao, tipo_gola):
        super().__init__(nome, preco, descricao)
        self.tipo_gola = tipo_gola