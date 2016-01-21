from django.test import TestCase

from . import models


class Models(TestCase):
    def test_get_template_name(self):
        self.assertEqual(
            models.FluentContentsPage().get_template_name(),
            'fluent_mezzanine/fluent_contents_page.html'
        )
