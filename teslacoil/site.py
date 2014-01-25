# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

import six
import django
from django.contrib.admin import site
from django.utils.text import capfirst
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import __version__ as teslacoil_version

class TeslaSite(object):
    """TeslaSite wraps a django AdminSite object to determine what model
    admin objects are registered and with what configuration."""

    def __init__(self, admin_site=site, name='tesla', app_name='tesla'):
        self.admin_site, self.name, self.app_name = admin_site, name, app_name

    _modeladmin_options = [
        'raw_id_fields',
        'fields',
        'exclude',
        'fieldsets',
        'filter_vertical',
        'filter_horizontal',
        'radio_fields',
        'prepopulated_fields',
        'readonly_fields',
        'ordering',
        'list_display',
        'list_display_links',
        'list_filter',
        'list_select_related',
        'list_per_page',
        'list_max_show_all',
        'list_editable',
        'search_fields',
        'date_hierarchy',
        'save_as',
        'save_on_top',
        'actions_on_top',
        'actions_on_bottom',
        'actions_selection_counter',
    ]

    @property
    def registry_config(self):
        try:
            return self._registered_app_map
        except AttributeError:
            registered_app_map = {}
            for model, model_admin in six.iteritems(self.admin_site._registry):
                meta = model._meta
                app_label = meta.app_label
                model_name = meta.object_name
                logger.debug('Registering ModelAdmin for %s.%s', app_label,
                             model_name)
                app_list = registered_app_map.setdefault(app_label, {})
                app_dict = app_list.setdefault(model_name, {})
                app_dict['verbose_name'] = capfirst(meta.verbose_name_plural),
                for option in self._modeladmin_options:
                    app_dict[option] = getattr(model_admin, option, None)
                logger.debug('Configuration dict for %s.%s is %s', app_label,
                             model_name, app_dict)
            self._registered_app_map = registered_app_map
            return registered_app_map

    def get_urls(self):
        from django.conf.urls import patterns, url, include

        urlpatterns = patterns(
            '',
            url('^_config/', api_view(['GET'])(self.site_config_view),
                name='site_config'),
        )

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    def site_config_view(self, request):
        return Response(self.site_config(request))

    def site_config(self, request):
        to_return = {
            'django_version': django.get_version(),
            'teslacoil_version': teslacoil_version,
            'apps': {}
        }
        apps = to_return['apps']
        for model, model_admin in six.iteritems(self.admin_site._registry):
            meta = model._meta
            app_label = meta.app_label
            model_name = meta.object_name
            has_module_perms = request.user.has_module_perms(app_label)
            if not has_module_perms: continue
            app_dict = apps.setdefault(app_label, {})
            perms = model_admin.get_model_perms(request)
            if not perms: continue
            model_dict = app_dict.setdefault(model_name, {})
            model_dict['perms'] = perms
            model_dict['config'] = self.registry_config[app_label][model_name]
        return to_return


