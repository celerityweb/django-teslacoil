# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django import http

def add_message_view(request):
    if not request.user:
        user = authenticate(username=settings.TEST_USER_USERNAME,
                            password=settings.TEST_USER_PASSWORD)
        login(request, user)
    messages.info(request, 'Test message')
    return http.HttpResponse('Success.', content_type='text/plain')

def noop_view(request):
    if not request.user:
        user = authenticate(username=settings.TEST_USER_USERNAME,
                            password=settings.TEST_USER_PASSWORD)
        login(request, user)
    return http.HttpResponse('Success.', content_type='text/plain')
