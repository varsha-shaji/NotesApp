from django.shortcuts import render,redirect, get_object_or_404
from .models import User, Note
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,'index.html')

def login(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email,password=password).first()
        if user:
            request.session['email'] = user.email
            return redirect('dashboard')
        else:
            return render(request,'LogReg.html',{'error':'Invalid credentials'})
    return render(request,'LogReg.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = User.objects.create(name=name,email=email,password=password)
            user.save()
            return redirect('login')
        else:
            return render(request,'LogReg.html',{'error':'Passwords do not match'})
        
def dashboard(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    user = User.objects.filter(email=email).first()
    if user:
        notes_qs = Note.objects.filter(user=user)
        total_notes = notes_qs.count()
        pinned_notes = notes_qs.filter(pinned=True).count()
        archived_notes = notes_qs.filter(archived=True).count()
        return render(request, 'dashboard.html', {
            'user': user,
            'total_notes': total_notes,
            'pinned_notes': pinned_notes,
            'archived_notes': archived_notes,
        })
    else:
        return redirect('login')

def add_note(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    user = User.objects.filter(email=email).first()
    if not user:
        return redirect('login')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')
        pinned = bool(request.POST.get('pinned'))
        archived = bool(request.POST.get('archived'))
        color = request.POST.get('color', '')
        Note.objects.create(
            user=user,
            title=title,
            content=content,
            tags=tags,
            pinned=pinned,
            archived=archived,
            color=color
        )
        return redirect('dashboard')
    return render(request, 'add_note.html', {'user': user})

def my_notes(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    user = User.objects.filter(email=email).first()
    if not user:
        return redirect('login')
    notes = Note.objects.filter(user=user)
    tag = request.GET.get('tag')
    pinned = request.GET.get('pinned')
    archived = request.GET.get('archived')
    if tag:
        notes = notes.filter(tags=tag)
    if pinned:
        notes = notes.filter(pinned=True)
    if archived:
        notes = notes.filter(archived=True)
    notes = notes.order_by('-created_at')
    return render(request, 'my_notes.html', {'user': user, 'notes': notes})

def edit_note(request, note_id):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    user = User.objects.filter(email=email).first()
    note = get_object_or_404(Note, id=note_id, user=user)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.tags = request.POST.get('tags')
        note.color = request.POST.get('color')
        note.save()
        return redirect('my_notes')
    return render(request, 'edit_note.html', {'user': user, 'note': note})

def toggle_pin(request, note_id):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    user = User.objects.filter(email=email).first()
    note = get_object_or_404(Note, id=note_id, user=user)
    note.pinned = not note.pinned
    note.save()
    return redirect('my_notes')

def toggle_archive(request, note_id):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    user = User.objects.filter(email=email).first()
    note = get_object_or_404(Note, id=note_id, user=user)
    note.archived = not note.archived
    note.save()
    return redirect('my_notes')

def delete_note(request, note_id):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    user = User.objects.filter(email=email).first()
    note = get_object_or_404(Note, id=note_id, user=user)
    if request.method == 'POST':
        note.delete()
        return redirect('my_notes')
    return render(request, 'delete_note_confirm.html', {'user': user, 'note': note})

def logout(request):
    request.session.flush()
    return redirect('login')