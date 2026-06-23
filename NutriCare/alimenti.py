from .models import AllergiaIntolleranza, Categoria_alimento, Alimento, Scatenare

# --------------------
# CREAZIONE CATEGORIE
# --------------------
carne = Categoria_alimento.objects.create(id_categoria="C01", nome="Carne")
pesce = Categoria_alimento.objects.create(id_categoria="C02", nome="Pesce")
verdura = Categoria_alimento.objects.create(id_categoria="C03", nome="Verdura")
frutta = Categoria_alimento.objects.create(id_categoria="C04", nome="Frutta")
latticini = Categoria_alimento.objects.create(id_categoria="C05", nome="Latticini")
cereali = Categoria_alimento.objects.create(id_categoria="C06", nome="Cereali")

# --------------------
# CARNE (10 alimenti)categoria
# --------------------
Alimento.objects.create(id_alimento="A001", nome="Petto di pollo", selezionabile=True,
    carboidrati=0, proteine=23, grassi=1.5, calorie=110, categoria=carne)

Alimento.objects.create(id_alimento="A002", nome="Manzo magro", selezionabile=True,
    carboidrati=0, proteine=21, grassi=5, calorie=150, categoria=carne)

Alimento.objects.create(id_alimento="A003", nome="Maiale", selezionabile=True,
    carboidrati=0, proteine=20, grassi=8, calorie=180, categoria=carne)

Alimento.objects.create(id_alimento="A004", nome="Agnello", selezionabile=True,
    carboidrati=0, proteine=19, grassi=9, calorie=200, categoria=carne)

Alimento.objects.create(id_alimento="A005", nome="Tacchino", selezionabile=True,
    carboidrati=0, proteine=24, grassi=2, calorie=120, categoria=carne)

Alimento.objects.create(id_alimento="A006", nome="Prosciutto crudo", selezionabile=True,
    carboidrati=0, proteine=25, grassi=15, calorie=250, categoria=carne)

Alimento.objects.create(id_alimento="A007", nome="Bresaola", selezionabile=True,
    carboidrati=0, proteine=32, grassi=2, calorie=160, categoria=carne)

Alimento.objects.create(id_alimento="A008", nome="Salsiccia", selezionabile=True,
    carboidrati=1, proteine=16, grassi=25, calorie=300, categoria=carne)

Alimento.objects.create(id_alimento="A009", nome="Hamburger", selezionabile=True,
    carboidrati=2, proteine=18, grassi=20, calorie=280, categoria=carne)

Alimento.objects.create(id_alimento="A010", nome="Speck", selezionabile=True,
    carboidrati=0, proteine=30, grassi=22, calorie=320, categoria=carne)


# --------------------
# PESCE (10 alimenti)
# --------------------
pesci = [
    ("A011", "Salmone", 0, 20, 13, 208),
    ("A012", "Tonno", 0, 23, 1, 110),
    ("A013", "Merluzzo", 0, 18, 1, 90),
    ("A014", "Orata", 0, 19, 5, 130),
    ("A015", "Sgombro", 0, 21, 12, 190),
    ("A016", "Spigola", 0, 20, 3, 120),
    ("A017", "Gamberi", 1, 24, 1, 105),
    ("A018", "Calamari", 3, 18, 2, 100),
    ("A019", "Polpo", 2, 17, 1, 90),
    ("A020", "Acciughe", 0, 22, 10, 200),
]

for id_a, nome, carb, prot, grassi, kcal in pesci:
    Alimento.objects.create(
        id_alimento=id_a,
        nome=nome,
        selezionabile=True,
        carboidrati=carb,
        proteine=prot,
        grassi=grassi,
        calorie=kcal,
        categoria=pesce
    )


# --------------------
# VERDURA (10 alimenti)
# --------------------
verdure = [
    ("A021", "Spinaci", 3, 3, 0.4, 23),
    ("A022", "Zucchine", 3, 2, 0.3, 20),
    ("A023", "Carote", 9, 1, 0.2, 40),
    ("A024", "Lattuga", 2, 1, 0.2, 15),
    ("A025", "Pomodori", 4, 1, 0.2, 18),
    ("A026", "Peperoni", 6, 1, 0.3, 25),
    ("A027", "Melanzane", 5, 1, 0.3, 25),
    ("A028", "Cetrioli", 3, 1, 0.1, 12),
    ("A029", "Broccoli", 6, 3, 0.4, 35),
    ("A030", "Cavolfiore", 5, 2, 0.3, 30),
]

for id_a, nome, carb, prot, grassi, kcal in verdure:
    Alimento.objects.create(
        id_alimento=id_a,
        nome=nome,
        selezionabile=True,
        carboidrati=carb,
        proteine=prot,
        grassi=grassi,
        calorie=kcal,
        categoria=verdura
    )


