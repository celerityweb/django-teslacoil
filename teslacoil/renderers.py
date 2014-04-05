from djangojsonschema.jsonschema import DjangoFormToJSONSchema
from rest_framework import renderers
from teslacoil.encoders import TeslaEncoder


class TeslaRenderer(renderers.JSONRenderer):

    encoder_class = TeslaEncoder

    def render(self, data, accepted_media_type=None, renderer_context=None):
        model_admin = renderer_context['view'].model_admin
        request = renderer_context['request']
        schema = DjangoFormToJSONSchema().convert_form(
            model_admin.get_form(request))

        response_wrapper = {
            'meta': schema,
            'objects': data,
        }

        return super(TeslaRenderer, self).render(
            response_wrapper, accepted_media_type, renderer_context)
