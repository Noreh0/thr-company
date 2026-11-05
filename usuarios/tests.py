from django.test import TestCase
from django.urls import reverse

from usuarios.models import Usuario

DADOS = {
    'nome': 'Maria Souza', 'email': 'Maria@Exemplo.com', 'telefone': '(41) 98888-7777',
    'password1': 'senha-forte-123', 'password2': 'senha-forte-123',
}


class CadastroTests(TestCase):
    def test_cadastro_cria_usuario_loga_e_normaliza_dados(self):
        r = self.client.post(reverse('usuarios:cadastro'), DADOS)
        self.assertRedirects(r, reverse('produtos:home'))
        u = Usuario.objects.get()
        self.assertEqual((u.email, u.username, u.first_name, u.telefone),
                         ('maria@exemplo.com', 'maria@exemplo.com', 'Maria Souza', '41988887777'))
        self.assertFalse(u.is_staff)
        self.assertNotEqual(u.password, 'senha-forte-123')  # guardada com hash
        self.assertEqual(self.client.session['_auth_user_id'], str(u.pk))

    def test_email_repetido_e_recusado_sem_diferenciar_maiusculas(self):
        self.client.post(reverse('usuarios:cadastro'), DADOS)
        self.client.logout()
        r = self.client.post(reverse('usuarios:cadastro'), {**DADOS, 'email': 'MARIA@exemplo.com'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Já existe uma conta')
        self.assertEqual(Usuario.objects.count(), 1)

    def test_telefone_invalido_e_recusado(self):
        r = self.client.post(reverse('usuarios:cadastro'), {**DADOS, 'telefone': '123'})
        self.assertContains(r, 'Informe o DDD')
        self.assertEqual(Usuario.objects.count(), 0)

    def test_telefone_com_55_e_aceito(self):
        self.client.post(reverse('usuarios:cadastro'), {**DADOS, 'telefone': '+55 41 98888-7777'})
        self.assertEqual(Usuario.objects.get().telefone, '41988887777')

    def test_cadastro_nao_redireciona_para_site_externo(self):
        r = self.client.post(reverse('usuarios:cadastro') + '?next=https://malicioso.com', DADOS)
        self.assertRedirects(r, reverse('produtos:home'))

    def test_login_e_logout(self):
        self.client.post(reverse('usuarios:cadastro'), DADOS)
        self.client.post(reverse('usuarios:logout'))
        self.assertNotIn('_auth_user_id', self.client.session)
        r = self.client.post(reverse('usuarios:login'), {'username': 'maria@exemplo.com', 'password': 'senha-forte-123'})
        self.assertRedirects(r, reverse('produtos:home'))

    def test_login_com_senha_errada_mostra_erro(self):
        self.client.post(reverse('usuarios:cadastro'), DADOS)
        self.client.logout()
        r = self.client.post(reverse('usuarios:login'), {'username': 'maria@exemplo.com', 'password': 'errada'})
        self.assertContains(r, 'role="alert"')
