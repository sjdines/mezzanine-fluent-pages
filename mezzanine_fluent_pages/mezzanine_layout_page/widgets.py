from django.forms.widgets import Select


class LayoutSelector(Select):
    """
    Modified `Select` class to select the original value.

    This was adapted from `fluent_pages/pagetypes/fluent_pages/widgets
    .py` in the `django-fluent-pages` app.
    """
    def render(self, name, value, attrs=None, choices=()):
        """
        Modified render to set the data original value.

        :param name: The name of the `Select` field.
        :param value: The value of the `Select` field.
        :param attrs: Additional attributes of the `Select` field.
        :param choices: Available choices for the `Select` field.
        :return: HTML select.
        """
        if attrs:
            attrs['data-original-value'] = value
        return super(LayoutSelector, self).render(name, value, attrs, choices)
