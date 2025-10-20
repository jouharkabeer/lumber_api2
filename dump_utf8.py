import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lumber_api.settings")  # <-- change this
django.setup()

with open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", "--all", "--indent", "2", stdout=f)
