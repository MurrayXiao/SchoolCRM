from django.contrib import admin
from crm import models

# Register your models here.

class Customeradmin(admin.ModelAdmin):
    list_display = ['name','contact_type','contact','source','consult_content','status','consultant','date']
    list_filter = ['contact_type','contact','status','date']
    search_fields = ['contact','status']
    readonly_fields = ['status', 'contact']
    filter_horizontal = ['consult_course']
    list_per_page = 5
    # actions = ['change_status',]
    # def change_status(self, *args, **kwargs):
    #     print('admin action', self,*,**kwargs)
    #     querysets.update(status=1)可以批量处理admin表格中的数据

admin.site.register(models.Branch)
admin.site.register(models.ClassList)
admin.site.register(models.CustomerInfo, Customeradmin)
admin.site.register(models.CourseRecord)
admin.site.register(models.Course)
admin.site.register(models.Userprofile)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Role)
admin.site.register(models.Student)
admin.site.register(models.StudyRecord)
admin.site.register(models.Menus)
