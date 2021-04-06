from django import forms

class ArtistName(forms.Form):
    artist_name = forms.CharField(label=(""),
                     widget=forms.TextInput(attrs={'placeholder': 'Artist Name'}))