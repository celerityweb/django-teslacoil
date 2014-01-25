# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

from django.contrib.messages.middleware import MessageMiddleware

class TeslaMessageMiddleware(MessageMiddleware):
    def process_response(self, request, response):
        add_header = hasattr(request, '_messages') and \
                     request._messages.added_new
        new_response  = super(TeslaMessageMiddleware, self).process_response(
            request, response)
        if add_header:
            new_response['X-Django-New-Messages'] = 'true'
        return new_response
