from django.template import Library
from django.utils.safestring import mark_safe
import datetime, time

register = Library()
#只有想系统注册过的tags，系统才能识别

@register.simple_tag #加上这句，就是一个合格的template tags了
#这个装饰器表明这个函数是一个模板标签
def get_model_verbose_name(admin_class):
    """在面包屑中显示中文昵称"""
    return admin_class.model._meta.verbose_name


@register.simple_tag
def build_filter_ele(filter_column, admin_class):
    """创建过滤元素"""
    column_obj = admin_class.model._meta.get_field(filter_column)
    # print('column obj',column_obj)
    try:
        filter_ele ="<div class='col-md-2'>%s<select class='form-control' name='%s'>" %(filter_column,filter_column)
        for choice in column_obj.get_choices():
            selected = ""
            if filter_column in admin_class.filter_conditions:#当前字段被过滤了
                # print("filter_column", choice,
                #         type(admin_class.filter_conditions.get(filter_column)),
                #         admin_class.filter_conditions.get(filter_column)
                if str(choice[0]) == admin_class.filter_conditions.get(filter_column):#当前值被选中了
                    selected = 'selected'
            option = "<option value='%s' %s>%s</option>" %(choice[0], selected, choice[1])
            filter_ele += option
    except AttributeError as e:
        # print('err', e)
        filter_ele = "<div class='col-md-2'>%s<select class='form-control' name = '%s__gte'>" %(filter_column,filter_column)
        #按照时间元素筛选
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ['','--------'],
                [time_obj,'Today'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), 'YearToDay(YTD)'],
                ['','All'],
            ]

            for i in time_list:
                selected = ''
                time_to_str = '' if not i[0] else "%s-%s-%s"%(i[0].year, i[0].month, i[0].day)
                if "%s__gte" %filter_column in admin_class.filter_conditions:#当前字段被过滤了
                    if time_to_str == admin_class.filter_conditions.get("%s__gte" %filter_column):#当前值被选中了
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>"%(time_to_str, selected, i[1])
                filter_ele += option

    filter_ele += '</select></div>'
    return mark_safe(filter_ele)


@register.simple_tag
def build_table_row(obj, admin_class):
    """生成一条记录的html element"""
    ele = ""
    if admin_class.list_display:
        for index, column_name in enumerate(admin_class.list_display):
            column_obj = admin_class.model._meta.get_field(column_name)
            if column_obj.choices:#get_xxx_display
                column_data = getattr(obj, 'get_%s_display' %column_name)()
            else:
                column_data = getattr(obj, column_name)
            td_ele = "<td>%s</td>" % column_data
            if index == 0:
                td_ele = "<td><a href='%s/change/'>%s</td>"%(obj.id, column_data)
            ele += td_ele
    else:
        td_ele = '<td><a href="%s/change/">%s</td>'%(obj.id, obj)
        ele += td_ele

    return mark_safe(ele)


@register.simple_tag
def get_model_name(admin_class):
    """当没有自定制admin时在页面中显示数据库表名"""
    return admin_class.model._meta.model_name.upper()


@register.simple_tag
def get_sorted_column(column, sorted_column, forloop):
    #进行排序并返回给前端
    #sorted_column = {'name':'-0'}
    if column in sorted_column:#这一列排序了
        #需要判断上一次排序是什么顺序，本次取反
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            this_time_sort_index = last_sort_index.strip('-')
        else:
            this_time_sort_index = '-%s' %last_sort_index
        return this_time_sort_index
    else:
        return forloop


@register.simple_tag
def render_filtered_args(admin_class, render_html=True):
    """拼接筛选条件"""
    if admin_class.filter_conditions:
        ele = ''
        for k, v in admin_class.filter_conditions.items():
            ele += '&%s=%s' %(k, v)
        if render_html:
            return mark_safe(ele)
        else:
            return ele
        # return mark_safe(ele)
    else:
        return ''


@register.simple_tag
def render_sorted_arrow(column, sorted_column):
    """渲染被筛选列旁边的升序或降序图标"""
    if column in sorted_column: #这一列被排序了
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden='true'></span>'''%arrow_direction
        return mark_safe(ele)
    return ''


@register.simple_tag
def render_paginator(querysets, admin_class, sorted_column):
    """渲染分页效果"""
    ele ='''<ul class='pagination'>'''
    for i in querysets.paginator.page_range:
        if abs(querysets.number - i) < 2:#设置显示的页数，绝对值小于2代表最多显示3页
            active = ''
            if querysets.number == i: #当前页，设置页码加深颜色
                active = 'active'
            filter_ele = render_filtered_args(admin_class)#进行条件拼接，设置在筛选和排序的基础上进行分页
            sorted_ele = ''
            if sorted_column:
                sorted_ele = '&_o=%s' %list(sorted_column.values())[0]
            p_ele = '''<li class="%s"><a href="?_page=%s%s%s">%s</a></li>''' %(active,i,filter_ele,sorted_ele,i)
            ele += p_ele
    ele += '''</ul>'''
    return  mark_safe(ele)


@register.simple_tag
def get_current_sorted_column_index(sorted_column):
    #获取当前筛选列索引
    return list(sorted_column.values())[0] if sorted_column else ''


@register.simple_tag
def get_obj_field_value(form_obj, field):
    #获取只读行数据
    return getattr(form_obj.instance, field)
    #通过反射，获取数据库实例中field这一行的数据


@register.simple_tag
def get_available_m2m_data(field_name, form_obj, admin_class):
    """返回的是m2m字段关联表的所有数据与已选中的数据的差集"""
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())
    #m2m字段关联表的所有数据集合
    if form_obj.instance.id:
        #判断是在修改页面调用还是添加页面调用，以便返回不同的结果
        selected_data = set(getattr(form_obj.instance, field_name).all())
        #已选中的数据的集合
        return obj_list - selected_data
        #返回差集
    else:
        return obj_list


@register.simple_tag
def get_selected_m2m_data(field_name, form_obj, admin_class):
    """返回已选的m2m数据"""
    if form_obj.instance.id:
    # 判断是在修改页面调用还是添加页面调用，以便返回不同的结果
        selected_data = getattr(form_obj.instance, field_name).all()
        return selected_data
    else:
        return []


@register.simple_tag
def display_all_related_objs(obj):
    """返回要被删除对象的所有关联对象"""
    ele = "<ul><b style='color:red'>%s</b>"%obj
    for reversed_fk_obj in obj._meta.related_objects:
        related_table_name = reversed_fk_obj.name
        related_lookup_key = "%s_set" %related_table_name
        related_objs = getattr(obj, related_lookup_key).all()#反向查找所有关联的数据
        ele += "<li>%s<ul>" %related_table_name
        if reversed_fk_obj.get_internal_type() == "ManyToManyField" : #不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a>记录里与[%s]相关的数据将被删除"%(i._meta.
                                                                        app_label, i._meta.model_name, i.id, i, obj)
        else:
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>"%(i._meta.app_label,
                                                                                i._meta.model_name,i.id,i)
                ele += display_all_related_objs(i)
        ele += "</ul></li>"
    ele += "</ul>"
    return ele


@register.simple_tag
def get_distinct_actions_options(admin_class):
    """获取去重后的actions选项返回给前端"""
    return set(admin_class.actions)






























