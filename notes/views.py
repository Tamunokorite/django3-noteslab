from django.shortcuts import get_object_or_404, redirect, render
from notes.forms import NoteForm
from notes.models import Note
import time

# Create your views here.
def index(request):
    return render(request, 'notes/index.html', {'title': 'Notes'})

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
        return render(request, 'notes/viewnote.html', {'note':note, 'form':form})
    else:
        try:
            form = NoteForm(request.POST, instance=note)
            form.save()
            return redirect('mynotes')
        except ValueError:
            return render(request, 'notes/viewnote.html', {'form':NoteForm(), 'error':'Bad info'})