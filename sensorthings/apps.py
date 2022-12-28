from django.apps import AppConfig


class SensorthingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sensorthings'
    api_prefix = 'stapi'
    api_versions = ['v1.1']
