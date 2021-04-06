from django.shortcuts import render, redirect
from .spopulate import get_top_artists, create_playlist, match, main, artist_search
from .models import *
from .forms import ArtistName
from django.conf import settings

def check_profile(profile):
    if not profile.populated:
        get_top_artists(profile)

        
def homepage(request):
    print(settings.CLIENT_ID)
    return render(request, 'homepage.html')


def room(request):
    check_profile(request.user.profile)

    users = User.objects.all()
    
    return render(request, 'room.html', {'users': users})

def show_top_artists(request):
    return render(request,'top_artists.html')

def splat(request, user_id):
    user2 = User.objects.get(id=user_id)
    master_list = match([request.user, user2])
    playlist_id = main(master_list, request.user.profile, user2)

    return render(request, 'result.html', {'playlist_id':playlist_id})

def play(request, playlist_id):
    
    return render(request, 'play.html', {'playlist_id':playlist_id})


def addNewArtists(request):
    if request.method == 'POST':
        form = ArtistName(request.POST) 
        if form.is_valid(): 

            query = form.cleaned_data['artist_name']

            artist = artist_search(query, request.user.profile)

            print(artist)
            
            return redirect('add')
    else:
        form = ArtistName() # An unbound form
    return render(request, 'add_new_artists.html', {'form':form})
