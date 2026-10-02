from models.item_catalogo.itemCatalogo import ItemCatalogo

class Calca(ItemCatalogo):
    def __init__(self, nome, preco, descricao, tipo_modelagem):
        super().__init__(nome, preco, descricao)
        self.tipo_modelagem = tipo_modelagem