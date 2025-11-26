from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

class AddressesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'addresses'
