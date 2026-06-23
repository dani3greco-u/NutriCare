import random
from datetime import date, timedelta
from django.utils import timezone
# Sostituisci 'tuapp' con il nome reale della tua app Django
from NutriCare.models import (
    Nutrizionista, Paziente, Abbonamento, Acquisto, 
    Effettuare, Recensione, Rilevazione, Piano_alimentare,
    Giornata_tipo, Pasto, Inclusione, Alimento
)

print("🚀 Inizio popolamento dati di test...")

# 1. Recuperiamo gli alimenti e gli abbonamenti esistenti
alimenti = list(Alimento.objects.all())
abbonamenti = list(Abbonamento.objects.all())

if not alimenti or not abbonamenti:
    print("❌ Errore: Devi avere almeno un alimento e un abbonamento nel DB prima di avviare lo script.")
    exit()

# 2. Creazione Nutrizionisti
nutrizionisti = []
specializzazioni = ["Nutrizione Sportiva", "Dimagrimento", "Dietoterapia", "Nutrizione Clinica"]
for i in range(1, 6):
    n = Nutrizionista.objects.create(
        email=f"nutrizionista{i}@test.com",
        cf=f"XYZNTR00A01F205{i}",
        nome=f"Dottor{i}",
        cognome=f"Rossi{i}",
        password="pbkdf2_sha256$...fakesecret...",
        sesso=random.choice(["M", "F"]),
        eta=random.randint(30, 60),
        n_albo=f"ALBO-{1000+i}",
        specializzazione=random.choice(specializzazioni),
        stato=1
    )
    nutrizionisti.append(n)

pazienti = []
for i in range(1, 36):
    p = Paziente.objects.create(
        email=f"paziente{i}@test.com",
        cf=f"XYZPZN00A01F20{i}",
        nome=f"Paziente{i}",
        cognome=f"Bianchi{i}",
        password="pbkdf2_sha256$...fakesecret...",
        sesso=random.choice(["M", "F"]),
        eta=random.randint(18, 70),
        note_cliniche="Nessuna nota particolare."
    )
    pazienti.append(p)

paziente_target = pazienti[0]
peso_iniziale = 85.0
for settimane in range(5):
    data_ril = date.today() - timedelta(weeks=(4 - settimane))
    Rilevazione.objects.create(
        paziente=paziente_target,
        data_rilevazione=data_ril,
        altezza=175.00,
        peso=peso_iniziale - (settimane * 1.2), # Peso che scende
        perc_massa_grassa=24.0 - (settimane * 0.5),
        commento=f"Controllo settimana {settimane}"
    )

nutrizionista_basso = nutrizionisti[0]
for i in range(12):
    Recensione.objects.create(
        stelle=1,
        commento="Poco professionale ed empatico.",
        paziente=pazienti[i],
        nutrizionista=nutrizionista_basso
    )

for i in range(12, 30):
    Recensione.objects.create(
        stelle=random.choice([4, 5]),
        commento="Ottimo professionista, molto consigliato!",
        paziente=pazienti[i],
        nutrizionista=random.choice(nutrizionisti[1:])
    )

alimento_star = random.choice(alimenti)

for idx, p in enumerate(pazienti):
    # Assegniamo quasi tutti i pazienti a nutrizionisti[1] per fargli superare la soglia dei 30 pazienti seguiti
    nutr = nutrizionisti[1] if idx < 32 else random.choice(nutrizionisti[2:])
    
    piano = Piano_alimentare.objects.create(
        data_inizio=date.today(),
        stato="attivo",
        obiettivo="Dimagrimento",
        paziente=p,
        nutrizionista=nutr
    )
    
    giornata = Giornata_tipo.objects.create(n_giorno="Lunedì", calorie_target=1800, piano=piano)
    pasto = Pasto.objects.create(nome="Pranzo", orario_consigliato="13:00:00", giornata=giornata)
    
    # Prescriviamo l'alimento star a tutti
    Inclusione.objects.create(grammatura=150.00, pasto=pasto, alimento=alimento_star)
    
    # E un secondo alimento a caso
    alimento_caso = random.choice(alimenti)
    if alimento_caso != alimento_star:
        Inclusione.objects.create(grammatura=100.00, pasto=pasto, alimento=alimento_caso)