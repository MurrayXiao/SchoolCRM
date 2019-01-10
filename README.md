# SchoolCRM
一个学校的客户，学员，讲师及销售的管理系统


实现功能：

1、实现了不同角色管理，不同的角色有不同的权限，每个角色可以做的事情可以动态配置

2、细化的权限管理。利用其中的钩子函数，可以实现更细致的权限管理，如限制每个销售人员只能查看自己创建的客户信息等

3、实现了动态菜单管理，用户页面上显示的菜单都是动态生成的

4、其中kingadmin模块，实现了类似django admin的功能，且很多地方做了优化，可以实现通用的增删改查功能。




使用配置：
python3.6+
Django version 2.1.4+



使用方法：
python manage.py runserver 127.0.0.0.1:8000

登录页面：/kingadmin/login.html

username: root@163.com password: rootroot
