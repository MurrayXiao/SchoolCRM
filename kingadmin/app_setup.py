# import os,django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PerfectCRM.settings")
# django.setup()
from django import conf

print(conf.settings.INSTALLED_APPS)
def kingadmin_auto_discover():
    """用于引入app中kingadmin模块"""
    for app_name in conf.settings.INSTALLED_APPS:
        #mod = importlib.import_module(app_name, 'kingadmin')
        try:
            mod = __import__('%s.kingadmin' % app_name)
        except ImportError:
            pass

kingadmin_auto_discover()