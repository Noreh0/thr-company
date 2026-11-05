from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['nome']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')
    nome = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    # Atributos específicos por categoria (tipo_sola, tipo_manga, material...)
    atributos = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-criado_em']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


class Variacao(models.Model):
    """Tamanho/cor + estoque. Um produto tem várias variações."""

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='variacoes')
    tamanho = models.CharField(max_length=20)
    cor = models.CharField(max_length=50, blank=True)
    estoque = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['produto', 'tamanho', 'cor'], name='variacao_unica'),
        ]

    def __str__(self):
        return f"{self.produto.nome} ({self.tamanho} {self.cor})".strip()
