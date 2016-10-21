# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-21 23:30
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        ('forum', '0001_initial'),
        ('pm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('emailVisible', models.BooleanField(default=False, verbose_name='E-mail visible')),
                ('subscribeToEmails', models.BooleanField(default=True, verbose_name='Mailing-list')),
                ('mpEmailNotif', models.BooleanField(default=False, verbose_name='Notification des MP par e-mail')),
                ('showSmileys', models.BooleanField(default=False, verbose_name='Affichage des smileys par defaut')),
                ('fullscreen', models.BooleanField(default=False, verbose_name="Utilisation de la largeur de l'écran")),
                ('showLogosOnSmartphone', models.BooleanField(default=True, verbose_name='Afficher les logos sur smartphone')),
                ('logo', models.ImageField(blank=True, upload_to='logo')),
                ('quote', models.CharField(blank=True, max_length=50, verbose_name='Citation')),
                ('website', models.URLField(blank=True, verbose_name='Site web')),
                ('pmUnreadCount', models.IntegerField(default=0)),
                ('resetDateTime', models.DateTimeField(default=datetime.datetime(2013, 1, 1, 0, 0))),
                ('is_online', models.BooleanField(default=False)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('pmReadCaret', models.ManyToManyField(blank=True, to='pm.Message')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['pk'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='forum.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'timestamp',
            },
        ),
        migrations.CreateModel(
            name='CategoryTimeStamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoryTimeStamps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TokenPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='categorytimestamp',
            unique_together=set([('user', 'category')]),
        ),
        migrations.AlterIndexTogether(
            name='categorytimestamp',
            index_together=set([('user', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together=set([('user', 'thread')]),
        ),
        migrations.AlterIndexTogether(
            name='bookmark',
            index_together=set([('user', 'thread')]),
        ),
    ]
