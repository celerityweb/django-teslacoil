# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from teslacoil.renderers import TeslaRenderer

class TeslaModelAdminMixin(object):
    def response_post_save_add(self, request, obj):
        return obj


class TeslaModelAdminViewSet(viewsets.ViewSet):
    """
    Exposes an API for performing CRUD operations on Django model instances.

    Extends django-rest-framework's ViewSet and wraps Django's ModelAdmin.
    """

    # These are initialized by the site object
    model = None
    model_admin = None
    tesla_admin = None
    site = None

    def __init__(self, *args, **kwargs):
        super(TeslaModelAdminViewSet, self).__init__(*args, **kwargs)

        # generate a dynamic serializer class for the model
        self.ModelDataSerializer = type(
            'ModelDataSerializer',
            (serializers.ModelSerializer,),
            {'Meta': type('Meta', (object,), {'model': self.model})})

        # generate a dynamic wrapper around the ModelAdmin instance
        self.tesla_admin = type(
            'TeslaModelAdmin',
            (type(self.model_admin), TeslaModelAdminMixin),
            {}
        )(model=self.model_admin.model, opts=self.model_admin.opts,
          admin_site=self.model_admin.admin_site)

    @classmethod
    def as_view(cls, actions=None, **initkwargs):
        # Use TeslaRenderer for all views in ViewSet
        initkwargs['renderer_classes'] = [TeslaRenderer]
        return super(TeslaModelAdminViewSet, cls).as_view(
            actions, **initkwargs)

    def list(self, request):
        queryset = self.model_admin.get_queryset(request)
        serializer = self.ModelDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        response = self.model_admin.add_view(request)

        # Default context for add_view
        # context = dict(self.admin_site.each_context(),
        #     title=(_('Add %s') if add else _('Change %s')) % force_text(opts.verbose_name),
        #     adminform=adminForm,
        #     object_id=object_id,
        #     original=obj,
        #     is_popup=(IS_POPUP_VAR in request.POST or
        #               IS_POPUP_VAR in request.GET),
        #     to_field=request.POST.get(TO_FIELD_VAR,
        #                               request.GET.get(TO_FIELD_VAR)),
        #     media=media,
        #     inline_admin_formsets=inline_formsets,
        #     errors=helpers.AdminErrorList(form, formsets),
        #     preserved_filters=self.get_preserved_filters(request),
        # )

        # If the create succeeded, we would have the output from
        # model_admin.response_post_save_add and if there were validation errors,
        # it would be the output from model_admin.render_change_form
        #
        # In our TeslaModelAdminMixin, we expect the new object to have been
        # returned from the response_post_save_add call.
        if isinstance(response, self.model):
            url_name = '%s:%s-detail' % (self.site.name,
                                         self.model._meta.object_name.lower())
            return Response(status=201,
                            headers={'location': reverse(url_name,
                                                         args=[response.pk])})
        elif isinstance(response, TemplateResponse):
            # There must have been validation errors.
            ctx = response.context
            return Response(status=400,
                            data=ctx['errors'].as_json())

    def retrieve(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).retrieve(request, pk)

    def update(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).update(request, pk)

    def partial_update(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).partial_update(request, pk)

    def destroy(self, request, pk=None):
        return super(TeslaModelAdminViewSet, self).destroy(request, pk)
