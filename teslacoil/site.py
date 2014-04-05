# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

import six
import django
from django.contrib.admin import site
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.api import get_messages
from django.utils.text import capfirst
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.routers import DefaultRouter
from teslacoil.viewsets import TeslaModelAdminViewSet

from . import __version__ as teslacoil_version

class LoginViewPermissions(IsAdminUser):
    def has_permission(self, request, view):
        if request.method == 'POST': # POST is what they use to login
            return True
        return super(LoginViewPermissions, self).has_permission(request, view)

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
            url('^_messages/', api_view(['GET'])(self.user_messages_view),
                name='site_messages'),
            url('^_session/',
                api_view(['GET', 'POST', 'DELETE'])(self.session_view),
                name='site_session'),
        )

        # add url patterns for Django models
        router = DefaultRouter()

        for model, model_admin in six.iteritems(self.admin_site._registry):
            # instantiate a dynamic ViewSet for `model_admin`
            ModelAdminViewSet = type(
                'ModelAdminViewSet',
                (TeslaModelAdminViewSet,),
                {'model': model, 'model_admin': model_admin, 'site': self})

            # create routes for the dynamic ViewSet
            router.register(r'^{app_name}/{model_name}'.format(
                    app_name=model._meta.app_label,
                    model_name=model._meta.module_name),
                ModelAdminViewSet)

        urlpatterns += router.urls

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name

    @permission_classes([IsAdminUser])
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

    @permission_classes([IsAdminUser])
    def user_messages_view(self, request):
        return Response(
            {'messages': [
                {'level': message.level,
                 'message': message.message,
                 'extra_tags': message.extra_tags}
                for message in get_messages(request)]})

    def _current_user_data(self, request):
        return {
            'pk': request.user.pk,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_superuser': request.user.is_superuser}

    @permission_classes([LoginViewPermissions])
    def session_view(self, request):
        if request.method == 'GET':
            return Response(self._current_user_data(request)
            )
        elif request.method == 'POST':
            form_obj = AuthenticationForm(request, request.DATA)
            # TODO: Make sure view that sends static HTML sets test cookie
            if form_obj.is_valid():
                login(request, form_obj.user_cache)
                return Response(self._current_user_data(request), status=201)
            return Response(form_obj.errors, status=403)
        elif request.method == 'DELETE':
            logout(request)
            return Response({}, status=205)

