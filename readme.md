# NutriCare

Applicazione web sviluppata con Django per la gestione di pazienti, nutrizionisti e piani alimentari.

## Requisiti

Prima di eseguire il progetto è necessario avere installato:

* Python 3.13
* MySQL Server
* pip
* Git (opzionale, per clonare il repository)

## Installazione

### 1. Clonare il repository

```bash
git clone <repository-url>
cd NutriCareProject
```

### 2. Creare e attivare l'ambiente virtuale

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

## Configurazione del database

Il progetto utilizza un database MySQL denominato `NutriCare`.

**Importante:

Il server MySQL deve essere in esecuzione.
Il database NutriCare deve essere già presente sulla macchina prima dell'avvio dell'applicazione.

Se necessario, è possibile crearlo con:

```sql
CREATE DATABASE NutriCare;
```

Le credenziali di accesso al database sono configurabili nel file:

```text
config/settings.py
```

## Inizializzazione del database

Applicare le migration di Django:

```bash
python manage.py migrate
```

## Creazione del superuser

Per accedere all'area di amministrazione di Django è necessario creare un superuser:

```bash
python manage.py createsuperuser
```

Seguire le istruzioni mostrate nel terminale per inserire username, email e password.

## Avvio dell'applicazione

Avviare il server di sviluppo:

```bash
python manage.py runserver
```

L'applicazione sarà disponibile all'indirizzo:

```text
http://127.0.0.1:8000/
```

L'area di amministrazione di Django è disponibile all'indirizzo:

```text
http://127.0.0.1:8000/admin/
```

## Account

* **Amministratore:** creato tramite il comando `python manage.py createsuperuser`.
* **Pazienti:** da inserire manualmente dalla schermata admin.
* **Nutrizionisti:** da inserire dalla schermata admin.

Il login per gli utenti sarà disponibile all'indirizzo:

```text
http://127.0.0.1:8000/
```

Inserire le credenziali di un paziente o un nutrizionista



## Struttura del progetto

```text
NutriCareProject/
│
├── config/                 # Configurazione del progetto Django
├── NutriCare/              # Applicazione principale
├── NutriCare/templates/    # Template HTML
├── NutriCare/static/       # File statici 
├── NutriCare/migrations/   # Migration del database
└── manage.py               # Entry point del progetto
```

