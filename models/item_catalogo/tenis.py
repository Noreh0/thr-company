from models.item_catalogo.itemCatalogo import ItemCatalogo

class Tenis(ItemCatalogo):
    def __init__(self, nome, preco, descricao,categoria, tipo_sola):
        super().__init__(nome, preco, descricao, categoria)
        self.tipo_sola = tipo_sola
    def __str__(self):
        return f"{self.nome} - {self.preco} - {self.descricao} - {self.tipo_sola} - {self.categoria}"