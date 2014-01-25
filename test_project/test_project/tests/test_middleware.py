# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

__all__ = ['TestMessagesMiddleware']

class TestMessagesMiddleware(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(settings.TEST_USER_USERNAME,
                                             settings.TEST_USER_EMAIL,
                                             settings.TEST_USER_PASSWORD)

    def test_messages_header(self):
        response = self.client.get(reverse('add-message'))
        self.assertEqual(response.status_code, 200)
        self.assert_('X-Django-New-Messages' in response)
        logger.debug('X-Django-New-Messages found when message was added')

        response = self.client.get(reverse('noop-view'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('X-Django-New-Messages' in response)
        logger.debug('X-Django-New-Messages absent when message was not added')


