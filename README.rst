.. image:: https://secure.travis-ci.org/sjdines/mezzanine-fluent-pages.png?branch=master
   :target: http://travis-ci.org/sjdines/mezzanine-fluent-pages

Mezzanine Fluent Pages
======================

Introduction
------------

`Mezzanine <https://github.com/stephenmcd/mezzanine>`__ is a content
management platform that provides a single yet highly extensible
architecture. With in the project there are different types of pages
geared towards achieving a task.

`Fluent Contents <https://github.com/edoburu/django-fluent-contents>`__ offers
a widget engine to display various content on a page built in
``Django``.

This project bridges the two providing page types for
`Mezzanine <https://github.com/stephenmcd/mezzanine>`__ that utilize
`Fluent Contents <https://github.com/edoburu/django-fluent-contents>`__
for the page data.

There are two (2) different implementations provided within this project
(which are discussed in more detail further on):

-  ``mezzanine_page``
-  ``mezzanine_layout_page``

These page implementations borrow heavily from
`Fluent Pages <https://github.com/edoburu/django-fluent-pages>`__
but have been kept purposely separate due to the overheads of installing
`Fluent Pages <https://github.com/edoburu/django-fluent-pages>`__.
The ideal would be to move this common code into the
`Fluent Utils <https://github.com/edoburu/django-fluent-utils>`__
package but that is not currently in the purview of this project.

Page types
----------

There are currently two (2) page types:

-  ``mezzanine_page``
-  ``mezzanine_layout_page``

``mezzanine_page``.
~~~~~~~~~~~~~~~~~~~

``mezzanine_page`` provides a single content region for use on the page
which content plugins can be used for.

It has not been made in a readily extensible manner as it is quite
minimal and if you want a more tailored solution you are better off
copying the app into your project and making relevant modifications.

Refer to the
`Fluent Contents <https://github.com/edoburu/django-fluent-contents>`__
app in regards to creating content plugins and limiting plugin
availability.

``mezzanine_layout_page``
~~~~~~~~~~~~~~~~~~~~~~~~~

``mezzanine_layout_page`` provides the ability to have different
templates used for the particular page and the regions available
specified on the templates themselves. This allows for the complete
customisation of the regions needed and the content plugins available to
them.

Refer to the
`Fluent Contents <https://github.com/edoburu/django-fluent-contents>`__
app in regards to creating content plugins and limiting plugin
availability.

Settings
^^^^^^^^

``MEZZANINE_PAGES_TEMPLATE_DIR``
''''''''''''''''''''''''''''''''

``MEZZANINE_PAGES_TEMPLATE_DIR`` allows the specification of the folder
to use to find available layouts for layout creation. If not value is
specified it will fallback to the first listing in the ``TEMPLATE_DIRS``
settings. If that doest not exist an exception will be raised.

The value should consist of the string path to the template directory.

``MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR`` allows the option to allow
relative directories.

It is a boolean flag defaulting to ``True``.

Installation
~~~~~~~~~~~~

To install ``mezzanine_fluent_pages`` run:

::

    pip install -e git+ssh://git@github.com/sjdines/mezzanine-fluent-pages#egg=mezzanine-fluent-pages

Please note that with Django versions 1.8 and 1.9 require specific versions of `html5lib`.
Installation can be done with the following:

::

    pip install -e git+ssh://git@github.com/sjdines/mezzanine-fluent-pages#egg=mezzanine-fluent-pages[html5libpin]

Then add the page type(s) you wish to ``INSTALLED_APPS``:

::

    INSTALLED_APPS += (
        'mezzanine_fluent_pages.mezzanine_page',
        'mezzanine_fluent_pages.mezzanine_layout_page',
    )

Define the location of ``MEZZANINE_PAGES_RELATIVE_TEMPLATE_DIR`` if
required (see above).

Run migrations:

::

    $ python manage.py migrate

It's ready to go!

Supported Versions
~~~~~~~~~~~~~~~~~~
