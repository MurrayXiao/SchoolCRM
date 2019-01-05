from django.forms import ModelForm


def create_dynamic_model_form(admin_class, form_add=False):
    """动态的生成modelform,并根据form_add状态判断生成的modelform是修改页面还是添加页面，以便在修改状态显示只读的数据且不可编辑，
    在添加页面可以添加数据（包含只读行)"""
    class Meta:
        model = admin_class.model
        fields = "__all__"
        if not form_add:#修改页面，设置只读属性有效
            exclude = admin_class.readonly_fields
            admin_class.form_add = False
            #因为自始至终admin_class实例只有一个，这里修改是为了避免上一次添加时将其改为了True
        else:#添加页面
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):
        #在动态生成的modelform中加入field对象参数，以便生成bootstrap中的效果
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})
        return ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm',(ModelForm,),{'Meta':Meta,'__new__':__new__})
    return dynamic_form
