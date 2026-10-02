from models.item_catalogo.itemCatalogo import ItemCatalogo

class Catalogo:
    def __init__(self):
        self._roupas = []

    def adicionar_roupa(self, item):
        if isinstance(item, ItemCatalogo):
            self._roupas.append(item)
        else:
            return "O item não é uma roupa ou acessório!"
    