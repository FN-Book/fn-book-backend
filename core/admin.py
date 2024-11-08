from django.contrib import admin

from django.contrib import admin
from .models import Usuario, Noticia, AvaliacaoComentario, SolicitacaoContribuicao, LogAcao, MapaCalor

admin.site.register(Usuario)
admin.site.register(Noticia)
admin.site.register(AvaliacaoComentario)
admin.site.register(SolicitacaoContribuicao)
admin.site.register(LogAcao)
admin.site.register(MapaCalor)
