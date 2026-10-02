from models.item_catalogo.itemCatalogo import ItemCatalogo

class Tenis(ItemCatalogo):
    def __init__(self, nome, preco, descricao, tipo_sola):
        super().__init__(nome, preco, descricao)
        self.tipo_sola = tipo_sola