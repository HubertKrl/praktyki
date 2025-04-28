from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

from .models import Glassone, Glasstwo, Glassthree,Szybaform,Szyba,Ramka
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.views.generic import ListView
class index(LoginRequiredMixin,TemplateView):
    template_name = 'catalog2/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pakiet1'] = Glassone.objects.all()
        context['pakiet2'] = Glasstwo.objects.all()
        context['pakiet3'] = Glassthree.objects.all()
        return context
#def index(request):
#    pakiet1=Glassone.objects.all()
#    pakiet2=Glasstwo.objects.all()
#    pakiet3=Glassthree.objects.all()

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import HttpResponseForbidden
from .models import AccessKey

from django.http import HttpResponseForbidden
from .models import AccessKey

from django.http import HttpResponseForbidden
from .models import AccessKey

class TokenRequiredMixin:
    """
    Mixin, który sprawdza, czy w nagłówku HTTP lub w parametrze URL
    znajduje się poprawny klucz dostępu. Jeśli klucz nie istnieje, jest
    nieprawidłowy lub wygasł, użytkownik otrzyma odpowiedź 403 Forbidden.
    """
    def dispatch(self, request, *args, **kwargs):
        # Najpierw próba odczytania z nagłówka
        access_key = request.META.get('HTTP_X_ACCESS_KEY')
        # Jeśli nie znaleziono w nagłówkach, spróbuj pobrać z parametrów GET
        if not access_key:
            access_key = request.GET.get('access_key')
        if not access_key:
            return HttpResponseForbidden("Brak klucza dostępu.")
        try:
            ak = AccessKey.objects.get(key=access_key)
        except AccessKey.DoesNotExist:
            return HttpResponseForbidden("Nieprawidłowy klucz dostępu.")
        if not ak.is_valid():
            return HttpResponseForbidden("Klucz dostępu wygasł lub jest nieaktywny.")
        return super().dispatch(request, *args, **kwargs)
