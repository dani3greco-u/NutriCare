import json
from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Avg
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .forms import (
    GiornataFormSet,
    InclusioneFormSet,
    PastoFormSet,
    PianoForm,
    RecensioneForm,
    RilevazioneForm,
)

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
)

# UTIL

def controlla_abbonamento(paziente):
    return AbbonamentiAttivi.objects.filter(
        paziente=paziente,
        attivo=True,
        data_fine__gte=timezone.now().date()
    ).exists()


def effettua_pagamento(paziente, prezzo, abbonamento, partner, sconto_utilizzato):
    acquisto = Acquisti.objects.create(
        id_acquisto=f"ACQ{int(timezone.now().timestamp())}",
        data_acquisto=timezone.now().date(),
        prezzo_pagato=prezzo,
        metodo_pagamento="online",
        abbonamento=abbonamento,
        coppia=bool(partner),
        partner=partner,
        sconto_utilizzato=sconto_utilizzato
    )

    Effettuare.objects.create(
        paziente=paziente,
        acquisto=acquisto
    )

    abbonamento_vecchio = AbbonamentiAttivi.objects.filter(
        paziente=paziente,
        attivo=True,
    ).first()

    if abbonamento_vecchio:
        abbonamento_vecchio.attivo = False
        abbonamento_vecchio.save(update_fields=['attivo'])

    AbbonamentiAttivi.objects.create(
        paziente=paziente,
        abbonamento=abbonamento,
        data_inizio=timezone.now().date(),
        data_fine=timezone.now().date() + timedelta(days=abbonamento.durata),
        attivo=True
    )

# AUTH

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if Nutrizionisti.objects.filter(email=email, password=password).exists():
            request.session['email'] = email
            request.session['role'] = 'nutrizionista'
            return redirect('dashboard_nutrizionista')

        elif Pazienti.objects.filter(email=email, password=password).exists():
            request.session['email'] = email
            request.session['role'] = 'paziente'
            return redirect('dashboard_paziente')

        return render(request, 'login.html', {'error': 'Credenziali errate'})

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')

# DASHBOARD

def dashboard_nutrizionista(request):
    if request.session.get('role') != 'nutrizionista':
        return redirect('login')

    nutrizionista = get_object_or_404(Nutrizionisti, email=request.session['email'])

    pazienti = Pazienti.objects.filter(
        piani_alimentari__nutrizionista=nutrizionista,
        piani_alimentari__stato="Attivo"
    ).distinct()

    recensioni = Recensioni.objects.filter(
        nutrizionista=nutrizionista
    ).order_by('-data_inserimento')

    media_voti = recensioni.aggregate(Avg('stelle'))['stelle__avg']
    media_arrotondata = round(media_voti, 1) if media_voti else 0

    return render(request, 'dashboard_nutrizionista.html', {
        'pazienti': pazienti,
        'recensioni': recensioni,
        'nutrizionista': nutrizionista,
        'media_voti': media_voti
    })


def dashboard_paziente(request):
    if request.session.get('role') != 'paziente':
        return redirect('login')

    paziente = get_object_or_404(Pazienti, email=request.session['email'])

    piano = Piani_alimentari.objects.filter(
        paziente=paziente,
        stato='Attivo'
    ).first()

    rilevazioni = Rilevazioni.objects.filter(
        paziente=paziente
    ).order_by('data_rilevazione')

    abbonamento_attivo = AbbonamentiAttivi.objects.filter(
        paziente=paziente,
        attivo=True,
        data_fine__gte=timezone.now().date()
    ).first()

    date_lista = [r.data_rilevazione.strftime('%d/%m') for r in rilevazioni]
    pesi_lista = [float(r.peso) for r in rilevazioni]

    return render(request, 'dashboard_paziente.html', {
        'paziente': paziente,
        'rilevazioni': rilevazioni,
        'piano': piano,
        'date_json': json.dumps(date_lista),
        'pesi_json': json.dumps(pesi_lista),
        'abbonamento_attivo': abbonamento_attivo,
    })

