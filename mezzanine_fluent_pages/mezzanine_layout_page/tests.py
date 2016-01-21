from django.conf import settings
from django.contrib import admin as django_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.template import TemplateDoesNotExist
from django.test import TestCase
from django.utils import six
from django_dynamic_fixture import G
from mezzanine_fluent_pages.mezzanine_layout_page.admin import FluentContentsLayoutPageAdmin

from . import appsettings, admin, fields, forms, models, widgets


User = get_user_model()


class Admin(TestCase):
    def setUp(self):
        self.admin_instance = admin.FluentContentsLayoutPageAdmin(
            models.FluentContentsLayoutPage,
            django_admin.site
        )

    def test_fluentcontentslayoutpageadmin_get_placeholder_data(self):
        self.assertEqual(self.admin_instance.get_placeholder_data(None, None), [])

        layout = G(
            models.PageLayout,
            template_path='layouts/default.html'
        )
        layout_page = G(
            models.FluentContentsLayoutPage,
            layout=layout
        )

        self.assertEqual(len(self.admin_instance.get_placeholder_data(None, layout_page)), 1)

        layout_page.delete()
        layout.delete()

    def test_fluentcontentslayoutpageadmin_formfield_for_foreignkey(self):
        self.assertIsInstance(
            self.admin_instance.formfield_for_foreignkey(
                models.FluentContentsLayoutPage.layout.field
            ).widget,
            widgets.LayoutSelector
        )
        self.assertNotIsInstance(
            self.admin_instance.formfield_for_foreignkey(
                models.FluentContentsLayoutPage.site.field
            ).widget,
            widgets.LayoutSelector
        )

    def test_fluentcontentslayoutpageadmin_get_urls(self):
        self.assertEqual(
            len(self.admin_instance.get_urls()),
            len(super(FluentContentsLayoutPageAdmin, self.admin_instance).get_urls()) + 1
        )

    def test_fluentcontentslayoutpageadmin_get_layout_view(self):
        layout = G(
            models.PageLayout,
            template_path='layouts/default.html'
        )
        response = self.admin_instance.get_layout_view(None, 999)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.jsondata['success'])
        self.assertEqual(response.jsondata['error'], 'Layout not found')

        response = self.admin_instance.get_layout_view(None, layout.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.jsondata['placeholders'][0]['slot'], 'main')
        self.assertEqual(response.jsondata['placeholders'][0]['role'], 'm')
        self.assertEqual(response.jsondata['placeholders'][0]['allowed_plugins'], [])
        self.assertEqual(response.jsondata['placeholders'][0]['fallback_language'], None)
        self.assertEqual(response.jsondata['placeholders'][0]['title'], 'Main')
        self.assertEqual(response.jsondata['id'], 1)
        self.assertEqual(response.jsondata['key'], '1')
        self.assertEqual(response.jsondata['title'], '1')
        layout.delete()

    def test_fluentcontentslayoutpageadmin_get_readonly_fields(self):
        layout = G(
            models.PageLayout,
            template_path='layouts/default.html'
        )
        layout_page = G(
            models.FluentContentsLayoutPage,
            layout=layout
        )
        read_only_fields = self.admin_instance.get_readonly_fields(None, None)
        self.assertEqual(read_only_fields, ())
        request = HttpRequest()
        request.user = AnonymousUser()
        read_only_fields = self.admin_instance.get_readonly_fields(request, layout_page)
        self.assertEqual(read_only_fields, ('layout',))
        layout_page.delete()
        layout.delete()
        del request

    def test_fluentcontentslayoutpageadmin_has_change_page_layout_permission(self):
        layout = G(
            models.PageLayout,
            template_path='layouts/default.html'
        )
        layout_page = G(
            models.FluentContentsLayoutPage,
            layout=layout
        )
        request = HttpRequest()
        request.user = AnonymousUser()
        self.assertFalse(
            self.admin_instance.has_change_page_layout_permission(request, layout_page)
        )
        user = G(
            User,
            is_staff=True,
            is_active=True,
            is_superuser=True
        )
        request.user = user
        self.assertTrue(
            self.admin_instance.has_change_page_layout_permission(request, layout_page)
        )
        del request
        user.delete()
        layout_page.delete()
        layout.delete()


class AppSettings(TestCase):
    def test_mezzanine_pages_template_configuration(self):
        with self.settings(MEZZANINE_PAGES_TEMPLATE_DIR=None):
            with self.assertRaises(ImproperlyConfigured) as cm:
                six.moves.reload_module(appsettings)
            self.assertEqual(
                str(cm.exception),
                'The setting `MEZZANINE_PAGES_TEMPLATE_DIR` or `TEMPLATE_DIRS[0]` need to be '
                'defined!'
            )

        with self.settings(MEZZANINE_PAGES_TEMPLATE_DIR='./test/'):
            with self.assertRaises(ImproperlyConfigured) as cm:
                six.moves.reload_module(appsettings)
            self.assertEqual(
                str(cm.exception),
                'The setting `MEZZANINE_PAGES_TEMPLATE_DIR` needs to be an absolute path!'
            )

        with self.settings(MEZZANINE_PAGES_TEMPLATE_DIR='/test/'):
            with self.assertRaises(ImproperlyConfigured) as cm:
                six.moves.reload_module(appsettings)
            self.assertEqual(
                str(cm.exception),
                'The path `/test/` in the setting `MEZZANINE_PAGES_TEMPLATE_DIR` does not exist!'
            )

        with self.settings(TEMPLATE_DIRS=('./test/', )):
            mezzanine_pages_template_dir = settings.MEZZANINE_PAGES_TEMPLATE_DIR
            del settings.MEZZANINE_PAGES_TEMPLATE_DIR

            with self.assertRaises(ImproperlyConfigured) as cm:
                six.moves.reload_module(appsettings)
            self.assertEqual(
                str(cm.exception),
                'The setting `TEMPLATE_DIRS[0]` needs to be an absolute path!'
            )

            settings.MEZZANINE_PAGES_TEMPLATE_DIR = mezzanine_pages_template_dir

        six.moves.reload_module(appsettings)


