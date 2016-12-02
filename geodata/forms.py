from django import forms
from .models import Gpslocation

class Gpslocationform(forms.ModelForm):
    date = forms.CharField()
    class Meta:
        model = Gpslocation
        fields = ('latitude','longitude','speed','direction','distance',
                  'locationmethod','username','phonenumber','sessionid',
                  'accuracy','extrainfo','eventtype',)
        