from models.item_catalogo.acessorios import Acessorios
from models.item_catalogo.blusas import Blusas
from models.item_catalogo.calcas import Calcas
from models.item_catalogo.camisas import Camisas
from models.item_catalogo.tenis import Tenis

from models.catalogo import Catalogo


tenis_bape01 = Tenis("Bape Sneaker", 799.99, "Tenis branco da bape", "Tenis", "plataforma")
camisa1 = Camisas("Nike Air T-shirt", 159.99, "Camisa com caracteristica única de núvens", "Camisas", "Quadrada")

catalogo = Catalogo()

Catalogo.adicionar_roupa(catalogo, tenis_bape01)
Catalogo.adicionar_roupa(catalogo, camisa1)
# catalogo.listar_roupas()

catalogo.listar_info_produtos(tenis_bape01)
catalogo.listar_info_produtos(camisa1)