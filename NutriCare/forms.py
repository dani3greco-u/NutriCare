# NutriCare/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Alimenti, Giornate_tipo, Inclusione, Pasti, Pazienti, Piani_alimentari, Recensioni, Rilevazioni
from django.db import models

class PianoForm(forms.ModelForm):
    class Meta:
        model = Piani_alimentari
        fields = [ 'data_inizio', 'obiettivo']
        widgets = {
            'data_inizio': forms.DateInput(attrs={'type': 'date'}),
        }

class RilevazioneForm(forms.ModelForm):
    class Meta:
        model = Rilevazioni
        fields = ['data_rilevazione', 'peso', 'altezza', 'perc_massa_grassa', 'commento']
        widgets = {
            'data_rilevazione': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'altezza': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'perc_massa_grassa': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
            'commento': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PazienteForm(forms.ModelForm):
    class Meta:
        model = Pazienti
        fields = ['nome', 'cognome', 'email', 'sesso', 'cf', 'password', 'eta', 'note_cliniche']
        widgets = {
            'password': forms.PasswordInput(),
            'note_cliniche': forms.Textarea(attrs={'rows': 3}),
        }

class PastoForm(forms.ModelForm):
    class Meta:
        model = Pasti
        fields = ['nome', 'orario_consigliato', 'calorie_totali']
        widgets = {
            'orario_consigliato': forms.TimeInput(attrs={'type': 'time'}),
        }

class InclusioneForm(forms.ModelForm):
    alimento = forms.ModelChoiceField(
        queryset=Alimenti.objects.filter(selezionabile=True),
        empty_label="Seleziona alimento..."
    )
    class Meta:
        model = Inclusione
        fields = ['alimento', 'grammatura']

class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensioni
        fields = ['stelle', 'commento']
        widgets = {
            'commento': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Scrivi qui la tua opinione...'}),
            'stelle': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '5'}),
        }


InclusioneFormSet = inlineformset_factory(
    Pasti, 
    Inclusione, 
    form=InclusioneForm, 
    extra=0, 
    can_delete=True)

PastoFormSet = inlineformset_factory(
    Giornate_tipo, 
    Pasti, 
    form=PastoForm, 
    extra=0, 
    can_delete=True
)

GiornataFormSet = inlineformset_factory(
    Piani_alimentari,
    Giornate_tipo,
    fields=('n_giorno', 'calorie_target', 'note'),
    extra=0,
    can_delete=True
)


