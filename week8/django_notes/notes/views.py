from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Note
from .forms import NoteForm


def index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})


def create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note created successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm()
    return render(request, 'notes/form.html', {'form': form, 'title': 'Create Note'})


def edit(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/form.html', {'form': form, 'title': 'Edit Note'})


def delete(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('index')
    return render(request, 'notes/delete.html', {'note': note})