# PAZIENTE / NUTRIZIONISTA

def dettaglio_paziente(request, email):
    if request.session.get('role') != 'nutrizionista':
        return redirect('login')

    paziente = get_object_or_404(Pazienti, email=email)
    nutrizionista = get_object_or_404(Nutrizionisti, email=request.session['email'])

    piano_attivo = Piani_alimentari.objects.filter(
        paziente=paziente,
        stato='Attivo',
        nutrizionista_id=nutrizionista
    ).first()

    rilevazioni = Rilevazioni.objects.filter(
        paziente=paziente
    ).order_by('data_rilevazione')

    date_lista = [r.data_rilevazione.strftime('%d/%m') for r in rilevazioni]
    pesi_lista = [float(r.peso) for r in rilevazioni]

    return render(request, 'dettaglio_paziente.html', {
        'paziente': paziente,
        'rilevazioni': rilevazioni,
        'piano_attivo': piano_attivo,
        'date_json': json.dumps(date_lista),
        'pesi_json': json.dumps(pesi_lista),
    })


def associa_paziente(request):
    if request.session.get('role') != 'nutrizionista':
        return redirect('login')

    nutrizionista = get_object_or_404(Nutrizionisti, email=request.session['email'])

    if request.method == 'POST':
        email = request.POST.get('email')
        paziente = Pazienti.objects.filter(email=email).first()

        if paziente:
            gia_associato = Piani_alimentari.objects.filter(
                paziente=paziente,
                nutrizionista=nutrizionista,
                stato='Attivo'
            ).exists()

            if not controlla_abbonamento(paziente):
                messages.error(request, "Il paziente non possiede un abbonamento attivo.")
                return redirect("associa_paziente")

            if not gia_associato:
                return redirect('crea_piano', email=paziente.email)

            messages.error(request, "Paziente già associato")
            return redirect("associa_paziente")

        messages.error(request, "Nessun paziente trovato con questa email.")
        return redirect("associa_paziente")

    return render(request, 'associa_paziente.html')

# RILEVAZIONI

