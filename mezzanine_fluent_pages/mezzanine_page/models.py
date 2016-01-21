from fluent_contents.models import PlaceholderField
from mezzanine.pages.models import Page


class FluentContentsPage(Page):
    """
    A mezzanine `Page` type with fluent contents.
    """
    content = PlaceholderField('mezzanine_page_content')

    def get_template_name(self):
        """
        Obtain the template to use for front end rendering.

        :return: String of template location.
        """
        return 'fluent_mezzanine/fluent_contents_page.html'
