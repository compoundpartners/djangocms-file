# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .helpers import concat_classes
from .models import File, Folder
from .forms import FileForm


class FilePlugin(CMSPluginBase):
    model = File
    form = FileForm
    name = _('File')
    change_form_template = 'djangocms_file/admin/link.html'
    text_enabled = True

    fieldsets = [
        (None, {
            'fields': (
                'file_src',
                ('name', 'link_type'),
                'description',
                'terms',
                ('link_context'),
                ('link_size', 'link_outline'),
                ('link_block', 'show_file_size'),
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'template',
                ('link_target', 'link_title'),
                'attributes',
            )
        }),
    ]

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_file/{}/file.html'.format(instance.template)

    def render(self, context, instance, placeholder):
        link_classes = []
        if instance.link_context:
            if instance.link_type == 'link':
                link_classes.append('text-{}'.format(instance.link_context))
            else:
                link_classes.append('btn')
                if not instance.link_outline:
                    link_classes.append(
                        'btn-{}'.format(instance.link_context)
                    );
                else:
                    link_classes.append(
                        'btn-outline-{}'.format(instance.link_context)
                    );
        if instance.link_size:
            link_classes.append(instance.link_size);
        if instance.link_block:
            link_classes.append('btn-block');

        classes = concat_classes(link_classes + [
            instance.attributes.get('class'),
        ])
        instance.attributes['class'] = classes

        # Check if (Aldryn) Google Tag Manager (GTM) is installed, and pass to template
        if 'aldryn_google_tag_manager' in settings.INSTALLED_APPS:
            context['gtm_installed'] = True

        return super(FilePlugin, self).render(
            context, instance, placeholder
        )


class FolderPlugin(CMSPluginBase):
    model = Folder
    name = _('Folder')
    text_enabled = True

    fieldsets = [
        (None, {
            'fields': (
                'folder_src',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'template',
                'link_target',
                'show_file_size',
                'attributes',
            )
        }),
    ]

    def render(self, context, instance, placeholder):
        context['folder_files'] = instance.get_files()
        return super(FolderPlugin, self).render(context, instance, placeholder)

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_file/{}/folder.html'.format(instance.template)


plugin_pool.register_plugin(FilePlugin)
plugin_pool.register_plugin(FolderPlugin)
