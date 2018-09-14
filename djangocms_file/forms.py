# -*- coding: utf-8 -*-

from django import forms
from .models import File


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = '__all__'
        widgets = {
            'link_type': forms.RadioSelect(attrs={'class': 'inline-block'}),
        }
