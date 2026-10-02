class Usuario:
    def __init__(self, nome, email, senha_hash):
        self.nome = nome
        self.email = email
        self._senha_hash = senha_hash

    def __str__(self):
        return f"Nome: {self.nome}"