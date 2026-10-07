from models.item_catalogo.itemCatalogo import ItemCatalogo

class Blusas(ItemCatalogo):
    def __init__(self, nome, preco, descricao, categoria, tipo_gola):
        super().__init__(nome, preco, descricao, categoria)
        self.tipo_gola = tipo_gola