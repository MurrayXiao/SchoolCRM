from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import conf
import json
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from kingadmin import app_setup
from kingadmin.sites import site
from kingadmin import form_handle

# Create your views here.


app_setup.kingadmin_auto_discover()
    #自动发现并导入app中kingadmin模块,便于kingadmin模块迁移

@login_required
def app_index(request):
    """kingadmin首页"""
    return render(request, 'kingadmin/app_index.html', {'site':site})


@login_required
def app_components(request, app_name):
    """单个app内容页面"""
    return render(request, 'kingadmin/app_components.html', {'site':site, 'app_name':app_name})

def get_filter_result(request, querysets):
    """获取筛选结果"""
    filter_conditions = {}
    for key, val in request.GET.items():
        if key in ('_page','_o','_q'): continue
        if val:
            filter_conditions[key] = val
    print('filter_conditons', filter_conditions)
    return querysets.filter(**filter_conditions),filter_conditions


def get_orderby_result(request, querysets, admin_class):
    """排序"""
    current_ordered_column = {}
    orderby_index = request.GET.get('_o')
    if orderby_index:
        orderby_key = admin_class.list_display[abs(int(orderby_index))]
        current_ordered_column[orderby_key] = orderby_index#为了让前端知道当前排序的列
        if orderby_index.startswith('-'):
            orderby_key = '-' + orderby_key
        return querysets.order_by(orderby_key), current_ordered_column
    else:
        return querysets, current_ordered_column


def get_searched_result(request, querysets, admin_class):
    """获取搜索框的搜索结果，多组搜索之间是或的关系"""
    search_key = request.GET.get('_q')
    if search_key:
        q = Q()
        q.connector = 'OR'
        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains"%search_field, search_key))

        return querysets.filter(q)
    return querysets


@login_required
def table_obj_list(request, app_name, model_name):
    """取出指定model里的数据返回给前端"""
    admin_class = site.enabled_admins[app_name][model_name]

    if request.method == "POST":
        # print("request.POST",request.POST)
        selected_action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids'))
        # print('selected_action',selected_action,"selected_ids",selected_ids)
        if selected_action:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_class, selected_action)
            response = admin_action_func(request, selected_objs)
            if response:
                return response
        else:#删除页面
            if selected_ids: #这些选中的数据都要被删除
                admin_class.model.objects.filter(id__in=selected_ids).delete()

    querysets = admin_class.model.objects.all().order_by('-id')
    print("app_name",app_name,"model_name",model_name, "admin_class",admin_class, "querysets",querysets, 'admin_class',admin_class, 'admin_class_actions',admin_class.actions)
    querysets, filter_conditions = get_filter_result(request, querysets)
    admin_class.filter_conditions = filter_conditions

    #search queryset result
    querysets = get_searched_result(request, querysets, admin_class)
    admin_class.search_key = request.GET.get('_q','')

    #sorted querysets
    querysets, sorted_column = get_orderby_result(request, querysets, admin_class)

    paginator = Paginator(querysets, admin_class.list_per_page)
    #设置分页及每页显示行数
    page = request.GET.get('_page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        #如果输入数据不是整数，默认显示第一页
        querysets = paginator.page(1)
    except EmptyPage:
        #如果输入页码超过总页数范围，默认返回最后一页
        querysets = paginator.page(paginator.num_pages)

    print(request.GET)
    # print("admin class", admin_class.model)

    return render(request, 'kingadmin/table_obj_list.html', locals())


@login_required
def table_obj_change(request, app_name, model_name, obj_id):
    """kingadmin数据修改页"""
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == 'GET':
        form_obj = model_form(instance = obj)
        #将需要修改项的数据传到前端
    elif request.method =='POST':
        #判断修改的数据否符合规则，是的话保存并返回，不是的话返回前端错误信息
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kingadmin/%s/%s'%(app_name, model_name))
    return render(request, 'kingadmin/table_obj_change.html', locals())


@login_required
def table_obj_add(request, app_name, model_name):
    """kingadmin数据添加页"""
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class, form_add=True)
    if request.method == 'GET':
        form_obj = model_form()
    elif request.method == 'POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kingadmin/%s/%s' %(app_name, model_name))
    return render(request, 'kingadmin/table_obj_add.html', locals())


@login_required
def table_obj_delete(request, app_name, model_name, obj_id):
    """kingadmin数据删除页"""
    admin_class = site.enabled_admins[app_name][model_name]
    obj = admin_class.model.objects.get(id = obj_id)
    if request.method == 'GET':
        return render(request, 'kingadmin/table_obj_delete.html',locals())
    elif request.method == 'POST':
        obj.delete()
        return redirect('/kingadmin/%s/%s/'%(app_name, model_name))


def acc_login(request):
    """登录验证"""
    if request.method == 'GET':
        return render(request, 'kingadmin/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # print('pass authenticate', user, type(user), username, password)
            login(request, user)
            return redirect(request.POST.get('next','/kingadmin/'))
        else:
            errors_message = 'Wrong username or password!'
            return render(request, 'kingadmin/login.html', {'errors_message':errors_message})


def acc_logout(request):
    """退出登录"""
    logout(request)
    return redirect('kingadmin/login.html')


