class Usuario:
    def __init__(self, nome, email, telefone, senha_hash, is_admin = False):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self._senha_hash = senha_hash
        self.is_admin = is_admin
        self._carrinho = []

    def __str__(self):
        return f"Nome: {self.nome}"

    def adicionar_produto_ao_carrinho(self, item):
        self._carrinho.append(item)
        