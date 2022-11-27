from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView, CreateView
from django import forms
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.core.files.storage import FileSystemStorage

from chatterapp.models import Room, Theme, Message, MessageFile

# Create your views here.
#def hello(request):
#    return HttpResponse("Hello world!")

def hello(request):
  s = request.GET.get('s', '')
  return HttpResponse(f'Hello, {s} world!')

#def hello(request, name):
#    return HttpResponse(f"Hello {name}!")

def ahoj(request):
    return HttpResponse("Ahoj světe!")

def home(request):
    #return HttpResponse("Home")
    return render(request, "chatterapp/home.html")

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rooms(request):
    rooms = Room.objects.all()  # z dabáze vytáhneme všechny záznamy
    context = {'rooms': rooms}  # výsledek si uložíme do slovníku
    return render(request, "chatterapp/rooms.html", context)  # vykreslíme template
    #return render(request, "chatterapp/rooms.html", {'rooms': Room.objects.all()})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def room(request, pk):
    room = Room.objects.get(id=pk)
    # pokud dostaneme data metodou post (z formuláře) => nová zpráva
    if request.method == 'POST':
        body = request.POST.get('body').strip()
        file_url = None
        if request.FILES.get('upload'):              # pokud jsme odeslali soubor
            upload = request.FILES.get('upload')     # vytáhnu soubor z requestu
            file_storage = FileSystemStorage()       # práce se souborovým systémem
            file = file_storage.save(upload.name, upload)  # uložíme soubor na disk
            file_url = file_storage.url(file)        # vytáhnu ze souboru url adresu a uložím

        if len(body) > 0 or file_url:
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=body,
                file=file_url
            )
            '''if file_url:
                message_file = MessageFile.objects.create(
                    file=file_url,
                    message=message
                )'''

    # najít zprávy dané místnosti
    messages = Message.objects.filter(room=pk)

    context = {'room': room, 'messages': messages}
    return render(request, "chatterapp/room.html", context)

# první metoda pro vytváření nové místnosti pomocí dvou metod:
# 1. zobrazí se formulář pomocí new_room
# 2. data z formuláře zpracuje create_room
# zobrazení formuláře pro vytvoření nové místnosti (ale nevytvoří místnost)
@login_required
def new_room(request):
    themes = Theme.objects.all()
    context = {'themes': themes}
    return render(request, 'chatterapp/new_room.html', context)

# zpracuje data z formuláře (new_room) a vytvoří novou místnost
@login_required
def create_room(request):
    if request.method == 'POST':  # pokud jsme dostali data metodou POST
        if request.POST.get('private'):
            private = True
        else:
            private = False
        room = Room.objects.create(
            name=request.POST.get('name'),
            theme=Theme.objects.get(id=request.POST.get('theme')),
            description=request.POST.get('description'),
            private=private,
            owner=request.user
        )
        #return redirect('rooms')
        return redirect('room', pk=room.id)
    else:
        return redirect('home')

# druhá metoda pro vytváření nové místnosti pomocí jedné metody:
@login_required
def create_room_v2(request):
    if request.method == 'POST':  # pokud jsme dostali data metodou POST
        if request.POST.get('private'):
            private = True
        else:
            private = False
        # ošetřit prázdné jméno
        name = request.POST.get('name').strip()  # strip "ořízne" prázdné znaky na začátku a na konci
        # ošetřit prázdný popis
        description = request.POST.get('description').strip()
        if len(name) > 0 and len(description) > 0:
            room = Room.objects.create(
                name=name,
                theme=Theme.objects.get(id=request.POST.get('theme')),
                description=description,
                private=private,
                owner=request.user
            )
            return redirect('room', pk=room.id)
        # pokud místnost nebyla vytvořena
        if len(name) == 0:
            context = {'error_message': "I can not create room without name."}
        if len(description) == 0:
            context = {'error_message': "I can not create room without description."}
        if len(name) == 0 and len(description) == 0:
            context = {'error_message': "I can not create room without name and description."}
        return render(request, 'chatterapp/error_page.html', context)
    else:   # pokud jsme nedostali data pomocí POST, zobrazíme formulář
        themes = Theme.objects.all()
        context = {'themes': themes}
        return render(request, 'chatterapp/new_room_v2.html', context)


# třetí metoda pro vytváření nové místnosti pomocí třídy (FormView):
class RoomForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    private = forms.BooleanField()


@method_decorator(login_required, name='dispatch')
class RoomFormView(FormView):
    template_name = "chatterapp/new_room_v3.html"  # odkážeme se na template
    form_class = RoomForm
    success_url = '/rooms/'


# čtvrtá metoda pro vytváření nové místnosti pomocí třídy (CreateView):
@method_decorator(login_required, name='dispatch')
class RoomCreateView(CreateView):
    model = Room
    #fields = ['name', 'theme', 'description', 'private']
    fields = '__all__'
    success_url = '/rooms/'


@login_required
def delete_room(request, pk):
    try:
        if request.user == Room.owner or request.user.is_superuser:
            room = Room.objects.get(id=pk)
            context = {'room': room}
            return render(request, 'chatterapp/delete_room.html', context)
        else:
            context = {'error_message': "You cant delete this room."}
            return render(request, 'chatterapp/error_page.html', context)
    except:
        context = {'error_message': "Room not exist."}
        return render(request, 'chatterapp/error_page.html', context)
    #return redirect('rooms')

@login_required
def delete_room_yes(request, pk):
    try:
        room = Room.objects.get(id=pk)
        room.delete()
    except:
        pass
    return redirect('rooms')

