# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine_fluent_pages.mezzanine_layout_page.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='FluentContentsLayoutPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
            ],
            options={
                'ordering': ('_order',),
                'permissions': (('change_page_layout', 'Can change Page layout'),),
            },
            bases=('pages.page',),
        ),
        migrations.CreateModel(
            name='PageLayout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.SlugField(help_text='A short name to identify the layout programmatically', verbose_name='key')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('template_path', mezzanine_fluent_pages.mezzanine_layout_page.fields.TemplateFilePathField(verbose_name=b'template file', recursive=True, match=b'.*\\.html$')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Layout',
                'verbose_name_plural': 'Layouts',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fluentcontentslayoutpage',
            name='layout',
            field=models.ForeignKey(verbose_name='Layout', to='mezzanine_layout_page.PageLayout'),
            preserve_default=True,
        ),
    ]
