import setuptools


setuptools.setup(
    name='mezzanine_fluent_pages',
    version='0.0.1',
    author='Stuart Dines',
    author_email='me@stuartdines.com',
    description='An implementation of a `mezzanine` page type using '
                '`django-fluent-contents`.',
    long_description=open('README.rst', 'rb').read().decode('utf-8'),
    packages=setuptools.find_packages(),
    install_requires=[
        'Mezzanine',
        'coverage',
        'django-fluent-contents[text]',
        'django-wysiwyg',
    ],
    extras_require={
        'dev': [
            'django-debug-toolbar',
            'ipdb',
            'ipython',
            'Werkzeug',
        ],
        'test': [
            'tox',
            'django-dynamic-fixture',
        ]
    },
)
