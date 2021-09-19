from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from notes.forms import NoteForm
from notes.models import Note
# from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'notes/index.html', {'title': 'NotesLab'})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'notes/signup.html', {'title': 'NotesLab | Sign Up', 'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('mynotes')
            except IntegrityError:
                return render(request, 'notes/signup.html', {'title': 'NotesLab | Sign Up', 'form': UserCreationForm(), 'error': 'This username is taken. Please try another one'})
        else:
            return render(request, 'notes/signup.html', {'title': 'NotesLab | Sign Up', 'form': UserCreationForm(), 'error': 'Passwords do not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, "notes/login.html", {'title': 'NotesLab | Login', 'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "notes/login.html", {'title': 'NotesLab | Login', 'form':AuthenticationForm(), "error":"Username and password did not match"})
        else:
            login(request, user)
            return redirect('mynotes')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

@login_required
def newnote(request):
    if request.method == 'GET':
        return render(request, 'notes/newnote.html', {'title': 'New Note', 'form': NoteForm()})
    else:
        try:
            form = NoteForm(request.POST)
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            return redirect('mynotes')
        except ValueError:
            return render(request, 'notes/newnote.html', {'title': 'New Note', 'form': NoteForm(), 'error': 'Bad data passed in. Try again.'})

@login_required
def viewnotes(request):
    notes = Note.objects.filter(user=request.user, deleted=False).order_by('-modified')
    return render(request, 'notes/viewnotes.html', {'title': 'My Notes', 'notes': notes})

@login_required
def viewnote(request, id):
    note = get_object_or_404(Note, pk=id)
    if request.user != note.user:
        return redirect('index')
    if request.method == 'GET':
        form = NoteForm(instance=note)
        return render(request, 'notes/viewnote.html', {'title': note.title,'note':note, 'form':form})
    else:
        try:
            form = NoteForm(request.POST, instance=note)
            note.modified = timezone.now()
            form.save()
            return redirect('mynotes')
        except ValueError:
            return render(request, 'notes/viewnote.html', {'title': note.title,'form':NoteForm(), 'error':'Bad info'})

@login_required
def deletenote(request, id):
    note = get_object_or_404(Note, pk=id)
    if request.user != note.user:
        return redirect('index')
    note.deleted = True
    note.date_deleted = timezone.now()
    note.save()
    return redirect('mynotes')