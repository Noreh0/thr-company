from decimal import Decimal
from urllib.parse import parse_qs, urlparse

from django.test import TestCase
from django.urls import reverse

from pedidos.models import Pedido
from produtos.models import Categoria, Produto, Variacao
from usuarios.models import Usuario


class FluxoDeCompraTests(TestCase):
    def setUp(self):
        categoria = Categoria.objects.create(nome='Tênis')
        self.produto = Produto.objects.create(
            categoria=categoria, nome='Tênis Cano Baixo', descricao='x', preco=Decimal('599.90'))
        self.v42 = Variacao.objects.create(produto=self.produto, tamanho='42', estoque=3)
        self.v43 = Variacao.objects.create(produto=self.produto, tamanho='43', estoque=0)
        self.usuario = Usuario.objects.create_user(
            'maria@x.com', 'maria@x.com', 'senha-forte-123', first_name='Maria', telefone='41988887777')

    def adicionar(self, variacao, quantidade=1):
        return self.client.post(reverse('carrinho:adicionar'), {'variacao': variacao.id, 'quantidade': quantidade})

    # ----- catálogo aberto a todos
    def test_catalogo_nao_exige_login(self):
        self.assertEqual(self.client.get(reverse('produtos:home')).status_code, 200)
        self.assertContains(self.client.get(reverse('produtos:lista')), 'Tênis Cano Baixo')
        self.assertContains(self.client.get(self.produto_url()), 'Adicionar ao carrinho')

    def produto_url(self):
        return reverse('produtos:detalhe', args=[self.produto.slug])

    def test_filtro_por_categoria_e_busca(self):
        outra = Categoria.objects.create(nome='Bonés')
        Produto.objects.create(categoria=outra, nome='Boné Preto', descricao='x', preco=10)
        r = self.client.get(reverse('produtos:lista'), {'categoria': outra.slug})
        self.assertContains(r, 'Boné Preto')
        self.assertNotContains(r, 'Tênis Cano Baixo')
        r = self.client.get(reverse('produtos:lista'), {'q': 'cano'})
        self.assertContains(r, 'Tênis Cano Baixo')
        self.assertNotContains(r, 'Boné Preto')

    def test_produto_inativo_some_do_catalogo(self):
        self.produto.ativo = False
        self.produto.save()
        self.assertEqual(self.client.get(self.produto_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse('produtos:lista')), 'Tênis Cano Baixo')

    # ----- carrinho sem login
    def test_carrinho_funciona_sem_login(self):
        r = self.adicionar(self.v42, 2)
        self.assertRedirects(r, reverse('carrinho:ver'))
        r = self.client.get(reverse('carrinho:ver'))
        self.assertContains(r, 'Tênis Cano Baixo')
        self.assertContains(r, '1.199,80')

    def test_nao_adiciona_tamanho_esgotado(self):
        self.adicionar(self.v43)
        self.assertNotContains(self.client.get(reverse('carrinho:ver')), 'Tênis Cano Baixo')

    def test_quantidade_limitada_ao_estoque(self):
        self.adicionar(self.v42, 10)
        self.assertEqual(self.client.session['carrinho'][str(self.v42.id)], 3)

    def test_sem_tamanho_escolhido_mostra_erro(self):
        r = self.client.post(reverse('carrinho:adicionar'), {'quantidade': 1}, follow=True)
        self.assertContains(r, 'Escolha um tamanho')

    def test_atualizar_e_remover(self):
        self.adicionar(self.v42, 1)
        self.client.post(reverse('carrinho:atualizar'), {'variacao': self.v42.id, 'quantidade': 2})
        self.assertEqual(self.client.session['carrinho'][str(self.v42.id)], 2)
        self.client.post(reverse('carrinho:remover'), {'variacao': self.v42.id})
        self.assertEqual(self.client.session['carrinho'], {})

    def test_preco_vem_do_banco_nao_do_navegador(self):
        self.client.post(reverse('carrinho:adicionar'), {'variacao': self.v42.id, 'quantidade': 1, 'preco': '0.01'})
        self.assertContains(self.client.get(reverse('carrinho:ver')), '599,90')

    # ----- checkout exige login
    def test_checkout_exige_login_e_volta_depois(self):
        self.adicionar(self.v42)
        r = self.client.get(reverse('pedidos:checkout'))
        self.assertRedirects(r, f"{reverse('usuarios:login')}?next={reverse('pedidos:checkout')}")

    def test_login_retorna_ao_checkout(self):
        self.adicionar(self.v42)
        r = self.client.post(
            f"{reverse('usuarios:login')}?next={reverse('pedidos:checkout')}",
            {'username': 'MARIA@x.com', 'password': 'senha-forte-123', 'next': reverse('pedidos:checkout')})
        self.assertRedirects(r, reverse('pedidos:checkout'))

    def test_checkout_com_carrinho_vazio_volta_ao_carrinho(self):
        self.client.force_login(self.usuario)
        self.assertRedirects(self.client.get(reverse('pedidos:checkout')), reverse('carrinho:ver'))

    def test_checkout_cria_pedido_baixa_estoque_e_vai_ao_whatsapp(self):
        self.client.force_login(self.usuario)
        self.adicionar(self.v42, 2)
        r = self.client.post(reverse('pedidos:checkout'))

        pedido = Pedido.objects.get()
        self.assertEqual(pedido.usuario, self.usuario)
        self.assertEqual(pedido.status, Pedido.Status.AGUARDANDO)
        self.assertEqual(pedido.total, Decimal('1199.80'))
        item = pedido.itens.get()
        self.assertEqual((item.nome, item.tamanho, item.quantidade, item.preco_unitario),
                         ('Tênis Cano Baixo', '42', 2, Decimal('599.90')))
        self.v42.refresh_from_db()
        self.assertEqual(self.v42.estoque, 1)
        self.assertEqual(self.client.session['carrinho'], {})

        self.assertEqual(r.status_code, 302)
        url = urlparse(r.url)
        self.assertEqual((url.scheme, url.netloc, url.path), ('https', 'wa.me', '/5541999999999'))
        texto = parse_qs(url.query)['text'][0]
        self.assertIn(f'pedido #{pedido.pk}', texto)
        self.assertIn('Maria - (41) 98888-7777', texto)
        self.assertIn('2x Tênis Cano Baixo (42) - R$ 599,90', texto)
        self.assertIn('Total: R$ 1.199,80', texto)

    def test_historico_do_pedido_nao_muda_com_novo_preco(self):
        self.client.force_login(self.usuario)
        self.adicionar(self.v42, 1)
        self.client.post(reverse('pedidos:checkout'))
        self.produto.preco = Decimal('1.00')
        self.produto.save()
        self.assertEqual(Pedido.objects.get().itens.get().preco_unitario, Decimal('599.90'))

    def test_estoque_acabou_entre_carrinho_e_pedido(self):
        self.client.force_login(self.usuario)
        self.adicionar(self.v42, 3)
        Variacao.objects.filter(pk=self.v42.pk).update(estoque=1)  # outro cliente comprou
        r = self.client.post(reverse('pedidos:checkout'), follow=True)
        # carrinho foi ajustado para 1 unidade (o que existe) e o pedido sai com 1
        pedido = Pedido.objects.get()
        self.assertEqual(pedido.itens.get().quantidade, 1)

    def test_meus_pedidos_mostra_so_os_do_proprio_usuario(self):
        outro = Usuario.objects.create_user('joao@x.com', 'joao@x.com', 'senha-forte-123', telefone='41977776666')
        Pedido.objects.create(usuario=outro, total=5)
        self.client.force_login(self.usuario)
        self.adicionar(self.v42)
        self.client.post(reverse('pedidos:checkout'))
        r = self.client.get(reverse('pedidos:meus'))
        self.assertContains(r, 'Pedido #')
        self.assertEqual(len(r.context['pedidos']), 1)
        self.assertContains(r, 'wa.me')

    def test_meus_pedidos_exige_login(self):
        self.assertEqual(self.client.get(reverse('pedidos:meus')).status_code, 302)

    # ----- admin
    def test_cancelar_no_admin_devolve_estoque_uma_vez(self):
        self.client.force_login(self.usuario)
        self.adicionar(self.v42, 2)
        self.client.post(reverse('pedidos:checkout'))
        pedido = Pedido.objects.get()
        self.client.logout()

        admin = Usuario.objects.create_superuser('adm', 'adm@x.com', 'senha-forte-123', telefone='41900000000')
        self.client.force_login(admin)
        url = reverse('admin:pedidos_pedido_change', args=[pedido.pk])
        dados = {'status': 'cancelado', 'observacao': '',
                 'itens-TOTAL_FORMS': 0, 'itens-INITIAL_FORMS': 0, 'itens-MIN_NUM_FORMS': 0, 'itens-MAX_NUM_FORMS': 1000}
        self.assertEqual(self.client.post(url, dados).status_code, 302)
        self.v42.refresh_from_db()
        self.assertEqual(self.v42.estoque, 3)  # 3 - 2 + 2

        self.client.post(url, {**dados, 'status': 'pago'})
        self.client.post(url, dados)  # cancela de novo
        self.v42.refresh_from_db()
        self.assertEqual(self.v42.estoque, 3)  # não devolve duas vezes

    def test_admin_lista_pedidos(self):
        admin = Usuario.objects.create_superuser('adm', 'adm@x.com', 'senha-forte-123', telefone='41900000000')
        Pedido.objects.create(usuario=self.usuario, total=10)
        self.client.force_login(admin)
        r = self.client.get(reverse('admin:pedidos_pedido_changelist'))
        self.assertContains(r, 'wa.me/5541988887777')
