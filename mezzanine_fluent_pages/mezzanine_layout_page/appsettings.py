import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


# Configure the directory that the templates for for the layouts are available at.
MEZZANINE_PAGES_TEMPLATE_DIR = getattr(
    settings,
    'MEZZANINE_PAGES_TEMPLATE_DIR',
    settings.TEMPLATE_DIRS[0] if settings.TEMPLATE_DIRS else None
)

# Configure if relative directory templates should be used.
MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR = getattr(
    settings,
    'MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR',
    True
)


# Validate required settings.
if not MEZZANINE_PAGES_TEMPLATE_DIR:
    raise ImproperlyConfigured(
        _('The setting `MEZZANINE_PAGES_TEMPLATE_DIR` or `TEMPLATE_DIRS[0]` need to be defined!')
    )
else:
    # Clean settings
    MEZZANINE_PAGES_TEMPLATE_DIR = MEZZANINE_PAGES_TEMPLATE_DIR.rstrip('/') + '/'

    # Test whether the template dir for page templates exists.
    settingName = 'TEMPLATE_DIRS[0]'
    if hasattr(settings, 'MEZZANINE_PAGES_TEMPLATE_DIR'):
        settingName = 'MEZZANINE_PAGES_TEMPLATE_DIR'

    if not os.path.isabs(MEZZANINE_PAGES_TEMPLATE_DIR):
        raise ImproperlyConfigured(
            'The setting `{0}` needs to be an absolute path!'.format(settingName)
        )
    if not os.path.exists(MEZZANINE_PAGES_TEMPLATE_DIR):
        raise ImproperlyConfigured(
            'The path `{0}` in the setting `{1}` does not exist!'.format(
                MEZZANINE_PAGES_TEMPLATE_DIR,
                settingName
            )
        )