# --------------------
# FRUTTA (10 alimenti)
# --------------------
frutti = [
    ("A031", "Mela", 14, 0.3, 0.2, 52),
    ("A032", "Banana", 23, 1.1, 0.3, 89),
    ("A033", "Arancia", 12, 0.9, 0.1, 47),
    ("A034", "Pera", 15, 0.4, 0.1, 57),
    ("A035", "Uva", 18, 0.6, 0.2, 69),
    ("A036", "Fragole", 8, 0.7, 0.3, 32),
    ("A037", "Ananas", 13, 0.5, 0.1, 50),
    ("A038", "Kiwi", 15, 1.1, 0.5, 61),
    ("A039", "Pesca", 10, 0.9, 0.3, 39),
    ("A040", "Mango", 17, 0.8, 0.4, 60),
]

for id_a, nome, carb, prot, grassi, kcal in frutti:
    Alimento.objects.create(
        id_alimento=id_a,
        nome=nome,
        selezionabile=True,
        carboidrati=carb,
        proteine=prot,
        grassi=grassi,
        calorie=kcal,
        categoria=frutta
    )

latti = [
    ("A041", "Latte intero", 4.8, 3.3, 3.6, 64),
    ("A042", "Latte scremato", 5.0, 3.4, 0.1, 35),
    ("A043", "Yogurt bianco", 4.0, 4.0, 3.0, 60),
    ("A044", "Yogurt greco", 3.5, 9.0, 5.0, 95),
    ("A045", "Mozzarella", 1.0, 18.0, 17.0, 250),
    ("A046", "Parmigiano", 0.0, 33.0, 28.0, 390),
    ("A047", "Ricotta", 3.0, 11.0, 13.0, 174),
    ("A048", "Burro", 0.1, 0.5, 82.0, 740),
    ("A049", "Panna", 3.0, 2.0, 35.0, 340),
    ("A050", "Formaggio spalmabile", 2.5, 6.0, 25.0, 260),
]

# --------------------
# FOR LOOP
# --------------------
for id_a, nome, carb, prot, grassi, kcal in latti:
    Alimento.objects.create(
        id_alimento=id_a,
        nome=nome,
        selezionabile=True,
        carboidrati=carb,
        proteine=prot,
        grassi=grassi,
        calorie=kcal,
        categoria=latticini
    )

cere = [
    ("A051", "Pane integrale", 41.0, 8.0, 4.0, 247),
    ("A052", "Pane bianco", 49.0, 9.0, 3.2, 265),
    ("A053", "Pasta", 75.0, 13.0, 1.5, 360),
    ("A054", "Riso bianco", 80.0, 7.0, 0.7, 350),
    ("A055", "Riso integrale", 77.0, 7.5, 2.5, 340),
    ("A056", "Farro", 70.0, 15.0, 2.0, 340),
    ("A057", "Orzo", 73.0, 12.0, 1.5, 330),
    ("A058", "Mais", 74.0, 9.0, 4.0, 365),
    ("A059", "Cous cous", 77.0, 12.0, 1.0, 376),
    ("A060", "Cracker", 65.0, 10.0, 12.0, 420),
]

# --------------------
# FOR LOOP
# --------------------
for id_a, nome, carb, prot, grassi, kcal in cere:
    Alimento.objects.create(
        id_alimento=id_a,
        nome=nome,
        selezionabile=True,
        carboidrati=carb,
        proteine=prot,
        grassi=grassi,
        calorie=kcal,
        categoria=cereali
    )

lattosio = AllergiaIntolleranza.objects.create(
    id_allergia="ALL01",
    nome="Lattosio",
    descrizione="Intolleranza al latte e derivati"
)

glutine = AllergiaIntolleranza.objects.create(
    id_allergia="ALL02",
    nome="Glutine",
    descrizione="Reazione al glutine presente nei cereali"
)

crostacei = AllergiaIntolleranza.objects.create(
    id_allergia="ALL03",
    nome="Crostacei",
    descrizione="Allergia a gamberi, granchi e simili"
)

istamina = AllergiaIntolleranza.objects.create(
    id_allergia="ALL04",
    nome="Istamina",
    descrizione="Sensibilità a pesce conservato o fermentato"
)

Scatenare.objects.create(
    alimento=Alimento.objects.get(nome="Latte Intero"),
    allergia=lattosio
)

Scatenare.objects.create(
    alimento=Alimento.objects.get(nome="Formaggio spalmabile"),
    allergia=lattosio
)

Scatenare.objects.create(
    alimento=Alimento.objects.get(nome="Pane bianco"),
    allergia=glutine
)

Scatenare.objects.create(
    alimento=Alimento.objects.get(nome="Pasta"),
    allergia=glutine
)

Scatenare.objects.create(
    alimento=Alimento.objects.get(nome="Gamberi"),
    allergia=crostacei
)

Scatenare.objects.create(
    alimento=Alimento.objects.get(nome="Calamari"),
    allergia=crostacei
)

Scatenare.objects.create(
    alimento=Alimento.objects.get(nome="Sgombro"),
    allergia=istamina
)

Scatenare.objects.create(
    alimento=Alimento.objects.get(nome="Tonno"),
    allergia=istamina
)