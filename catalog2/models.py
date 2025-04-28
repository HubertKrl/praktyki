from django.db import models
from django import forms
from django.db import models
from django.utils import timezone

class AccessKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Data, po której klucz traci ważność (opcjonalnie)")

    def __str__(self):
        return self.key

    def is_valid(self):
        """
        Metoda pomocnicza sprawdzająca, czy klucz jest aktywny i (jeśli ustawione) nie wygasł.
        """
        if not self.active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True

class Ramka(models.Model):
    nazwa = models.CharField(max_length=500)
    grubosc = models.DecimalField(decimal_places=2, max_digits=5)

    class Meta:
        verbose_name = "ramka"
        verbose_name_plural = "ramki"

    def __str__(self):
        return f"{self.nazwa}, {self.grubosc}"


class Szyba(models.Model):
    nazwa = models.CharField(max_length=500)
    grubosc = models.DecimalField(decimal_places=2, max_digits=5)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    class Meta:
        verbose_name = "szyba"
        verbose_name_plural = "szyby"

    def __str__(self):
        return f"{self.nazwa}, {self.grubosc}   "

class Szybaform(forms.ModelForm):
    class Meta:
        model=Szyba
        fields=["image"]

class wlasciwosci(models.Model):
    ufactor=models.DecimalField(decimal_places=2, max_digits=5)
    gfactor=models.DecimalField(decimal_places=2, max_digits=5)
    rw=models.DecimalField(decimal_places=2, max_digits=5)
    class Meta:
        abstract=True

class Glassone(wlasciwosci):
    szyba1 = models.ForeignKey(Szyba, on_delete=models.CASCADE, unique=True)

    class Meta:

        verbose_name = "pakiet jednoszybowy"
        verbose_name_plural = "pakiety jednoszybowe"

    def __str__(self):
        return f"Glassone: {self.szyba1}"


class Glasstwo(wlasciwosci):
    szyba1 = models.ForeignKey(Szyba, on_delete=models.CASCADE, related_name='glasstwo_szyba1_set')
    ramka1 = models.ForeignKey(Ramka, on_delete=models.CASCADE, related_name='glasstwo_ramka1_set')
    szyba2 = models.ForeignKey(Szyba, on_delete=models.CASCADE, related_name='glasstwo_szyba2_set')

    class Meta:

        verbose_name = "pakiet dwuszybowy"
        verbose_name_plural = "pakiety dwuszybowe"
        constraints = [
            models.UniqueConstraint(fields=['szyba1', 'ramka1', 'szyba2'], name='unique_glasstwo_combination')
        ]

    def grubosc_calkowita(self):
        return float(self.szyba1.grubosc + self.szyba2.grubosc + self.ramka1.grubosc)

    def __str__(self):
        grubosc = self.grubosc_calkowita()
        return f"Glasstwo: {self.szyba1}, {self.ramka1}, {self.szyba2}, {grubosc}"


class Glassthree(wlasciwosci):
    szyba1 = models.ForeignKey(Szyba, on_delete=models.CASCADE, related_name='glassthree_szyba1_set')
    ramka1 = models.ForeignKey(Ramka, on_delete=models.CASCADE, related_name='glassthree_ramka1_set')
    szyba2 = models.ForeignKey(Szyba, on_delete=models.CASCADE, related_name='glassthree_szyba2_set')
    ramka2 = models.ForeignKey(Ramka, on_delete=models.CASCADE, related_name='glassthree_ramka2_set')
    szyba3 = models.ForeignKey(Szyba, on_delete=models.CASCADE, related_name='glassthree_szyba3_set')

    class Meta:

        verbose_name = "pakiet trzyszybowy"
        verbose_name_plural = "pakiety trzyszybowe"
        constraints = [
            models.UniqueConstraint(fields=['szyba1', 'ramka1', 'szyba2', 'ramka2', 'szyba3'], name='unique_glassthree_combination')
        ]
    @property
    def grubosc_calkowita(self):
        return float(self.szyba1.grubosc + self.szyba2.grubosc + self.szyba3.grubosc + self.ramka1.grubosc + self.ramka2.grubosc)

    def __str__(self):
        return f"Glassthree: {self.szyba1}, {self.ramka1}, {self.szyba2}, {self.ramka2}, {self.szyba3}"


