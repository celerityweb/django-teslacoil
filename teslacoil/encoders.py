# TODO: do we still need this?

from django.contrib.admin import ModelAdmin
from django.db.models.base import ModelBase
from rest_framework.utils import encoders

class TeslaEncoder(encoders.JSONEncoder):

    def default(self, o):
        if isinstance(o, ModelAdmin):
            _data = {}
            _data['model'] =  '{module_name}.{model_name}'.format(
                    module_name=o.model.__module__,
                    model_name=o.model._meta.model_name)
            _data['fields'] = []
            for field in o.model._meta.fields:
                _field_data = {}
                _field_data['name'] = field.name
                _field_data['help_text'] = field.help_text
                _field_data['unique'] = field.unique

                if field.max_length:
                    _field_data['max_length'] = field.max_length

                _data['fields'].append(_field_data)
            return _data
        return super(TeslaEncoder, self).default(o)
