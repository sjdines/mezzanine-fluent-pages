import os
from django import forms

from . import appsettings


class TemplateFilePathFieldForm(forms.FilePathField):
    """
    The associated formfield to select a template path.

    This was adapted from `fluent_pages/forms/fields.py` in the
    `django-fluent-pages` app.
    """
    def __init__(self, *args, **kwargs):
        """
        Override choices to make them relative if desired.

        This has been modified from the `fluent_pages` version to use a
        different setting name.

        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: None
        """
        # If path is `None` it will cause a `TypeError` when it tries to coerce it to unicode
        # in `Django<1.8` when it calls `listdir(top)`.
        if kwargs['path'] is None:
            kwargs['path'] = ''

        super(TemplateFilePathFieldForm, self).__init__(*args, **kwargs)
        # Make choices relative if requested.
        if appsettings.MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR:
            self.choices.sort(key=lambda choice: choice[1])
            self.choices = self.widget.choices = [
                (filename.replace(self.path, '', 1), title) for filename, title in self.choices
            ]

    def prepare_value(self, value):
        """
        Allow effortlessly switching between relative and absolute paths.

        This has been modified from the `fluent_pages` version to use a
        different setting name.

        :param value: The value selected.
        :return: The value selected (either absolute or relative).
        """
        if value is not None:
            if appsettings.MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR:
                # Turn old absolute paths into relative paths.
                if os.path.isabs(value) and value.startswith(self.path):
                    value = value[len(self.path):].lstrip('/')
            else:
                # If setting is disabled, turn relative path back to abs.
                if not os.path.isabs(value):
                    value = os.path.join(self.path, value)
        return value
