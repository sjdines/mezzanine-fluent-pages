from django.db import models
from django.template.loader import get_template
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from mezzanine.pages.models import Page

from . import appsettings, fields


@python_2_unicode_compatible
class PageLayout(models.Model):
    """
    A ``PageLayout`` object defines a template that can be used by a page.

    This was adapted from `fluent_pages/models/db.py` in the `django-fluent-pages` app.
    """
    key = models.SlugField(
        _('key'),
        help_text=_("A short name to identify the layout programmatically")
    )
    title = models.CharField(
        _('title'),
        max_length=255
    )
    template_path = fields.TemplateFilePathField(
        'template file',
        path=appsettings.MEZZANINE_PAGES_TEMPLATE_DIR
    )

    def get_template(self):
        """
        Return the template to render this layout.

        :return: Template object.
        """
        return get_template(self.template_path)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _('Layout')
        verbose_name_plural = _('Layouts')


class FluentContentsLayoutPage(Page):
    """
    A `Mezzanine` page type that uses template layouts.
    """
    layout = models.ForeignKey(
        'mezzanine_layout_page.PageLayout',
        verbose_name=_('Layout'),
    )

    class Meta:
        permissions = (
            ('change_page_layout', _('Can change Page layout')),
        )

    def get_template_name(self):
        """
        Return the template name (file path) to be used for rendering.

        :return: Template file path.
        """
        return self.layout.template_path
