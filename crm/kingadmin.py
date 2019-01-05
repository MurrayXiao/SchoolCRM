
from kingadmin.sites import site
from kingadmin.admin_base import BaseKingAdmin
from crm import models
print('crm kingadmin ............')

class CustomerAdmin(BaseKingAdmin):
    list_display = ['id','name','source','contact_type','contact','consultant','consult_content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']
    readonly_fields = ['contact','status']
    filter_horizontal = ['consult_course']
    actions = ['change_status',]
    def change_status(self, request, querysets):
        print("kingadmin action", self, request, querysets)
        querysets.update(status = 0)

site.register(models.CustomerInfo,CustomerAdmin)
site.register(models.Role)
site.register(models.Menus)
site.register(models.Userprofile)
site.register(models.StudyRecord)
site.register(models.Student)
site.register(models.CustomerFollowUp)
site.register(models.Course)
site.register(models.CourseRecord)
site.register(models.ClassList)
site.register(models.Branch)
