from models.item_catalogo.itemCatalogo import ItemCatalogo

class Calca(ItemCatalogo):
    def __init__(self, nome, preco, descricao,categoria, tipo_modelagem):
        super().__init__(nome, preco, descricao, categoria)
        self.tipo_modelagem = tipo_modelagem