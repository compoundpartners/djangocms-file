# -*- coding: utf-8 -*-
"""
Enables the user to add a "File" plugin that displays a file wrapped by
an <anchor> tag.
"""
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _

from cms.models import CMSPlugin

from djangocms_attributes_field.fields import AttributesField

from filer.fields.file import FilerFileField
from filer.fields.folder import FilerFolderField


LINK_TARGET = (
    ('_self', _('Open in same window')),
    ('_blank', _('Open in new window')),
    ('_parent', _('Delegate to parent')),
    ('_top', _('Delegate to top')),
)


# Add additional choices through the ``settings.py``.
def get_templates():
    choices = [
        ('default', _('Default')),
    ]
    choices += getattr(
        settings,
        'DJANGOCMS_FILE_TEMPLATES',
        [],
    )
    return choices


@python_2_unicode_compatible
class File(CMSPlugin):
    """
    Renders a file wrapped by an anchor
    """
    search_fields = ('name',)

    template = models.CharField(
        verbose_name=_('Template'),
        choices=get_templates(),
        default=get_templates()[0][0],
        max_length=255,
    )
    file_src = FilerFileField(
        verbose_name=_('File'),
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    name = models.CharField(
        verbose_name=_('Display name'),
        blank=True,
        max_length=255,
        help_text=_('Overrides the default file display name with the given value.'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        default=''
    )
    terms = models.TextField(
        verbose_name=_('Terms'),
        blank=True,
        default=''
    )
    show_terms = models.BooleanField(
        verbose_name=_('Show terms'),
        blank=True,
        default=False,
    )
    link_target = models.CharField(
        verbose_name=_('Link target'),
        choices=LINK_TARGET,
        blank=True,
        max_length=255,
        default='',
    )
    link_title = models.CharField(
        verbose_name=_('Link title attrubute'),
        blank=True,
        max_length=255,
    )
    show_file_size = models.BooleanField(
        verbose_name=_('Show file size'),
        blank=True,
        default=False,
        help_text=_('Appends the file size at the end of the name.'),
    )

    LINK_CHOICES = (
        ('link', _('Link')),
        ('btn', _('Button')),
    )
    link_type = models.CharField(
        verbose_name=_('Type'),
        choices=LINK_CHOICES,
        default=LINK_CHOICES[1][0],  # Button
        max_length=255,
        help_text=_('Adds either the .btn-* or .text-* classes.'),
    )

    COLOR_STYLE_CHOICES = (
        ('link', _('Link')),
        ('primary', _('Primary')),
        ('secondary', _('Secondary')),
        ('success', _('Success')),
        ('danger', _('Danger')),
        ('warning', _('Warning')),
        ('info', _('Info')),
        ('light', _('Light')),
        ('dark', _('Dark')),
    )
    link_context = models.CharField(
        verbose_name=_('Context'),
        choices=COLOR_STYLE_CHOICES,
        blank=True,
        max_length=255,
    )

    LINK_SIZE_CHOICES = (
        ('btn-sm', _('Small')),
        ('', _('Medium')),
        ('btn-lg', _('Large')),
    )
    link_size = models.CharField(
        verbose_name=_('Size'),
        choices=LINK_SIZE_CHOICES,
        blank=True,
        max_length=255,
    )

    link_outline = models.BooleanField(
        verbose_name=_('No background'),
        default=False,
        help_text=_('Removes the button background, keeping only a coloured border.'),
    )

    link_block = models.BooleanField(
        verbose_name=_('Block'),
        default=False,
        help_text=_('Extends the button to the width of its container.'),
    )

    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
        excluded_keys=['href', 'title', 'target'],
    )

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
    )

    def __str__(self):
        if self.file_src and self.file_src.label:
            return self.file_src.label
        return str(self.pk)

    def get_short_description(self):
        if self.file_src and self.name:
            return self.name
        if self.file_src and self.file_src.label:
            return self.file_src.label
        return ugettext('<file is missing>')

    def copy_relations(self, oldinstance):
        # Because we have a ForeignKey, it's required to copy over
        # the reference from the instance to the new plugin.
        self.file_src = oldinstance.file_src


@python_2_unicode_compatible
class Folder(CMSPlugin):
    """
    Renders a folder plugin to the selected tempalte
    """
    template = models.CharField(
        verbose_name=_('Template'),
        choices=get_templates(),
        default=get_templates()[0][0],
        max_length=255,
    )
    folder_src = FilerFolderField(
        verbose_name=_('Folder'),
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    link_target = models.CharField(
        verbose_name=_('Link target'),
        choices=LINK_TARGET,
        blank=True,
        max_length=255,
        default='',
    )
    show_file_size = models.BooleanField(
        verbose_name=_('Show file size'),
        blank=True,
        default=False,
        help_text=_('Appends the file size at the end of the name.'),
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
        excluded_keys=['href', 'target'],
    )

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
    )

    def __str__(self):
        if self.folder_src and self.folder_src.name:
            return self.folder_src.name
        return str(self.pk)

    def get_short_description(self):
        if self.folder_src and self.folder_src.name:
            return self.folder_src.name
        return ugettext('<folder is missing>')

    def copy_relations(self, oldinstance):
        # Because we have a ForeignKey, it's required to copy over
        # the reference from the instance to the new plugin.
        self.folder_src = oldinstance.folder_src

    def get_files(self):
        folder_files = []
        if self.folder_src:
            for folder in self.folder_src.files:
                folder_files.append(folder)
        return folder_files
