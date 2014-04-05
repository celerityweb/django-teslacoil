from rest_framework import renderers
from teslacoil.encoders import TeslaEncoder


class TeslaRenderer(renderers.JSONRenderer):

    encoder_class = TeslaEncoder

    def render(self, data, accepted_media_type=None, renderer_context=None):
        model = renderer_context['view'].model
        model_admin = renderer_context['view'].model_admin
        request = renderer_context['request']

        response_wrapper = {
            'meta': model_admin,
            'objects': data,
        }

        return super(TeslaRenderer, self).render(
            response_wrapper, accepted_media_type, renderer_context)
