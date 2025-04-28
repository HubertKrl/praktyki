from rest_framework import serializers
from .models import Ramka, Szyba, Glassone, Glasstwo, Glassthree

class RamkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ramka
        fields = ['id', 'nazwa', 'grubosc']


class SzybaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Szyba
        fields = ['id', 'nazwa', 'grubosc'  ]


class GlassoneSerializer(serializers.ModelSerializer):
    szyba1 = SzybaSerializer()

    class Meta:
        model = Glassone
        fields = ['id', 'szyba1']


class GlasstwoSerializer(serializers.ModelSerializer):
    szyba1 = SzybaSerializer()
    ramka1 = RamkaSerializer()
    szyba2 = SzybaSerializer()

    class Meta:
        model = Glasstwo
        fields = ['id', 'szyba1', 'ramka1', 'szyba2']


class GlassthreeSerializer(serializers.ModelSerializer):
    szyba1 = SzybaSerializer()
    ramka1 = RamkaSerializer()
    szyba2 = SzybaSerializer()
    ramka2 = RamkaSerializer()
    szyba3 = SzybaSerializer()
    grubosc_calkowita = serializers.SerializerMethodField()
    class Meta:
        model = Glassthree
        fields = ['id','szyba1','ramka1','szyba2','ramka2','szyba3','grubosc_calkowita','gfactor','ufactor','rw']

    def get_grubosc_calkowita(self, obj):
        # Jeżeli w modelu masz np. metodę lub property `grubosc_calkowita`
        # Możesz tu dokonać wszelkich obliczeń lub po prostu zwrócić wartość
        return obj.grubosc_calkowita