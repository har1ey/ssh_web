__author__ = 'har1ey'

from django.forms import ModelForm
from models import Key
from django import forms

class SshKeyForm(ModelForm):
    class Meta:
        model = Key
        fields = ['ssh_key']
