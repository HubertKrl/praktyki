# forms.py
from django import forms
from .models import Szyba, Ramka, Glassone, Glasstwo, Glassthree


class PakietForm(forms.Form):
    PAKIET_CHOICES = (
        ('glassone', 'Pakiet Jednoszybowy'),
        ('glasstwo', 'Pakiet Dwuszybowy'),
        ('glassthree', 'Pakiet Trzyszybowy'),
    )

    szyba1 = forms.ModelChoiceField(queryset=Szyba.objects.all(), label="Wybierz Szybę 1")
    ramka1 = forms.ModelChoiceField(queryset=Ramka.objects.all(), label="Wybierz Ramkę 1", required=False)
    szyba2 = forms.ModelChoiceField(queryset=Szyba.objects.all(), label="Wybierz Szybę 2", required=False)
    ramka2 = forms.ModelChoiceField(queryset=Ramka.objects.all(), label="Wybierz Ramkę 2", required=False)
    szyba3 = forms.ModelChoiceField(queryset=Szyba.objects.all(), label="Wybierz Szybę 3", required=False)

    def __init__(self, *args, **kwargs):
        pakiet_type = kwargs.pop('pakiet_type', None)
        super().__init__(*args, **kwargs)

        if pakiet_type == 'glassone':
            self.fields['ramka1'].required = False
            self.fields['szyba2'].required = False
            self.fields['ramka2'].required = False
            self.fields['szyba3'].required = False
        elif pakiet_type == 'glasstwo':
            self.fields['ramka1'].required = True
            self.fields['szyba2'].required = True
            self.fields['ramka2'].required = False
            self.fields['szyba3'].required = False
        elif pakiet_type == 'glassthree':
            self.fields['ramka1'].required = True
            self.fields['szyba2'].required = True
            self.fields['ramka2'].required = True
            self.fields['szyba3'].required = True

    def clean(self):
        cleaned_data = super().clean()
        pakiet_type = cleaned_data.get("pakiet_type")

        if pakiet_type == 'glassone':
            if not cleaned_data.get("szyba1"):
                raise forms.ValidationError("Wybierz szyba1")
        elif pakiet_type == 'glasstwo':
            if not cleaned_data.get("szyba1") or not cleaned_data.get("ramka1") or not cleaned_data.get("szyba2"):
                raise forms.ValidationError("Wszystkie pola dla pakietu dwuszybowego są wymagane.")
        elif pakiet_type == 'glassthree':
            if not cleaned_data.get("szyba1") or not cleaned_data.get("ramka1") or not cleaned_data.get(
                    "szyba2") or not cleaned_data.get("ramka2") or not cleaned_data.get("szyba3"):
                raise forms.ValidationError("Wszystkie pola dla pakietu trzyszybowego są wymagane.")

        return cleaned_data

from django import forms

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(label="Wybierz plik CSV")