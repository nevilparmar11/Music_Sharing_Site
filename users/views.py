from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from music.models import Album, Song
from .forms import  UserForm
from .models import Friend


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'users/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'users/index.html', {'albums': albums})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'users/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = user.username
            request.session['id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['email'] = user.email
            request.session['password'] = user.password
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'users/index.html', {'albums': albums})
            else:
                return render(request, 'users/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'users/login.html', {'error_message': 'Invalid login'})
    return render(request, 'users/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        last_name = form.cleaned_data['last_name']
        first_name = form.cleaned_data['first_name']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        request.session['username'] = user.username
        request.session['id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['email'] = user.email
        request.session['password'] = user.password
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'users/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'users/register.html', context)

def profile(request):
    return render(request, 'users/profile.html')


def edit_profile(request):
    return render(request, 'users/edit_profile.html')


def update_profile(request):
    if request.method == "POST":
        server_firstname = request.POST['first_name']
        server_lastname = request.POST['last_name']
        server_password = request.POST['password']
        if server_password == request.POST['confirm_password']:
            try:
                user = User.objects.get(username = request.session['username'])
                user.first_name = server_firstname
                user.last_name = server_lastname
                user.password = server_password
                user.save()
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['password'] = user.password
                return render(request,'users/profile.html')
            except:
                messages.error(request, 'ERROR: Invalid inputs, try again!')
                return render(request,'users/edit_profile.html')
        else:
            messages.error(request, 'ERROR: Passwords do not match, try again!')
            return render(request,'users/edit_profile.html')
    else:
        messages.error(request, 'ERROR: Invalid inputs, try again!')
        return render(request,'users/edit_profile.html')


def follow_users(request):
    context = {
        "notfriends": User.objects.exclude(id=request.session['id']).exclude(followers__follower_id=request.session['id']),
        "friends": User.objects.filter(followers__follower_id=request.session['id'])
    }
    return render(request, 'users/follow_users.html', context)


def follow(request, followee_id):
    Friend.objects.create(follower_id=request.session['id'], followee_id=followee_id)
    context = {
        "notfriends": User.objects.exclude(id=request.session['id']).exclude(
            followers__follower_id=request.session['id']),
        "friends": User.objects.filter(followers__follower_id=request.session['id'])
    }
    return render(request,'users/follow_users.html',context)


def unfollow(request, followee_id):
    Friend.objects.filter(followee_id=followee_id).delete()
    context = {
        "notfriends": User.objects.exclude(id=request.session['id']).exclude(
            followers__follower_id=request.session['id']),
        "friends": User.objects.filter(followers__follower_id=request.session['id'])
    }
    return render(request,'users/follow_users.html',context)


def my_followers(request):
    context = {
        "my_followers": User.objects.filter(followers__follower_id=request.session['id'])
        }
    return render(request, 'users/my_followers.html', context)


def follower_profile(request, follower_id):
    context = {
        "friend": User.objects.get(id=follower_id)
    }
    return render(request, 'users/follower_profile.html', context)
