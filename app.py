from models.item_catalogo.acessorios import Acessorios
from models.item_catalogo.blusas import Blusas
from models.item_catalogo.calcas import Calca
from models.item_catalogo.camisas import Camisas
from models.item_catalogo.tenis import Tenis

from models.catalogo import Catalogo


tenis_bape01 = Tenis("Bape Sneaker", 799.99, "Tenis branco da bape", "Tenis", "plataforma")

catalogo = Catalogo()

Catalogo.adicionar_roupa(catalogo, tenis_bape01)
catalogo.listar_roupas()