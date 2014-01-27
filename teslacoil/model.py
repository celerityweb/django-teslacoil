# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

from rest_framework import serializers, viewsets
from rest_framework.response import Response

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

        self.ModelSchemaSerializer = None

        class TeslaModelSerializer(serializers.Serializer):
            schema = self.ModelSchemaSerializer
            objects = self.ModelDataSerializer

        self.ModelSerializer = TeslaModelSerializer

    def list(self, request):
        queryset = self.model_admin.get_queryset(request)
        serializer = self.ModelDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        return super(TeslaModelAdminViewSet, self).create(request)

    def retrieve(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).retrieve(request, pk)

    def update(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).update(request, pk)

    def partial_update(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).partial_update(request, pk)

    def destroy(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).destroy(request, pk)
