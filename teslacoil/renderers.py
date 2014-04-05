from rest_framework import renderers

class TeslaRenderer(renderers.JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = super(TeslaRenderer, self).render(
            data, accepted_media_type, renderer_context)
        return response
