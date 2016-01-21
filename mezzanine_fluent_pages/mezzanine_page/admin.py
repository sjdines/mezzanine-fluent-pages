from django.contrib import admin
from fluent_contents.admin import PlaceholderFieldAdmin
from mezzanine.pages.admin import PageAdmin

from . import models


class FluentContentsPageAdmin(PlaceholderFieldAdmin, PageAdmin):
    """
    Admin definition for `FluentContentsPage`.
    """
    fieldsets = PageAdmin.fieldsets + (
        (
            None,
            {
                'fields': ['content', ]
            }
        ),
    )

admin.site.register(models.FluentContentsPage, FluentContentsPageAdmin)
