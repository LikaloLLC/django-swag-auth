# Generated by Django 2.2.2 on 2021-05-18 13:54

import django.db.models.deletion
import encrypted_model_fields.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectorToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connector', models.CharField(max_length=30, verbose_name='connector')),
                ('token', encrypted_model_fields.fields.EncryptedTextField(
                    help_text='"oauth_token" (OAuth1) or access token (OAuth2)', verbose_name='token')),
                ('token_secret', encrypted_model_fields.fields.EncryptedTextField(blank=True,
                                                                                  help_text='"oauth_token_secret" (OAuth1) or refresh token (OAuth2)',
                                                                                  verbose_name='token secret')),
                ('expires_at', models.DateTimeField(blank=True, null=True, verbose_name='expires at')),
            ],
        ),
        migrations.CreateModel(
            name='SwaggerStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, help_text='Swagger URL', null=True, verbose_name='url')),
                ('token', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                            to='swagconnect.ConnectorToken', verbose_name='token')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
