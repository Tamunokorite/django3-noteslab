from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from notes.forms import NoteForm
from notes.models import Note
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'notes/index.html', {'title': 'Notes'})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'notes/signup.html', {'title': 'Sign Up', 'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('mynotes')
            except IntegrityError:
                return render(request, 'notes/signup.html', {'title': 'Sign Up', 'form': UserCreationForm(), 'error': 'This username is taken. Please try another one'})
        else:
            return render(request, 'notes/signup.html', {'title': 'Sign Up', 'form': UserCreationForm(), 'error': 'Passwords do not match'})

def newnote(request):
    if request.method == 'GET':
        return render(request, 'notes/newnote.html', {'title': 'New Note', 'form': NoteForm()})
    else:
        try:
            form = NoteForm(request.POST)
            form.save(commit=True)
            return redirect('mynotes')
        except ValueError:
            return render(request, 'notes/newnote.html', {'title': 'New Note', 'form': NoteForm(), 'error': 'Bad data passed in. Try again.'})

def viewnotes(request):
    notes = Note.objects.filter(deleted=False)
    return render(request, 'notes/viewnotes.html', {'title': 'My Notes', 'notes': notes})

def viewnote(request, id):
    note = get_object_or_404(Note, pk=id)
    if request.method == 'GET':
        form = NoteForm(instance=note)
        return render(request, 'notes/viewnote.html', {'title': note.title,'note':note, 'form':form})
    else:
        try:
            form = NoteForm(request.POST, instance=note)
            note.modified = datetime.now()
            form.save()
            return redirect('mynotes')
        except ValueError:
            return render(request, 'notes/viewnote.html', {'title': note.title,'form':NoteForm(), 'error':'Bad info'})

def deletenote(request, id):
    note = get_object_or_404(Note, pk=id)
    note.deleted = True
    note.date_deleted = datetime.now()
    note.save()
    return redirect('mynotes')