def gestisci_rilevazioni(request, email):
    if request.session.get('role') != 'nutrizionista':
        return redirect('login')

    paziente = get_object_or_404(Pazienti, email=email)

    ultima_rilevazione = Rilevazioni.objects.filter(
        paziente=paziente
    ).order_by('-data_rilevazione').first()

    RilevazioneFormSet = modelformset_factory(
        Rilevazioni,
        form=RilevazioneForm,
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        formset = RilevazioneFormSet(
            request.POST,
            queryset=Rilevazioni.objects.filter(paziente=paziente)
        )

        if formset.is_valid():
            nuove = [
                f for f in formset
                if f.cleaned_data and not f.instance.pk and not f.cleaned_data.get('DELETE')
            ]

            if ultima_rilevazione and nuove:
                for f in nuove:
                    if f.cleaned_data.get('data_rilevazione') <= ultima_rilevazione.data_rilevazione:
                        formset.non_form_errors = [
                            f"Errore: La data deve essere successiva al {ultima_rilevazione.data_rilevazione}"
                        ]
                        return render(request, 'gestisci_rilevazioni.html', {
                            'formset': formset,
                            'paziente': paziente
                        })

            try:
                istanze = formset.save(commit=False)
                for i in istanze:
                    i.paziente = paziente
                    i.save()

                formset.save()
                messages.success(request, "Rilevazioni salvate con successo!")
                return redirect('gestisci_rilevazioni', email=email)

            except IntegrityError:
                formset.non_form_errors = ["Errore: Esiste già una rilevazione per questa data."]

    else:
        formset = RilevazioneFormSet(
            queryset=Rilevazioni.objects.filter(paziente=paziente).order_by('data_rilevazione')
        )

    return render(request, 'gestisci_rilevazioni.html', {
        'formset': formset,
        'paziente': paziente
    })

# PIANO ALIMENTARE

def gestisci_piano(request, email, pk):
    if request.session.get('role') != 'nutrizionista':
        return redirect('login')

    paziente = get_object_or_404(Pazienti, email=email)
    piano = get_object_or_404(Piani_alimentari, pk=pk, paziente=paziente)

    nutrizionista_session = get_object_or_404(
        Nutrizionisti,
        email=request.session['email']
    )

    is_readonly = (
        piano.stato == 'Archiviato'
        or piano.nutrizionista != nutrizionista_session
    )

    if request.method == 'POST':
        formset = GiornataFormSet(request.POST, instance=piano)

        if not controlla_abbonamento(paziente):
            messages.error(request, "Il paziente non possiede un abbonamento attivo.")
            return redirect("gestisci_piano", email=email, pk=pk)

        if formset.is_valid():
            istanze = formset.save(commit=False)
            conta = piano.giornate.count()

            for i, istanza in enumerate(istanze):
                if not istanza.n_giorno:
                    istanza.n_giorno = f"Giorno {conta + i + 1}"

            formset.save()
            messages.success(request, "Giornate aggiornate con successo!")
            return redirect('gestisci_piano', email=email, pk=pk)

        messages.error(request, "Errore: Controlla i dati inseriti.")

    else:
        formset = GiornataFormSet(instance=piano)

    return render(request, 'gestisci_piano.html', {
        'formset': formset,
        'paziente': paziente,
        'piano': piano,
        'is_readonly': is_readonly
    })

# PASTI / ALIMENTI

def gestisci_pasti(request, giornata_id):
    giornata = get_object_or_404(Giornate_tipo, pk=giornata_id)
    piano = giornata.piano
    is_readonly = (piano.stato == 'Archiviato')

    if request.method == 'POST':
        formset = PastoFormSet(request.POST, instance=giornata)

        if not controlla_abbonamento(piano.paziente):
            messages.error(request, "Il paziente non possiede un abbonamento attivo.")
            return redirect("gestisci_pasti", giornata_id=giornata.pk)

        if formset.is_valid():
            pasti = formset.save()

            for pasto in pasti:
                macro = pasto.calcola_macro()
                pasto.calorie_totali = macro['calorie']
                pasto.proteine_totali = macro['proteine']
                pasto.carboidrati_totali = macro['carboidrati']
                pasto.grassi_totali = macro['grassi']
                pasto.save()

            return redirect('gestisci_pasti', giornata_id=giornata.pk)

        messages.error(request, "Errore: Inserisci tutti i campi correttamente.")

    else:
        formset = PastoFormSet(instance=giornata)

    tot = {'calorie': 0, 'proteine': 0, 'carboidrati': 0, 'grassi': 0}

    for f in formset:
        if f.instance.pk:
            f.macro = f.instance.calcola_macro()
        else:
            f.macro = tot.copy()

        for k in tot:
            tot[k] += f.macro[k]

    rimanenti = giornata.calorie_target - tot['calorie']

    return render(request, 'gestisci_pasti.html', {
        'formset': formset,
        'giornata': giornata,
        'totali': tot,
        'rimanenti': rimanenti,
        'is_readonly': is_readonly
    })


def gestisci_alimenti(request, pasto_id):
    pasto = get_object_or_404(Pasti, pk=pasto_id)
    giornata = pasto.giornata
    piano = giornata.piano
    is_readonly = (piano.stato == 'Archiviato')
    paziente = piano.paziente

    if request.method == 'POST':
        formset = InclusioneFormSet(request.POST, instance=pasto)

        if not controlla_abbonamento(piano.paziente):
            messages.error(request, "Il paziente non possiede un abbonamento attivo.")
            return redirect("gestisci_alimenti", pasto_id=pasto.pk)

        if formset.is_valid():
            formset.save()

            macro = pasto.calcola_macro()
            pasto.calorie_totali = macro['calorie']
            pasto.proteine_totali = macro['proteine']
            pasto.carboidrati_totali = macro['carboidrati']
            pasto.grassi_totali = macro['grassi']
            pasto.save()

            messages.success(request, "Alimenti aggiornati!")
            return redirect('gestisci_alimenti', pasto_id=pasto.pk)

        messages.error(request, "Errore inserimento dati.")

    else:
        formset = InclusioneFormSet(instance=pasto)

        allergie = paziente.allergie.all()

        formset.form.base_fields['alimento'].queryset = Alimenti.objects.filter(
            selezionabile=True
        ).exclude(
            scatenare__allergia__in=allergie
        )

    return render(request, 'gestisci_alimenti.html', {
        'formset': formset,
        'pasto': pasto,
        'is_readonly': is_readonly,
    })

# PIANI / VISUALIZZAZIONE

def crea_piano(request, email):
    if request.session.get('role') != 'nutrizionista':
        return redirect('login')

    paziente = get_object_or_404(Pazienti, email=email)

    storico = Piani_alimentari.objects.filter(
        paziente=paziente
    ).order_by('id_piano_alimentare')

    if request.method == 'POST':
        form = PianoForm(request.POST)

        if form.is_valid():
            vecchio = Piani_alimentari.objects.filter(
                paziente=paziente,
                stato='Attivo'
            ).first()

            data_inizio = form.cleaned_data['data_inizio']

            if vecchio and data_inizio <= vecchio.data_inizio:
                messages.error(request, f"Il nuovo piano deve essere successivo al {vecchio.data_inizio}")
                return redirect('crea_piano', email=email)

            nuovo = form.save(commit=False)
            nuovo.paziente = paziente
            nuovo.nutrizionista = Nutrizionisti.objects.get(email=request.session['email'])
            nuovo.stato = 'Attivo'
            nuovo.save()

            if vecchio:
                vecchio.stato = 'Archiviato'
                vecchio.data_fine = nuovo.data_inizio
                vecchio.save()

            return redirect('gestisci_piano', email=email, pk=nuovo.pk)

    else:
        form = PianoForm()

    return render(request, 'crea_piano.html', {
        'form': form,
        'paziente': paziente,
        'storico': storico
    })


def visualizza_piano(request, pk):
    piano = get_object_or_404(Piani_alimentari, pk=pk)

    if request.session.get('role') == 'paziente' and piano.paziente.email != request.session.get('email'):
        return redirect('dashboard_paziente')

    return render(request, 'visualizza_piano.html', {'piano': piano})


def visualizza_storico(request):
    if request.session.get('role') == 'paziente':
        paziente = get_object_or_404(Pazienti, email=request.session['email'])
    else:
        return redirect('dashboard_nutrizionista')

    return render(request, 'storico_paziente.html', {
        'piani': Piani_alimentari.objects.filter(paziente=paziente).order_by('-data_inizio'),
        'rilevazioni': Rilevazioni.objects.filter(paziente=paziente).order_by('-data_rilevazione'),
        'acquisti': Acquisti.objects.filter(effettuare__paziente=paziente).distinct()
    })

# RECENSIONI

def scrivi_recensione(request):
    if request.session.get('role') != 'paziente':
        return redirect('login')

    paziente = get_object_or_404(Pazienti, email=request.session['email'])
    piano = Piani_alimentari.objects.filter(paziente=paziente, stato='Attivo').first()

    recensioni = Recensioni.objects.filter(paziente=paziente)

    nutrizionista = piano.nutrizionista if piano else None

    gia = Recensioni.objects.filter(paziente=paziente, nutrizionista=nutrizionista).exists()

    if request.method == 'POST' and piano and not gia:
        form = RecensioneForm(request.POST)

        if form.is_valid():
            r = form.save(commit=False)
            r.paziente = paziente
            r.nutrizionista = nutrizionista
            r.save()
            return redirect('scrivi_recensione')
    else:
        form = RecensioneForm()

    return render(request, 'scrivi_recensione.html', {
        'piano': piano,
        'form': form,
        'gia_recensito': gia,
        'recensioni': recensioni,
        'nutrizionista': nutrizionista,
    })

# ABBONAMENTI

def acquista_abbonamento(request, id_abbonamento):
    paziente = get_object_or_404(Pazienti, email=request.session['email'])
    abbonamento = get_object_or_404(Abbonamenti, pk=id_abbonamento)

    attivo = AbbonamentiAttivi.objects.filter(
        paziente=paziente,
        attivo=True,
        data_fine__gte=timezone.now().date()
    ).first()

    if attivo:
        messages.error(request, "Hai già un abbonamento attivo")
        return redirect("abbonamenti")

    listino = Listini_prezzi.objects.filter(
        abbonamento=abbonamento,
        data_fine_validita__isnull=True
    ).first()

    sconto = Acquisti.objects.filter(
        partner=paziente,
        sconto_utilizzato=False
    ).first()

    if sconto:
        prezzo = listino.prezzo * Decimal(0.8)
        effettua_pagamento(paziente, prezzo, abbonamento, None, False)
        sconto.sconto_utilizzato = True
        sconto.save(update_fields=['sconto_utilizzato'])
        return redirect("abbonamenti")

    partner_id = request.GET.get("partner_id")

    if partner_id:
        flag = False

        acquisti = Acquisti.objects.filter(effettuare__paziente=paziente).distinct()
        for a in acquisti:
            if a.partner and a.partner.email == partner_id:
                flag = True

        acquisti_partner = Acquisti.objects.filter(effettuare__paziente=partner_id).distinct()
        for a in acquisti_partner:
            if a.partner and a.partner.email == paziente.email:
                flag = True

        if flag:
            messages.error(request, f"Hai gia usato lo sconto con {partner_id}")
            return redirect("abbonamenti")

        partner = Pazienti.objects.filter(email=partner_id).first()
        effettua_pagamento(paziente, listino.prezzo, abbonamento, partner, False)
        return redirect("abbonamenti")

    effettua_pagamento(paziente, listino.prezzo, abbonamento, None, False)
    return redirect("abbonamenti")


def lista_abbonamenti(request):
    paziente = get_object_or_404(Pazienti, email=request.session['email'])

    attivo = AbbonamentiAttivi.objects.filter(
        paziente=paziente,
        attivo=True,
        data_fine__gte=timezone.now().date()
    ).first()

    sconto = Acquisti.objects.filter(
        partner=paziente,
        sconto_utilizzato=False
    ).first()

    if sconto:
        persona = Effettuare.objects.filter(acquisto=sconto.id_acquisto).first()
        messages.success(request, f"Hai diritto a uno sconto (link con {persona.paziente.email})")

    return render(request, "abbonamenti.html", {
        "abbonamenti": Abbonamenti.objects.all(),
        "abbonamento_attivo": attivo,
        "acquisto_scontato": sconto
    })

# API

def trova_alternative(request, id_alimento, pasto_id):
    alimento = get_object_or_404(Alimenti, pk=id_alimento)
    pasto = get_object_or_404(Pasti, pk=pasto_id)

    calorie = alimento.calorie

    allergie = pasto.giornata.piano.paziente.allergie.all()

    alternative = Alimenti.objects.filter(
        categoria=alimento.categoria,
        selezionabile=True
    ).exclude(id_alimento=id_alimento).exclude(
        scatenare__allergia__in=allergie
    )[:10]

    data = []

    for a in alternative:
        grammi = (calorie / a.calorie) * 100

        data.append({
            "id": a.id_alimento,
            "nome": a.nome,
            "calorie": float(a.calorie),
            "grammi": round(grammi, 1)
        })

    return JsonResponse({"alternative": data})


def utente_by_email(request):
    email = request.GET.get("email")

    paziente = Pazienti.objects.filter(email=email).first()

    if not paziente:
        return JsonResponse({"success": False})

    return JsonResponse({
        "success": True,
        "email": paziente.email,
        "nome": paziente.nome
    })