#    return render(request, 'catalog2/index.html', {'pakiet1': pakiet1 ,'pakiet2' :pakiet2 ,'pakiet3' : pakiet3})
class pakiet_jednoszybowy(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = 'catalog2/pakiet_jednoszybowy.html'
    permission_required = 'catalog2.view_glassone'

    login_url = '/login/'

    def handle_no_permission(self):
        # Jeśli użytkownik nie ma dostępu, zamiast błędu wyświetlamy stronę z komunikatem
        return render(self.request, 'catalog2/no_access.html', status=403)
    def dispatch(self, request, *args, **kwargs):

        request.session['model_type'] = 'glassone'
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pakiet1'] = Glassone.objects.all()
        context['szyba'] =Szyba.objects.all()
        context['ramka'] = Ramka.objects.all()
        return context
#def pakiet_jednoszybowy(request):
#    pakiet1 = Glassone.objects.all()

#    return render(request,'catalog2/pakiet_jednoszybowy.html',{'pakiet1':pakiet1})

class pakiet_dwuszybowy(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = 'catalog2/pakiet_dwuszybowy.html'
    permission_required = 'catalog2.view_glasstwo'
    login_url = '/login/'

    def handle_no_permission(self):
        # Jeśli użytkownik nie ma dostępu, zamiast błędu wyświetlamy stronę z komunikatem
        return render(self.request, 'catalog2/no_access.html', status=403)
    def dispatch(self, request, *args, **kwargs):
        # Ustawienie zmiennej w sesji na podstawie modelu
        request.session['model_type'] = 'glasstwo'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pakiet2'] = Glasstwo.objects.all()
        context['szyba'] =Szyba.objects.all()
        context['ramka'] = Ramka.objects.all()
        return context
#def pakiet_dwuszybowy(request):
#    pakiet2 = Glasstwo.objects.all()
#
#    return render(request, 'catalog2/pakiet_dwuszybowy.html', {'pakiet2': pakiet2})


class pakiet_trzyszybowy(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = 'catalog2/pakiet_trzyszybowy.html'
    permission_required = 'catalog2.view_glassthree'
    login_url = '/login/'

    def handle_no_permission(self):
        # Jeśli użytkownik nie ma dostępu, zamiast błędu wyświetlamy stronę z komunikatem
        return render(self.request, 'catalog2/no_access.html', status=403)
    def dispatch(self, request, *args, **kwargs):
        # Ustawienie zmiennej w sesji na podstawie modelu
        request.session['model_type'] = 'glassthree'
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pakiet3'] = Glassthree.objects.all()
        context['szyba'] =Szyba.objects.all()
        context['ramka'] = Ramka.objects.all()

        return context
#def pakiet_trzyszybowy(request):
#    pakiet3 = Glassthree.objects.all()
#
#    return render(request, 'catalog2/pakiet_trzyszybowy.html', {'pakiet3': pakiet3})



class Szyby(LoginRequiredMixin,TemplateView):
    template_name = 'catalog2/szyby.html'

    def dispatch(self, request, *args, **kwargs):
        # Ustawienie zmiennej w sesji na podstawie modelu
        request.session['model_type'] = 'szyby'
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['szyby'] = Szyba.objects.all()
        return context

class Ramki(LoginRequiredMixin, TemplateView):
        template_name = 'catalog2/ramki.html'

        def dispatch(self, request, *args, **kwargs):
            # Ustawienie zmiennej w sesji na podstawie modelu
            request.session['model_type'] = 'ramki'
            return super().dispatch(request, *args, **kwargs)
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['ramki'] = Ramka.objects.all()
            return context


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa


def render_pdf(request):
    model_type = request.session.get('model_type')


    if model_type == 'glassone':
        szyba_data = Glassone.objects.all()
        html = render_to_string('pdfg1.html', {'szyba_data': szyba_data})
    elif model_type == 'glasstwo':
        szyba_data = Glasstwo.objects.all()
        html = render_to_string('pdfg2.html', {'szyba_data': szyba_data})
    elif model_type == 'glassthree':
        szyba_data = Glassthree.objects.all()
        html = render_to_string('pdfg3.html', {'szyba_data': szyba_data})
    elif model_type=='szyby':
        szyba_data=Szyba.objects.all()
        for szyba in szyba_data:
            if szyba.image:
                szyba.image_url = request.build_absolute_uri(szyba.image.url)
            else:
                szyba.image_url = None  # Jeśli brak obrazu, ustawiamy na None
        html = render_to_string('pdfs.html', {'szyba_data': szyba_data})

    elif model_type == 'ramki':
        szyba_data = Szyba.objects.all()
        html = render_to_string('pdfr.html', {'szyba_data': szyba_data})
    else:
        szyba_data = []
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="document.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Błąd podczas generowania PDF')
    return response


#class ProduktListView(ListView):
#    model = Glassthree
#    template_name = 'catalog2/pakiet_trzyszybowy.html'
#    paginate_by = 10
#    def get_queryset(self):
#        # Zastosowanie porządku do zapytania
#        return Glassthree.objects.all().order_by('-szyba1')
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['pakiet3']=Glassthree.objects.all()
#        return context

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ramka, Szyba, Glassone, Glasstwo, Glassthree
from .serializers import RamkaSerializer, SzybaSerializer, GlassoneSerializer, GlasstwoSerializer, GlassthreeSerializer

class RamkaAPIView(TokenRequiredMixin ,APIView):
    template_name = 'katalog/protected_data.html'
    def get(self, request):
        ramki = Ramka.objects.all()
        serializer = RamkaSerializer(ramki, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RamkaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SzybaAPIView(TokenRequiredMixin ,APIView):
    template_name = 'katalog/protected_data.html'
    def get(self, request):
        szyby = Szyba.objects.all()
        serializer = SzybaSerializer(szyby, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SzybaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Pakiet_jednoszybowyAPIView(APIView):
    def get(self, request):
        glassone = Glassone.objects.all()
        serializer = GlassoneSerializer(glassone, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GlassoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.decorators import permission_required
class Pakiet_dwuszybowyAPIView(APIView):
    def get(self, request):
        glasstwo = Glasstwo.objects.all()
        serializer = GlasstwoSerializer(glasstwo, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GlasstwoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Glassthree  # Upewnij się, że to właściwy model dla pakietów
import json


class delete_pakiet1(PermissionRequiredMixin, View):
    # Ustaw wymagane uprawnienie – pamiętaj, by podać je zgodnie z modelem:
    permission_required = 'catalog2.delete_glassone'
    raise_exception = True  # Spowoduje podniesienie wyjątku PermissionDenied, jeśli uprawnienie nie zostanie spełnione

    def delete(self, request, *args, **kwargs):
        # Próbujemy pobrać ID z query string
        pakiet_id = request.GET.get('id')

        # Jeśli nie ma go w parametrach URL, spróbuj pobrać z JSON w ciele zapytania
        if not pakiet_id:
            try:
                data = json.loads(request.body)
                pakiet_id = data.get('id')
            except Exception:
                pass

        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glassone.objects.get(pk=pakiet_id)
            pakiet.delete()
            return JsonResponse({'success': True})
        except Glassone.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['DELETE'])

class delete_pakiet2(PermissionRequiredMixin, View):
    # Ustawienie wymaganego uprawnienia – zmień 'moja_aplikacja' na nazwę swojej aplikacji
    permission_required = 'catalog2.delete_glasstwo'
    raise_exception = True  # Jeśli użytkownik nie ma uprawnień, zostanie zwrócony błąd 403

    def delete(self, request, *args, **kwargs):
        # Próbujemy pobrać ID z parametrów zapytania (query string)
        pakiet_id = request.GET.get('id')

        # Jeśli nie ma go w query, spróbuj pobrać z body jako JSON
        if not pakiet_id:
            try:
                data = json.loads(request.body)
                pakiet_id = data.get('id')
            except Exception:
                pass

        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glasstwo.objects.get(pk=pakiet_id)
            pakiet.delete()
            return JsonResponse({'success': True})
        except Glasstwo.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['DELETE'])

class delete_pakiet3(PermissionRequiredMixin, View):
    # Ustaw wymagane uprawnienie – zamień 'moja_aplikacja' na nazwę swojej aplikacji
    permission_required = 'catalog2.delete_glassthree'
    raise_exception = True  # Użytkownik bez uprawnień otrzyma błąd 403

    def delete(self, request, *args, **kwargs):
        # Próba pobrania ID z parametrów zapytania (query string)
        pakiet_id = request.GET.get('id')

        # Jeśli ID nie występuje w query, próbujemy odczytać je z ciała zapytania (JSON)
        if not pakiet_id:
            try:
                data = json.loads(request.body)
                pakiet_id = data.get('id')
            except Exception:
                pass

        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glassthree.objects.get(pk=pakiet_id)
            pakiet.delete()
            return JsonResponse({'success': True})
        except Glassthree.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['DELETE'])

class Pakiet_trzyszybowyAPIView(APIView):
    def delete_pakiet(request):
        if request.method == 'DELETE':
            pakiet_id = request.GET.get('id')
            if not pakiet_id:
                return JsonResponse({'error': 'Nie podano id.'}, status=400)
            try:
                # Zakładamy, że model nazywa się PakietTrzyszybowy
                pakiet = Glassthree.objects.get(pk=pakiet_id)
                pakiet.delete()
                return JsonResponse({'success': True})
            except Glassthree.DoesNotExist:
                return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)
        return HttpResponseNotAllowed(['DELETE'])
    def get(self, request):
        paginator=PageNumberPagination()
        paginator.page_size =10
        glassthree = Glassthree.objects.all()
        paginated_posts = paginator.paginate_queryset(glassthree, request)
        serializer = GlassthreeSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = GlassthreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render, redirect
from .forms import PakietForm
from .models import Glassone, Glasstwo, Glassthree


# views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
import logging
from .forms import PakietForm

def create_pakiet(request):


    # Pobieramy dane z bazy, jeśli potrzebujemy
    szyby = Szyba.objects.all()
    ramki = Ramka.objects.all()

    if request.method == 'GET':
        # Zapisywanie URL referera do sesji, jeśli jest dostępny
        previous_url = request.META.get('HTTP_REFERER', '/')
        request.session['previous_url'] = previous_url

        # Ustawienie pakiet_type w formularzu


    elif request.method == 'POST':
        previous_url = request.META.get('HTTP_REFERER', '/')
        request.session['previous_url'] = previous_url
        form = PakietForm(request.POST)
        if not form.is_valid():
            print("Błędy formularza:", form.errors)  # Lub użyj loggera
            # Możesz też zwrócić komunikaty do szablonu dla testów
        else:
            # Przetwarzanie formularza...
            pass
        if form.is_valid():
            try:
                # Pobieranie danych z formularza
                szyba1 = form.cleaned_data['szyba1']
                ramka1 = form.cleaned_data['ramka1']
                szyba2 = form.cleaned_data['szyba2']
                ramka2 = form.cleaned_data['ramka2']
                szyba3 = form.cleaned_data['szyba3']

                logger = logging.getLogger(__name__)
                # Przygotowanie treści e-maila z danymi z formularza
                subject = 'Dane z formularza pakietu trzyszybowego'
                message = (
                    f"Szyba 1: {szyba1}\n"
                    f"Ramka 1: {ramka1}\n"
                    f"Szyba 2: {szyba2}\n"
                    f"Ramka 2: {ramka2}\n"
                    f"Szyba 3: {szyba3}\n"
                )
                from_email = 'noreply@example.com'
                recipient_list = ['admin@example.com']

                # Wysyłka e-maila.
                # Jeśli ustawisz EMAIL_BACKEND na konsolowy w settings.py,
                # wiadomość zostanie wyświetlona w konsoli\
                logger.info(f"Wysyłam e-mail: {message}")
                print(f"Wysyłam e-mail: {message}")
                send_mail(subject, message, from_email, recipient_list)
                return redirect(previous_url)




            except Exception as e:
                form.add_error(None, f"Wystąpił błąd podczas zapisywania pakietu: {str(e)}")



    context = {
        'szyby': szyby,
        'ramki': ramki,
    }
    return render(request, 'catalog2/create_pakiet.html', context)


# Stwórz logger
logger = logging.getLogger(__name__)


def create_pakiet1(request):
    # Pobieramy dane z bazy, jeśli potrzebujemy
    szyby = Szyba.objects.all()
    ramki = Ramka.objects.all()

    if request.method == 'GET':
        # Zapisywanie URL referera do sesji, jeśli jest dostępny
        previous_url = request.META.get('HTTP_REFERER', '/')
        request.session['previous_url'] = previous_url

        # Ustawienie pakiet_type w formularzu


    elif request.method == 'POST':
        previous_url = request.META.get('HTTP_REFERER', '/')
        request.session['previous_url'] = previous_url
        form = PakietForm(request.POST)
        if not form.is_valid():
            print("Błędy formularza:", form.errors)  # Lub użyj loggera
            # Możesz też zwrócić komunikaty do szablonu dla testów
        else:
            # Przetwarzanie formularza...
            pass
        if form.is_valid():
            try:
                # Pobieranie danych z formularza
                szyba1 = form.cleaned_data['szyba1']



                logger = logging.getLogger(__name__)
                # Przygotowanie treści e-maila z danymi z formularza
                subject = 'Dane z formularza pakietu trzyszybowego'
                message = (
                    f"Szyba 1: {szyba1}\n"


                )
                from_email = 'noreply@example.com'
                recipient_list = ['admin@example.com']

                # Wysyłka e-maila.
                # Jeśli ustawisz EMAIL_BACKEND na konsolowy w settings.py,
                # wiadomość zostanie wyświetlona w konsoli\
                logger.info(f"Wysyłam e-mail: {message}")
                print(f"Wysyłam e-mail: {message}")
                send_mail(subject, message, from_email, recipient_list)
                return redirect(previous_url)
            except Exception as e:
                form.add_error(None, f"Wystąpił błąd podczas zapisywania pakietu: {str(e)}")

    return render(request, 'catalog2/create_pakiet1.html', {'form': form})


def create_pakiet2(request):
    szyby = Szyba.objects.all()
    ramki = Ramka.objects.all()

    if request.method == 'GET':
        # Zapisywanie URL referera do sesji, jeśli jest dostępny
        previous_url = request.META.get('HTTP_REFERER', '/')
        request.session['previous_url'] = previous_url

        # Ustawienie pakiet_type w formularzu


    elif request.method == 'POST':
        previous_url = request.META.get('HTTP_REFERER', '/')
        request.session['previous_url'] = previous_url
        form = PakietForm(request.POST)
        if not form.is_valid():
            print("Błędy formularza:", form.errors)  # Lub użyj loggera
            # Możesz też zwrócić komunikaty do szablonu dla testów
        else:
            # Przetwarzanie formularza...
            pass
        if form.is_valid():
            try:
                # Pobieranie danych z formularza
                szyba1 = form.cleaned_data['szyba1']
                ramka1 = form.cleaned_data['ramka1']
                szyba2 = form.cleaned_data['szyba2']

                logger = logging.getLogger(__name__)
                # Przygotowanie treści e-maila z danymi z formularza
                subject = 'Dane z formularza pakietu trzyszybowego'
                message = (
                    f"Szyba 1: {szyba1}\n"
                    f"Ramka 1: {ramka1}\n"
                    f"Szyba 2: {szyba2}\n"

                )
                from_email = 'noreply@example.com'
                recipient_list = ['admin@example.com']

                # Wysyłka e-maila.
                # Jeśli ustawisz EMAIL_BACKEND na konsolowy w settings.py,
                # wiadomość zostanie wyświetlona w konsoli\
                logger.info(f"Wysyłam e-mail: {message}")
                print(f"Wysyłam e-mail: {message}")
                send_mail(subject, message, from_email, recipient_list)
                return redirect(previous_url)
            except Exception as e:
                form.add_error(None, f"Wystąpił błąd podczas zapisywania pakietu: {str(e)}")

    return render(request, 'catalog2/create_pakiet2.html', {'form': form})


from django.shortcuts import render
from .models import Szyba, Ramka  # lub inna nazwa Twoich modeli

#def pakiet_trzyszybowy_view(request):
#    glassthree = Glassthree.objects.all()
#    szyby = Szyba.objects.all()
#    ramki = Ramka.objects.all()
#    context = {
#        'pak3': glassthree,
#        'szyby': szyby,
#        'ramki': ramki,
#    }
#    return render(request, 'catalog2/pakiet_trzyszybowy.html', context)
from rest_framework import viewsets
from .models import Glassthree
from .serializers import GlassthreeSerializer

import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Glassthree



class edit_pakiet(PermissionRequiredMixin, View):
    # Ustaw wymagane uprawnienie do zmiany (change) modelu Glassthree.
    # Zamień 'moja_aplikacja' na nazwę swojej aplikacji.
    permission_required = 'catalog2.change_glassthree'
    raise_exception = True  # Jeśli użytkownik nie ma uprawnień, zostanie zwrócony błąd 403

    def get(self, request, *args, **kwargs):
        """
        Obsługa żądania GET – pobranie danych pakietu w celu wypełnienia formularza edycji.
        Oczekujemy, że identyfikator pakietu zostanie przekazany przez query string jako ?id=...
        """
        pakiet_id = request.GET.get('id')
        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glassthree.objects.get(pk=pakiet_id)
        except Glassthree.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

        data = {
            'szyba1': pakiet.szyba1.id if pakiet.szyba1 else None,
            'ramka1': pakiet.ramka1.id if pakiet.ramka1 else None,
            'szyba2': pakiet.szyba2.id if pakiet.szyba2 else None,
            'ramka2': pakiet.ramka2.id if pakiet.ramka2 else None,
            'szyba3': pakiet.szyba3.id if pakiet.szyba3 else None,
            'grubosc_calkowita': pakiet.grubosc_calkowita,
        }
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        """
        Obsługa żądania PUT – aktualizacja danych danego pakietu.
        Identyfikator pakietu również pobieramy z query string (?id=...).
        W ciele żądania spodziewamy się JSON-a z danymi.
        """
        pakiet_id = request.GET.get('id')
        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glassthree.objects.get(pk=pakiet_id)
        except Glassthree.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Niepoprawne dane.'}, status=400)

        # Aktualizacja pól modelu; zakładamy, że klucze obce przekazywane są za pomocą notacji _id.
        if 'szyba1' in data:
            pakiet.szyba1_id = data['szyba1']
        if 'ramka1' in data:
            pakiet.ramka1_id = data['ramka1']
        if 'szyba2' in data:
            pakiet.szyba2_id = data['szyba2']
        if 'ramka2' in data:
            pakiet.ramka2_id = data['ramka2']
        if 'szyba3' in data:
            pakiet.szyba3_id = data['szyba3']
        if 'grubosc_calkowita' in data:
            pakiet.grubosc_calkowita = data['grubosc_calkowita']

        try:
            pakiet.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        """
        W przypadku wywołania metody innej niż GET lub PUT, zwracamy odpowiedź z niedozwoloną metodą.
        """
        return HttpResponseNotAllowed(['GET', 'PUT'])
class edit_pakiet2(PermissionRequiredMixin, View):
    # Ustawienie wymaganego uprawnienia do zmiany (change) obiektu Glasstwo.
    permission_required = 'catalog2.change_glasstwo'
    raise_exception = True  # Jeśli użytkownik nie ma uprawnień, zwrócony zostanie błąd 403

    def get(self, request, *args, **kwargs):
        """
        Obsługa żądania GET - pobranie danych pakietu, aby wypełnić formularz edycji.
        """
        # Pobieramy identyfikator pakietu z query string, np. ?id=1100
        pakiet_id = request.GET.get('id')
        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glasstwo.objects.get(pk=pakiet_id)
        except Glasstwo.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

        # Przygotowanie danych – przykładowo przekazujemy identyfikatory pól związanych (ForeignKey)
        data = {
            'szyba1': pakiet.szyba1.id if pakiet.szyba1 else None,
            'ramka1': pakiet.ramka1.id if pakiet.ramka1 else None,
            'szyba2': pakiet.szyba2.id if pakiet.szyba2 else None,
        }
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        """
        Obsługa żądania PUT - aktualizacja danych pakietu.
        """
        # Pobieramy identyfikator z query string
        pakiet_id = request.GET.get('id')
        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glasstwo.objects.get(pk=pakiet_id)
        except Glasstwo.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Niepoprawne dane.'}, status=400)

        # Aktualizacja pól – wykorzystujemy _id, aby przekazać wartość kluczy obcych
        if 'szyba1' in data:
            pakiet.szyba1_id = data['szyba1']
        if 'ramka1' in data:
            pakiet.ramka1_id = data['ramka1']
        if 'szyba2' in data:
            pakiet.szyba2_id = data['szyba2']

        try:
            pakiet.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        """
        Zwraca odpowiedź, gdy wywołana zostanie metoda HTTP inna niż GET lub PUT.
        """
        return HttpResponseNotAllowed(['GET', 'PUT'])
class edit_pakiet1(PermissionRequiredMixin, View):
    # Ustawienie wymaganego uprawnienia. Zamień 'moja_aplikacja' na właściwą nazwę Twojej aplikacji.
    permission_required = 'catalog2.change_glassone'
    raise_exception = True  # Jeśli użytkownik nie ma uprawnień, zwrócony zostanie błąd 403

    def get(self, request, *args, **kwargs):
        """
        Obsługa żądania GET - pobranie danych pakietu (np. do wypełnienia formularza edycji)
        """
        # Pobieramy identyfikator z parametrów zapytania (np. ?id=1100)
        pakiet_id = request.GET.get('id')
        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glassone.objects.get(pk=pakiet_id)
        except Glassone.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

        # Przygotowanie danych – przykładowo tylko pole szyba1
        data = {
            'szyba1': pakiet.szyba1.id if pakiet.szyba1 else None,
            # Możesz dodać kolejne pola, które chcesz udostępnić na formularzu edycji
        }
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        """
        Obsługa żądania PUT - aktualizacja danych pakietu
        """
        # Pobieramy ID pakietu z query string
        pakiet_id = request.GET.get('id')
        if not pakiet_id:
            return JsonResponse({'error': 'Nie podano id.'}, status=400)

        try:
            pakiet = Glassone.objects.get(pk=pakiet_id)
        except Glassone.DoesNotExist:
            return JsonResponse({'error': 'Pakiet nie istnieje.'}, status=404)

        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Niepoprawne dane.'}, status=400)

        # Aktualizacja pól – przykładowo aktualizacja szyba1 przy użyciu klucza obcego (_id)
        if 'szyba1' in data:
            pakiet.szyba1_id = data['szyba1']

        try:
            pakiet.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['GET', 'PUT'])


# catalog2/views.py
from django.http import FileResponse
from django.views import View
from .utils.converter import  generate_xlsx

class ExportXlsxView(View):
    def get(self, request, *args, **kwargs):
        file_data = generate_xlsx()
        return FileResponse(
            file_data,
            as_attachment=True,
            filename='pakiety.xlsx'
        )

from django.http import HttpResponse
from django.views import View
from .utils.csv_exporter import generate_csv

class ExportCsvView(View):
    def get(self, request, *args, **kwargs):
        csv_file = generate_csv()
        response = HttpResponse(csv_file.getvalue(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="pakiety.csv"'
        return response


import csv
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVImportForm
from catalog2.models import Glassone, Glasstwo, Glassthree, Szyba, Ramka


def import_csv_view(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
            except Exception as e:
                messages.error(request, f"Błąd odczytu pliku: {e}")
                # W przypadku błędu odczytu ponownie renderujemy stronę z formularzem
                return render(request, 'catalog2/import_csv.html', {'form': form})

            reader = csv.reader(decoded_file)
            rows = list(reader)
            if not rows:
                messages.error(request, "Plik CSV jest pusty.")
                return render(request, 'catalog2/import_csv.html', {'form': form})

            # Pomijamy pierwszy wiersz (nagłówek)
            header = rows.pop(0)
            current_section = None
            for row in rows:
                if not any(cell.strip() for cell in row):
                    continue
                if row[0] in ('Glassone', 'Glasstwo', 'Glassthree'):
                    current_section = row[0]
                    continue
                try:
                    if current_section == 'Glassone':
                        # Zakładamy format: [ID, szyba1_name, "", "", "", "", szyba1_grubosc, ufactor, gfactor, rw]
                        _, szyba1_name, _, _, _, _, szyba1_grubosc, ufactor, gfactor, rw = row
                        szyba, created = Szyba.objects.get_or_create(
                            nazwa=szyba1_name,
                            defaults={'grubosc': Decimal(szyba1_grubosc)}
                        )
                        Glassone.objects.create(
                            szyba1=szyba,
                            ufactor=Decimal(ufactor),
                            gfactor=Decimal(gfactor),
                            rw=Decimal(rw)
                        )
                    elif current_section == 'Glasstwo':
                        # Format: [ID, szyba1_name, ramka1_name, szyba2_name, "", "", "", ufactor, gfactor, rw]
                        _, szyba1_name, ramka1_name, szyba2_name, _, _, _, ufactor, gfactor, rw = row

                        szyba1 = Szyba.objects.get(nazwa=szyba1_name)
                        szyba2 = Szyba.objects.get(nazwa=szyba2_name)
                        ramka1 = Ramka.objects.get(nazwa=ramka1_name)

                        Glasstwo.objects.create(
                            szyba1=szyba1,
                            ramka1=ramka1,
                            szyba2=szyba2,
                            ufactor=Decimal(ufactor),
                            gfactor=Decimal(gfactor),
                            rw=Decimal(rw)
                        )
                    elif current_section == 'Glassthree':
                        # Format: [ID, szyba1_name, ramka1_name, szyba2_name, ramka2_name, szyba3_name, "", ufactor, gfactor, rw]
                        (_, szyba1_name, ramka1_name, szyba2_name, ramka2_name,
                         szyba3_name, _, ufactor, gfactor, rw) = row

                        szyba1 = Szyba.objects.get(nazwa=szyba1_name)
                        szyba2 = Szyba.objects.get(nazwa=szyba2_name)
                        szyba3 = Szyba.objects.get(nazwa=szyba3_name)
                        ramka1 = Ramka.objects.get(nazwa=ramka1_name)
                        ramka2 = Ramka.objects.get(nazwa=ramka2_name)

                        Glassthree.objects.create(
                            szyba1=szyba1,
                            ramka1=ramka1,
                            szyba2=szyba2,
                            ramka2=ramka2,
                            szyba3=szyba3,
                            ufactor=Decimal(ufactor),
                            gfactor=Decimal(gfactor),
                            rw=Decimal(rw)
                        )
                except Exception as e:
                    # Logowanie błędów lub przekazanie informacji o nieprzetworzonym wierszu
                    continue

            messages.success(request, "Import zakończony pomyślnie.")
            # Po zakończonym imporcie przekierowujemy użytkownika na stronę główną
            return redirect('index')
    else:
        form = CSVImportForm()
    return render(request, 'catalog2/import_csv.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .utils.import_xlsx import import_xlsx  # Upewnij się, że ścieżka do modułu jest poprawna

def import_xlsx_view(request):
    if request.method == 'POST':

        uploaded_file = request.FILES.get('xlsx_file')
        if not uploaded_file:
            messages.error(request, "Nie wybrano pliku.")
            return redirect("index")

        # Weryfikujemy, czy plik ma rozszerzenie XLSX (można rozszerzyć o walidację typu MIME)
        if not uploaded_file.name.lower().endswith('.xlsx'):
            messages.error(request, "Plik musi mieć rozszerzenie XLSX.")
            return redirect("index")

        try:
            # Wywołanie funkcji importującej; funkcja odczytuje plik i wykonuje zapis rekordów
            import_xlsx(uploaded_file)
            messages.success(request, "Import zakończony pomyślnie.")
        except Exception as e:
            # Logika obsługi błędów; warto rozbudować o szczegółowe logowanie w realnej aplikacji
            messages.error(request, f"Błąd podczas importu: {e}")
        return redirect("index")
    # Dla metody GET renderujemy szablon z formularzem
    return render(request, "import_xlsx.html")


import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def html_to_xml_view2(request):
    # Adresy – zmodyfikuj je zgodnie z konfiguracją Twojej aplikacji
    login_url = "http://127.0.0.1:8000/login/"  # Endpoint logowania
    target_url = "http://127.0.0.1:8000/pakiet_dwuszybowy/"  # Endpoint zabezpieczonego widoku

    # Dane logowania – podaj swoje poprawne dane
    login_data = {
        "username": "maxgren",
        "password": "makaron79",
    }

    session = requests.Session()


    try:
        login_get_response = session.get(login_url)
        login_get_response.raise_for_status()
    except requests.RequestException as e:
        error_xml = ('<?xml version="1.0" encoding="utf-8"?><error>Błąd przy pobieraniu strony logowania: {}</error>'
                     .format(e)).encode("utf-8")
        return HttpResponse(error_xml, status=500, content_type="application/xml")

    soup_login = BeautifulSoup(login_get_response.text, "html.parser")
    csrf_input = soup_login.find("input", attrs={"name": "csrfmiddlewaretoken"})
    if csrf_input:
        csrf_token = csrf_input.get("value")
        login_data["csrfmiddlewaretoken"] = csrf_token
    login_headers = {
        "Referer": login_url,
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.0.0 Safari/537.36"
        ),
    }

    try:
        login_post_response = session.post(login_url, data=login_data, headers=login_headers)
        login_post_response.raise_for_status()
    except requests.RequestException as e:
        error_xml = ('<?xml version="1.0" encoding="utf-8"?><error>Błąd przy logowaniu: {}</error>'
                     .format(e)).encode("utf-8")
        return HttpResponse(error_xml, status=500, content_type="application/xml")

    target_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": login_url
    }

    try:
        target_response = session.get(target_url, headers=target_headers)
        target_response.raise_for_status()
        html_content = target_response.text
    except requests.RequestException as e:
        error_xml = ('<?xml version="1.0" encoding="utf-8"?><error>Błąd przy pobieraniu danych: {}</error>'
                     .format(e)).encode("utf-8")
        return HttpResponse(error_xml, status=500, content_type="application/xml")

    soup = BeautifulSoup(html_content, "html.parser")
    tbody = soup.find("tbody")
    if not tbody:
        error_xml = (
            '<?xml version="1.0" encoding="utf-8"?><error>Nie znaleziono elementu &lt;tbody&gt; w HTML.</error>'
            ).encode("utf-8")
        return HttpResponse(error_xml, status=404, content_type="application/xml")

    data_list = []
    rows = tbody.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 7:
            continue
        record = {
            "szyba1": cells[0].get_text(strip=True),
            "ramka1": cells[1].get_text(strip=True),
            "szyba2": cells[2].get_text(strip=True),
            "grubosc_calkowita": cells[3].get_text(strip=True).replace("mm", "").strip(),
            "gfactor": cells[4].get_text(strip=True),
            "ufactor": cells[5].get_text(strip=True),
            "rw": cells[6].get_text(strip=True)
        }
        data_list.append(record)

    root = ET.Element("data")
    for record in data_list:
        rec_elem = ET.SubElement(root, "record")
        for key, value in record.items():
            child = ET.SubElement(rec_elem, key)
            child.text = value

    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    xml_declaration = b'<?xml version="1.0" encoding="utf-8"?>\n'
    final_xml = xml_declaration + xml_str

    return HttpResponse(final_xml, content_type="application/xml")
@require_GET
def html_to_xml_view1(request):

    login_url = "http://127.0.0.1:8000/login/"
    target_url = "http://127.0.0.1:8000/pakiet_jednoszybowy/"


    login_data = {
        "username": "maxgren",
        "password": "makaron79",
    }

    session = requests.Session()


    try:
        login_get_response = session.get(login_url)
        login_get_response.raise_for_status()
    except requests.RequestException as e:
        error_xml = ('<?xml version="1.0" encoding="utf-8"?><error>Błąd przy pobieraniu strony logowania: {}</error>'
                     .format(e)).encode("utf-8")
        return HttpResponse(error_xml, status=500, content_type="application/xml")

    soup_login = BeautifulSoup(login_get_response.text, "html.parser")
    csrf_input = soup_login.find("input", attrs={"name": "csrfmiddlewaretoken"})
    if csrf_input:
        csrf_token = csrf_input.get("value")
        login_data["csrfmiddlewaretoken"] = csrf_token
    login_headers = {
        "Referer": login_url,
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.0.0 Safari/537.36"
        ),
    }

    try:
        login_post_response = session.post(login_url, data=login_data, headers=login_headers)
        login_post_response.raise_for_status()
    except requests.RequestException as e:
        error_xml = ('<?xml version="1.0" encoding="utf-8"?><error>Błąd przy logowaniu: {}</error>'
                     .format(e)).encode("utf-8")
        return HttpResponse(error_xml, status=500, content_type="application/xml")

    target_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": login_url
    }

    try:
        target_response = session.get(target_url, headers=target_headers)
        target_response.raise_for_status()
        html_content = target_response.text
    except requests.RequestException as e:
        error_xml = ('<?xml version="1.0" encoding="utf-8"?><error>Błąd przy pobieraniu danych: {}</error>'
                     .format(e)).encode("utf-8")
        return HttpResponse(error_xml, status=500, content_type="application/xml")

    soup = BeautifulSoup(html_content, "html.parser")
    tbody = soup.find("tbody")
    if not tbody:
        error_xml = (
            '<?xml version="1.0" encoding="utf-8"?><error>Nie znaleziono elementu &lt;tbody&gt; w HTML.</error>'
            ).encode("utf-8")
        return HttpResponse(error_xml, status=404, content_type="application/xml")

    data_list = []
    rows = tbody.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue  # Pomijamy wiersze z niepełną liczbą komórek
        record = {
            "szyba1": cells[0].get_text(strip=True),
            "gfactor": cells[1].get_text(strip=True),
            "ufactor": cells[2].get_text(strip=True),
            "rw": cells[3].get_text(strip=True)
        }
        data_list.append(record)

    root = ET.Element("data")
    for record in data_list:
        rec_elem = ET.SubElement(root, "record")
        for key, value in record.items():
            child = ET.SubElement(rec_elem, key)
            child.text = value

    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    xml_declaration = b'<?xml version="1.0" encoding="utf-8"?>\n'
    final_xml = xml_declaration + xml_str

    return HttpResponse(final_xml, content_type="application/xml")


import requests
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def json_to_xml_view(request):

    api_url = "http://127.0.0.1:8000/api/pakiet_trzyszybowy/?page=1"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Sprawdzić, czy nie wystąpił błąd HTTP
        json_data = response.json()
    except requests.RequestException as e:
        error_xml = ('<?xml version="1.0" encoding="utf-8"?><error>Błąd przy pobieraniu danych z API: {}</error>'
                     .format(e)).encode("utf-8")
        return HttpResponse(error_xml, status=500, content_type="application/xml")



    root = ET.Element("data")

    for item in json_data.get("results", []):
        rec_elem = ET.SubElement(root, "record")
        # Przykładowa konwersja – dostosuj pola do Twojej struktury danych
        ET.SubElement(rec_elem, "id").text = str(item.get("id", ""))

        # Zakładamy, że 'szyba1' jest obiektem z polem 'nazwa'
        ET.SubElement(rec_elem, "szyba1").text = item.get("szyba1", {}).get("nazwa", "")
        ET.SubElement(rec_elem, "ramka1").text = item.get("ramka1", {}).get("nazwa", "")
        ET.SubElement(rec_elem, "szyba2").text = item.get("szyba2", {}).get("nazwa", "")
        ET.SubElement(rec_elem, "ramka2").text = item.get("ramka2", {}).get("nazwa", "")
        ET.SubElement(rec_elem, "szyba3").text = item.get("szyba3", {}).get("nazwa", "")
        ET.SubElement(rec_elem, "grubosc_calkowita").text = str(item.get("grubosc_calkowita", ""))
        ET.SubElement(rec_elem, "gfactor").text = str(item.get("gfactor", ""))
        ET.SubElement(rec_elem, "ufactor").text = str(item.get("ufactor", ""))
        ET.SubElement(rec_elem, "rw").text = str(item.get("rw", ""))

    # Konwertujemy drzewo XML do łańcucha bajtów
    xml_str = ET.tostring(root, encoding="utf-8", method="xml")
    xml_declaration = b'<?xml version="1.0" encoding="utf-8"?>\n'
    final_xml = xml_declaration + xml_str

    return HttpResponse(final_xml, content_type="application/xml")