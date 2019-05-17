# -*- coding: utf-8 -*-
from aldryn_client import forms


def split_and_strip(string):
    return [item.strip() for item in string.split(',') if item]


class Form(forms.BaseForm):
    templates = forms.CharField(
        'List of additional templates (comma separated)',
        required=False,
    )
    terms = forms.CharField(
        'Default Terms',
        required=False,
    )
    show_context = forms.CheckboxField(
        'Show Context',
        required=False,
        initial=False,
    )

    def clean(self):
        data = super(Form, self).clean()

        # prettify
        data['templates'] = ', '.join(split_and_strip(data['templates']))
        return data

    def to_settings(self, data, settings):
        if data['templates']:
            settings['DJANGOCMS_FILE_TEMPLATES'] = [
                (item, item)
                for item in split_and_strip(data['templates'])
            ]
        if data['terms']:
            settings['DJANGOCMS_FILE_TERMS'] = data['terms']
        if data['show_context']:
            settings['DJANGOCMS_FILE_SHOW_CONTEXT'] = int(data['show_context'])

        return settings
