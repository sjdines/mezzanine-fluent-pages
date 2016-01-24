from django.db import models

from . import forms


class TemplateFilePathField(models.FilePathField):
    """
    A field to select a template path.

    This was adapted from `fluent_pages/models/db.py` in the `django-fluent-pages` app.
    """
    def __init__(self, verbose_name=None, path='', **kwargs):
        """
        Update the file path field to only show HTML files.

        This enforces recursive lookups for the field.

        :param verbose_name: Verbose name for the field.
        :param path: The directory for file lookups.
        :param kwargs: Extra keyword arguments.
        :return: None.
        """
        defaults = dict(match=r'.*\.html$', recursive=True)
        defaults.update(kwargs)
        super(TemplateFilePathField, self).__init__(verbose_name, path=path, **defaults)

    def formfield(self, **kwargs):
        """
        Update the default form class.

        :param kwargs: Keyword arguments.
        :return: FormField instance.
        """
        # Like the FilePathField, the formfield does the actual work
        defaults = {'form_class': forms.TemplateFilePathFieldForm}
        defaults.update(kwargs)
        return super(TemplateFilePathField, self).formfield(**defaults)

    def deconstruct(self):
        """
        Deconstruction of field for `Django>=1.7` migration support.

        If this method is called with`Django<1.7` an `AttributeError`
        exception will be raised as the super field does not have
        this method.

        :return: Tuple of name, path, arguments and keyword arguments.
        """
        # For Django 1.7 migrations
        name, path, args, kwargs = super(TemplateFilePathField, self).deconstruct()
        if 'path' in kwargs:
            del kwargs["path"]
        return name, path, args, kwargs