class Fields(TestCase):
    def setUp(self):
        self.field = fields.TemplateFilePathField(path=appsettings.MEZZANINE_PAGES_TEMPLATE_DIR)

    def test_templatefilepathfield_init(self):
        self.assertEqual(self.field.recursive, True)
        self.assertEqual(self.field.match, r'.*\.html$')

    def test_templatefilepathfield_formfield(self):
        self.assertIsInstance(self.field.formfield(), forms.TemplateFilePathFieldForm)

    def test_templatefilepathfield_deconstruct(self):
        self.assertEqual(
            self.field.deconstruct(),
            (
                None,
                u'mezzanine_fluent_pages.mezzanine_layout_page.fields.TemplateFilePathField',
                [],
                {
                    u'recursive': True,
                    u'match': '.*\\.html$'
                }
            )
        )


class Forms(TestCase):
    def test_templatefilepathfieldform_init(self):
        appsettings.MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR = False

        form = forms.TemplateFilePathFieldForm(
            path=appsettings.MEZZANINE_PAGES_TEMPLATE_DIR,
            recursive=True
        )

        self.assertEqual(
            form.choices,
            [
                (
                    '%sadmin/fluent_mezzanine/change_form.html' %
                    appsettings.MEZZANINE_PAGES_TEMPLATE_DIR,
                    u'admin/fluent_mezzanine/change_form.html'
                ),
                (
                    '%slayouts/default.html' % appsettings.MEZZANINE_PAGES_TEMPLATE_DIR,
                    u'layouts/default.html'
                )
            ]
        )

        appsettings.MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR = True

        form = forms.TemplateFilePathFieldForm(
            path=appsettings.MEZZANINE_PAGES_TEMPLATE_DIR,
            recursive=True
        )

        self.assertEqual(
            form.choices,
            [
                (
                    'admin/fluent_mezzanine/change_form.html',
                    u'admin/fluent_mezzanine/change_form.html'
                ),
                (
                    'layouts/default.html',
                    u'layouts/default.html'
                )
            ]
        )

    def test_templatefilepathfieldform_prepare_value(self):
        appsettings.MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR = False
        form = forms.TemplateFilePathFieldForm(
            path=appsettings.MEZZANINE_PAGES_TEMPLATE_DIR,
            recursive=True
        )

        self.assertEqual(form.prepare_value(None), None)
        self.assertEqual(
            form.prepare_value('%slayouts/default.html' % appsettings.MEZZANINE_PAGES_TEMPLATE_DIR),
            '%slayouts/default.html' % appsettings.MEZZANINE_PAGES_TEMPLATE_DIR,
        )
        self.assertEqual(
            form.prepare_value('layouts/default.html'),
            '%slayouts/default.html' % appsettings.MEZZANINE_PAGES_TEMPLATE_DIR,
        )
        appsettings.MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR = True
        form = forms.TemplateFilePathFieldForm(
            path=appsettings.MEZZANINE_PAGES_TEMPLATE_DIR,
            recursive=True
        )
        self.assertEqual(
            form.prepare_value('%slayouts/default.html' % appsettings.MEZZANINE_PAGES_TEMPLATE_DIR),
            'layouts/default.html'
        )
        self.assertEqual(
            form.prepare_value('layouts/default.html'),
            'layouts/default.html'
        )


class Models(TestCase):
    def setUp(self):
        self.layout = G(
            models.PageLayout
        )
        self.layout_page = G(
            models.FluentContentsLayoutPage,
            layout=self.layout
        )

    def tearDown(self):
        self.layout_page.delete()
        self.layout.delete()

    def test_fluentcontentslayoutpage_get_template_name(self):
        # Test to see if template to be used is respected.
        self.assertEqual(
            self.layout_page.get_template_name(),
            self.layout.template_path
        )

    def test_pagelayout_get_template(self):
        # Test to see if fake template raises an exception.
        with self.assertRaises(TemplateDoesNotExist):
            self.layout.get_template()

        # Test to see if real template returns a template.
        template_path = 'layouts/default.html'
        layout = models.PageLayout.objects.create(
            key='key',
            title='title',
            template_path=template_path
        )
        self.assertEqual(layout.get_template().template.name, template_path)

    def test_str(self):
        # Test the string representations for models.
        self.assertEqual(str(self.layout), self.layout.title)
        self.assertEqual(str(self.layout_page), self.layout_page.titles)


class Widgets(TestCase):
    def test_layout_selector_renders(self):
        ls = widgets.LayoutSelector()

        # Test to see that the value gets set as the `data-original-value`.
        self.assertEqual(
            ls.render(
                'name',
                'value',
                {
                    'data-original-value': 'fake value'
                },
            ),
            '<select data-original-value="value" name="name">\n</select>'
        )

        # Test to see the code operates without `attrs` specified.
        self.assertEqual(
            ls.render(
                'name',
                'value',
            ),
            '<select name="name">\n</select>'
        )
