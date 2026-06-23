from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class AllergieIntolleranze(models.Model):
    id_allergia = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=30)
    descrizione = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Allergie e intolleranze"

    def __str__(self):
        return self.nome

class Nutrizionisti(models.Model):
    email = models.EmailField(primary_key=True, max_length=100)
    cf = models.CharField(max_length=16)
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    sesso = models.CharField(max_length=1)
    eta = models.IntegerField()
    n_albo = models.CharField(max_length=20)
    specializzazione = models.CharField(max_length=100)
    stato = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Nutrizionisti"

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.email})"

class Pazienti(models.Model):
    email = models.EmailField(primary_key=True, max_length=100)
    cf = models.CharField(max_length=16)
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    sesso = models.CharField(max_length=1)
    eta = models.IntegerField()
    note_cliniche = models.TextField(blank=True, null=True)

    allergie = models.ManyToManyField(AllergieIntolleranze, blank=True)

    class Meta:
        verbose_name_plural = "Pazienti"

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.email})"

class Piani_alimentari(models.Model):
    id_piano_alimentare = models.AutoField(primary_key=True)
    data_inizio = models.DateField()
    data_fine = models.DateField(null=True, blank=True)
    stato = models.CharField(max_length=20)
    obiettivo = models.CharField(max_length=100)
    
    paziente = models.ForeignKey(Pazienti, on_delete=models.CASCADE)
    nutrizionista = models.ForeignKey(Nutrizionisti, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Piani alimentari"

    def __str__(self):
        return f"Piano {self.id_piano_alimentare} - {self.paziente.nome} {self.paziente.cognome}"
    
class Categorie_alimenti(models.Model):
    id_categoria = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Categorie alimenti"

    def __str__(self):
        return self.nome

class Alimenti(models.Model):
    id_alimento = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=50)
    selezionabile = models.BooleanField()
    carboidrati = models.DecimalField(max_digits=5, decimal_places=2)
    proteine = models.DecimalField(max_digits=5, decimal_places=2)
    grassi = models.DecimalField(max_digits=5, decimal_places=2)
    calorie = models.DecimalField(max_digits=6, decimal_places=2)
    restrizioni = models.CharField(max_length=100, blank=True, null=True)

    categoria = models.ForeignKey(Categorie_alimenti, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Alimenti"
    
    def __str__(self):
        return self.nome


class Giornate_tipo(models.Model):
    n_giorno = models.CharField(max_length=20, blank=True)
    calorie_target = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.CharField(max_length=255, blank=True, null=True)


    piano = models.ForeignKey(Piani_alimentari, on_delete=models.CASCADE, related_name="giornate")
    
    class Meta:
        unique_together = ('piano', 'n_giorno')
        verbose_name_plural = "Giornate tipo"
    
    def __str__(self):
        return f"Giornata {self.n_giorno} - {self.calorie_target} kcal"

class Pasti(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    orario_consigliato = models.TimeField()
    calorie_totali = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    proteine_totali = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    carboidrati_totali = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    grassi_totali = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    
    giornata = models.ForeignKey(Giornate_tipo, on_delete=models.CASCADE, related_name="pasti")

    class Meta:
            ordering = ['orario_consigliato']
            verbose_name_plural = "Pasti"

    def calcola_macro(self):
        from django.db.models import Sum, F
        
        totali = self.inclusioni.aggregate(
            calorie=Sum(F('alimento__calorie') * F('grammatura') / 100),
            proteine=Sum(F('alimento__proteine') * F('grammatura') / 100),
            carboidrati=Sum(F('alimento__carboidrati') * F('grammatura') / 100),
            grassi=Sum(F('alimento__grassi') * F('grammatura') / 100)
        )
        
        # Se il pasto è vuoto, i valori saranno None
        return {
            'calorie': totali['calorie'] or 0,
            'proteine': totali['proteine'] or 0,
            'carboidrati': totali['carboidrati'] or 0,
            'grassi': totali['grassi'] or 0
        }
    
    def __str__(self):
        return self.nome

class Inclusione(models.Model):
    grammatura = models.DecimalField(max_digits=6, decimal_places=2)

    pasto = models.ForeignKey(Pasti, on_delete=models.CASCADE , related_name="inclusioni")
    alimento = models.ForeignKey(Alimenti, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.pasto.nome} - {self.alimento.nome}"

    class Meta:
        unique_together = ('pasto', 'alimento')
    verbose_name_plural = "Inclusioni"

class Abbonamenti(models.Model):
    id_abbonamento = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=50)
    descrizione = models.CharField(max_length=255, blank=True, null=True)
    durata = models.IntegerField()

    class Meta:
        verbose_name_plural = "Abbonamenti"

class AbbonamentiAttivi(models.Model):
    data_inizio = models.DateField(auto_now_add=True)
    data_fine = models.DateField()
    attivo = models.BooleanField(default=True)

    paziente = models.ForeignKey("Pazienti", on_delete=models.CASCADE)
    abbonamento = models.ForeignKey(Abbonamenti, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Abbonamenti attivi"

    def __str__(self):
        return f"{self.paziente} - {self.abbonamento}"

class Acquisti(models.Model):
    id_acquisto = models.CharField(primary_key=True, max_length=20)
    data_acquisto = models.DateField()
    prezzo_pagato = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pagamento = models.CharField(max_length=50)
    note = models.CharField(max_length=255, blank=True, null=True)
    coppia = models.BooleanField(default=False)
    sconto_utilizzato = models.BooleanField(default=False)

    abbonamento = models.ForeignKey(Abbonamenti, on_delete=models.CASCADE)
    partner = models.ForeignKey(Pazienti, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Acquisti"

class Listini_prezzi(models.Model):
    id_listino_prezzo = models.CharField(max_length=10) 
    prezzo = models.DecimalField(max_digits=10, decimal_places=2)
    data_inizio_validita = models.DateField()
    data_fine_validita = models.DateField(null=True, blank=True)

    abbonamento = models.ForeignKey(Abbonamenti, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('abbonamento', 'data_inizio_validita')
        verbose_name_plural = "Listini prezzi"

    def __str__(self):
        return f"{self.abbonamento.nome} - {self.prezzo}€ (dal {self.data_inizio_validita})"
    
class Rilevazioni(models.Model):
    paziente = models.ForeignKey(Pazienti, on_delete=models.CASCADE)
    data_rilevazione = models.DateField()
    altezza = models.DecimalField(max_digits=5, decimal_places=2)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    perc_massa_grassa = models.DecimalField(max_digits=5, decimal_places=2)
    commento = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('paziente', 'data_rilevazione')
        ordering = ['-data_rilevazione']
        verbose_name_plural = "Rilevazioni"

    def __str__(self):
        return f"Rilevazione {self.data_rilevazione} - {self.paziente.nome} {self.paziente.cognome}"

class Recensioni(models.Model):
    data_inserimento = models.DateTimeField(auto_now_add=True)
    stelle = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    commento = models.CharField(max_length=500)
    paziente = models.ForeignKey(Pazienti, on_delete=models.CASCADE)
    nutrizionista = models.ForeignKey(Nutrizionisti, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('paziente', 'nutrizionista')
        verbose_name_plural = "Recensioni"

    def __str__(self):
        return f"Recensione di {self.paziente.cognome} - {self.nutrizionista.cognome} "

class Scatenare(models.Model):
    alimento = models.ForeignKey(Alimenti, on_delete=models.CASCADE)
    allergia = models.ForeignKey(AllergieIntolleranze, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('alimento', 'allergia')
        verbose_name_plural = "alimento-allergia"
    
    def __str__(self):
        return f"{self.alimento.nome} scatenante per {self.allergia.nome}"

class Effettuare(models.Model):
    paziente = models.ForeignKey(Pazienti, on_delete=models.CASCADE)
    acquisto = models.ForeignKey(Acquisti, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('paziente', 'acquisto')
        verbose_name_plural = "Effettuazioni acquisti"
