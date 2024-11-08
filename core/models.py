from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo para o usuário, agora com campos adicionais e usando o sistema de senha seguro do Django
class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('pesquisador', 'Pesquisador'),
        ('administrador', 'Administrador'),
        ('contribuidor', 'Contribuidor'),
        ('usuario simples', 'Usuário simples'),
    ]
    
    regiao_ddd = models.CharField(max_length=5)
    data_atualizacao = models.DateTimeField(auto_now=True)  # Data da última atualização
    score = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    quantidade_contribuicoes = models.IntegerField(default=0)

    def __str__(self):
        return self.username

# Modelo para a tabela de notícias, com campo para imagem e data de modificação
class Noticia(models.Model):
    STATUS_CHOICES = [
        ('verdade', 'Verdade'),
        ('fake', 'Fake'),
    ]
    
    titulo = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='noticias_fotos/', null=True, blank=True)  # Usando ImageField para upload
    texto = models.TextField()
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
    contribuidor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)  # Data da última modificação
    alteracoes_sugeridas = models.JSONField(default=list)

    def __str__(self):
        return self.titulo

# Modelo para avaliações e comentários, com avaliação em estrelas
class AvaliacaoComentario(models.Model):
    TIPO_AVALIACAO_CHOICES = [
        ('gostei', 'Gostei'),
        ('nao gostei', 'Não gostei'),
        ('neutro', 'Neutro'),
    ]
    
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_avaliacao = models.CharField(max_length=20, choices=TIPO_AVALIACAO_CHOICES)
    comentario = models.TextField()
    avaliacao_estrela = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)  # Avaliação em estrelas (1 a 5)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.usuario.username} sobre {self.noticia.titulo}"

# Modelo para solicitações de contribuição, com descrição adicional e notificação de status
class SolicitacaoContribuicao(models.Model):
    STATUS_SOLICITACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status_solicitacao = models.CharField(max_length=10, choices=STATUS_SOLICITACAO_CHOICES)
    descricao = models.TextField(null=True, blank=True)  # Descrição adicional da solicitação
    notificado = models.BooleanField(default=False)  # Se o usuário foi notificado sobre o status

    def __str__(self):
        return f"Solicitação de {self.usuario.username} - Status: {self.status_solicitacao}"

# Modelo para logs de ações, com tipo de ação e referência ao objeto alterado
class LogAcao(models.Model):
    TIPO_ACAO_CHOICES = [
        ('criação', 'Criação'),
        ('edição', 'Edição'),
        ('exclusão', 'Exclusão'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    tipo_acao = models.CharField(max_length=10, choices=TIPO_ACAO_CHOICES)  # Tipo da ação
    data_acao = models.DateTimeField(auto_now_add=True)
    detalhes_acao = models.TextField()
    objeto_alterado = models.CharField(max_length=255, null=True, blank=True)  # Referência ao objeto alterado (e.g., nome da notícia)

    def __str__(self):
        return f"Ação {self.acao} realizada por {self.usuario.username}"

# Modelo para o mapa de calor, com tipo de interação
class MapaCalor(models.Model):
    INTERACAO_CHOICES = [
        ('visualizacao', 'Visualização'),
        ('comentario', 'Comentário'),
    ]
    
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    data_interacao = models.DateTimeField(auto_now_add=True)
    regiao_ddd = models.CharField(max_length=5)
    quantidade_interacoes = models.IntegerField(default=0)
    tipo_interacao = models.CharField(max_length=20, choices=INTERACAO_CHOICES, default='visualizacao')

    def __str__(self):
        return f"Mapa de Calor para {self.noticia.titulo} - Região: {self.regiao_ddd}"
