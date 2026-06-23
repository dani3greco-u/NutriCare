from django.contrib import admin

from .models import (
    Abbonamenti,
    AbbonamentiAttivi,
    Acquisti,
    Alimenti,
    Effettuare,
    Giornate_tipo,
    Listini_prezzi,
    Pasti,
    Pazienti,
    Nutrizionisti,
    Piani_alimentari,
    Recensioni,
    Rilevazioni,
    Scatenare,
    Inclusione,
    Categorie_alimenti,
    AllergieIntolleranze
)


admin.site.register(Abbonamenti)
admin.site.register(AbbonamentiAttivi)
admin.site.register(Acquisti)
admin.site.register(Alimenti)
admin.site.register(Giornate_tipo)
admin.site.register(Listini_prezzi)
admin.site.register(Pasti)
admin.site.register(Nutrizionisti)
admin.site.register(Piani_alimentari)
admin.site.register(Recensioni)
admin.site.register(Rilevazioni)
admin.site.register(Scatenare)
admin.site.register(Inclusione)
admin.site.register(Effettuare)
admin.site.register(Categorie_alimenti)
admin.site.register(AllergieIntolleranze)

@admin.register(Pazienti)
class PazienteAdmin(admin.ModelAdmin):
    filter_horizontal = ('allergie',) 
    list_display = ('nome', 'cognome', 'email')