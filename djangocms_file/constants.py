# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.utils.translation import ugettext_lazy as _
from django.conf import settings


DEFAULT_TERMS = getattr(
    settings,
    'DJANGOCMS_FILE_TERMS',
    '',
)
SHOW_CONTEXT = getattr(
    settings,
    'DJANGOCMS_FILE_SHOW_CONTEXT',
    False,
)
