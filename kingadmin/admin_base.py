from django.shortcuts import render,redirect
import json


class BaseKingAdmin():
    """默认kingadmin register注册时使用的基类"""
    def __init__(self):
        #添加默认的actions自带方法，在此添加是为了避免后面定制化方法actions，覆盖默认的方法
        self.actions.extend(self.default_actions)

    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []
    filter_horizontal = []
    list_per_page = 3
    default_actions = ['delete_selected_objs']
    actions = []

    def delete_selected_objs(self, request, querysets):
        #基类自带的actions中删除方法
        print('querysets',querysets)
        querysets_ids = json.dumps([i.id for i in querysets])
        return render(request, 'kingadmin/table_obj_delete.html',{'admin_class':self, 'objs':querysets,
                                                                  'querysets_ids':querysets_ids})
        #在保持URL不变的情况下，直接跳转到删除页面