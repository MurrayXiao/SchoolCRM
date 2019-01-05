# from crm import models
from kingadmin.sites import site
from student import models
from kingadmin.sites import site
from kingadmin.admin_base import BaseKingAdmin
# print('student kingadmin')
#
# class CustomAdmin():
#     list_display = ['name', 'source', 'contact_type', 'contact', 'status','consultant', 'date']
#     list_filter = ['source', 'status', 'consultant']
#     serch_fields = ['contact', 'consultant__name']
#
# site.register(models.Userprofile, CustomAdmin)
# site.register(models.Menus)
# site.register(models.Role)

print('student kingadmin')

class TestAdmin(BaseKingAdmin):
    list_display=['name']

site.register(models.Test, TestAdmin)