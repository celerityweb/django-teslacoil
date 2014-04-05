# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

from rest_framework import serializers, viewsets
from rest_framework.response import Response
from teslacoil.renderers import TeslaRenderer

class TeslaModelAdminViewSet(viewsets.ViewSet):
    """
    Exposes an API for performing CRUD operations on Django model instances.

    Extends django-rest-framework's ViewSet and wraps Django's ModelAdmin.
    """

    def __init__(self, *args, **kwargs):
        super(TeslaModelAdminViewSet, self).__init__(*args, **kwargs)

        # generate a dynamic serializer class for the model
        self.ModelDataSerializer = type('ModelDataSerializer', (serializers.ModelSerializer,), {
            'Meta': type('Meta', (object,), {
                'model': self.model,
            })
        })

    #@classmethod
    #def as_view(cls, actions=None, **initkwargs):
    #    # Use TeslaRenderer for all views in ViewSet
    #    initkwargs['renderer_classes'] = [TeslaRenderer]
    #    return super(TeslaModelAdminViewSet, cls).as_view(
    #        actions, **initkwargs)

    def list(self, request):
        queryset = self.model_admin.get_queryset(request)
        serializer = self.ModelDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        return super(TeslaModelAdminViewSet, self).create(request)

    def retrieve(self, request, pk=None):
        #obj = self.model_admin.get_object(request, pk)
        #change_form = self.model_admin.get_form(request, obj)
        response = self.model_admin.change_view(request, pk)
        ctx = response.context_data
        change_form = ctx['adminform']

        return Response(change_form.form.initial)

    def update(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).update(request, pk)

    def partial_update(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).partial_update(request, pk)

    def destroy(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).destroy(request, pk)
