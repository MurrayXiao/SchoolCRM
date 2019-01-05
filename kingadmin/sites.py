from kingadmin.admin_base import BaseKingAdmin


class AdminSite():
    """用于注册用的类"""
    def __init__(self):
        self.enabled_admins = {}


    def register(self, model_class, admin_class = None):
        """注册admin表"""
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if not admin_class:#为了避免多个model共享一个BaseKingAdmin内存对象
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()

        admin_class.model = model_class #把model_class赋值给了admin_class

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class


site = AdminSite()

