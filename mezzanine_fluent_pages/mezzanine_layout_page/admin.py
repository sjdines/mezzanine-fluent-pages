from django.conf.urls import url
from django.contrib import admin
from fluent_contents.admin import PlaceholderEditorAdmin
from fluent_contents.analyzer import get_template_placeholder_data
from fluent_utils.ajax import JsonResponse
from mezzanine.pages.admin import PageAdmin

from . import models, widgets


class FluentContentsLayoutPageAdmin(PlaceholderEditorAdmin, PageAdmin):
    """
    Admin configuration for `FluentContentsLayoutPage`.
    """
    # The `change_form_template` is overwritten to include the content type id in the JS which is
    # used in the fluent ajax calls.
    change_form_template = 'admin/fluent_mezzanine/change_form.html'

    class Media:
        # This is a custom JS adaption of the `fluent_layouts.js` found in
        # `fluent_pages.fluentpage`. The only modification is to change the `app_root` variable
        # declaration to a new endpoint. The rest of the code has been used here so `fluent_pages`
        # is not a requirement to use this package.
        js = ('fluent_mezzanine/fluent_layouts.js',)

    def get_placeholder_data(self, request, obj=None):
        """
        Provides a list of `fluent_contents.models.PlaceholderData`
        classes, that describe the contents of the template.

        :param request: Django request object.
        :param obj: Object to get place holder data from.
        :return: list of `~fluent_contents.models.PlaceholderData`
        """
        template = self.get_page_template(obj)
        if not template:
            return []  # No template means no data!
        else:
            return get_template_placeholder_data(template)

    def get_page_template(self, page):
        """
        Return the template that is associated with the page.

        If no page is provided then the first available template will
        be used as defined in `PageLayout`. If not `PageLayout` exists
        then `None` will be returned.

        :param page: Page object to obtain the template from.
        :return: Template object or None.
        """
        if page is None:
            # Add page. start with default template.
            try:
                return models.PageLayout.objects.all()[0].get_template()
            except IndexError:
                return None
        else:
            # Change page, honor template of object.
            return page.layout.get_template()

    # ---- Layout selector code ----

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Overwrite the widget for the `layout` foreign key.

        :param db_field: Field on the object.
        :param request: Django request object.
        :param kwargs: Extra keyword arguments.
        :return: Formfield.
        """
        if db_field.name == 'layout':
            kwargs['widget'] = widgets.LayoutSelector
        return super(FluentContentsLayoutPageAdmin, self).formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )

    def get_urls(self):
        """
        Add URL pattern for obtaining layout information.

        :return: List of URL patterns.
        """
        urls = super(FluentContentsLayoutPageAdmin, self).get_urls()
        my_urls = [
            url(
                r'^get_layout/(?P<id>\d+)/$',
                self.admin_site.admin_view(self.get_layout_view),
                name='get_layout',
            )
        ]
        return my_urls + urls

    def get_layout_view(self, request, id):
        """
        Return the metadata about a layout

        :param request: Django request object.
        :param id: Id integer value (pk) for the layout referenced.
        :return: JsonResponse with layout information or error message.
        """
        # Get the layout or if it does not exist return an error message.
        try:
            layout = models.PageLayout.objects.get(pk=id)
        except models.PageLayout.DoesNotExist:
            json = {'success': False, 'error': 'Layout not found'}
            status = 404
        else:
            template = layout.get_template()
            placeholders = get_template_placeholder_data(template)

            status = 200
            # Set useful information regarding the layout.
            json = {
                'id': layout.id,
                'key': layout.key,
                'title': layout.title,
                'placeholders': [p.as_dict() for p in placeholders],
            }

        return JsonResponse(json, status=status)

    # ---- Layout permission hooks ----

    def get_readonly_fields(self, request, obj=None):
        """
        Allow layout modification on initial creation only if no perms.

        If the user does not have the privilege to access the layout
        field initially we need to overwrite that as it is a required
        field.

        After it is set we can return to the default behaviour.

        :param request: Django request object.
        :param obj: Object instance that uses layout fields.
        :return: List of read only fields.
        """
        fields = super(FluentContentsLayoutPageAdmin, self).get_readonly_fields(request, obj)

        if (
            obj is not None and
            'layout' not in fields and
            not self.has_change_page_layout_permission(request, obj)
        ):
            # Disable on edit page only.
            # Add page is allowed, need to be able to choose initial layout
            fields = fields + ('layout',)
        return fields

    def has_change_page_layout_permission(self, request, obj):
        """
        Whether the user can change the page layout.

        :param request: Django request object.
        :param obj: Object instance that uses layout fields.
        :return: Boolean (True if user has permission to change
        the layout; False if the user does not have permission to
        change the layout).
        """
        codename = '{0}.change_page_layout'.format(obj._meta.app_label)
        return request.user.has_perm(codename, obj=obj)


class PageLayoutAdmin(admin.ModelAdmin):
    """
    Admin configuration for `PageLayout` model.
    """
    # Config list page:
    list_display = ['title', 'key', ]
    fieldsets = (
        (
            None, {
                'fields': (
                    'title',
                    'key',
                    'template_path'
                ),
            }
        ),
    )
    prepopulated_fields = {
        'key': (
            'title',
        )
    }


# Admin registration.
admin.site.register(models.FluentContentsLayoutPage, FluentContentsLayoutPageAdmin)
admin.site.register(models.PageLayout, PageLayoutAdmin)
