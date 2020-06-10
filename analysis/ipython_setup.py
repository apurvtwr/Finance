import os, sys
import pathlib

project_root = pathlib.Path('.').absolute().parent
sys.path.insert(0, str(project_root))
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Finance.settings")
import django
django.setup()