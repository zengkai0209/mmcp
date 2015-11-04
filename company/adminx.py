# coding=utf-8
from xadmin import views
import xadmin
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, \
    Side
from xadmin.plugins.batch import BatchChangeAction
from xadmin.plugins.inline import Inline
from xadmin.views.base import CommAdminView , ModelAdminView
from xadmin.models import CompanyGroup
from models import Company

from django.template.response import TemplateResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from company.models import *
from material.models import *
from project.models import *
from document.models import *
from order.models import *
from workflow.models import *


class BaseSetting(object):
    enable_themes = False
    use_bootswatch = False
xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    site_title = u'材料管理云平台'
    
    def get_site_menu(self):
        return (
            
            {'title': '项目管理', 'icon': 'fa fa-briefcase',  'menus':(
                {'title': Project._meta.verbose_name, 'icon': 'fa fa-briefcase', 'url': self.get_model_url(Project, 'changelist'), 'perm': self.get_model_perm(Project, 'view')},
                {'title': '价格查询', 'icon': 'fa fa-search', 'url': '/material/price', 'perm': self.get_model_perm(OrderLine, 'search_price')},
            )},


            {'title': '材料管理', 'icon': 'fa fa-tasks',  'menus':(
                {'title': Category._meta.verbose_name, 'icon': 'fa fa-th-large', 'url': self.get_model_url(Category, 'changelist'), 'perm': self.get_model_perm(Category, 'view')},
                {'title': Unit._meta.verbose_name, 'icon': 'fa fa-flask', 'url': self.get_model_url(Unit, 'changelist'), 'perm': self.get_model_perm(Unit, 'view')},
                {'title': Brand._meta.verbose_name, 'icon': 'fa fa-sun-o', 'url': self.get_model_url(Brand, 'changelist'), 'perm': self.get_model_perm(Brand, 'view')},
                {'title': Material._meta.verbose_name, 'icon': 'fa fa-tasks', 'url': self.get_model_url(Material, 'changelist'), 'perm': self.get_model_perm(Material, 'view')},
                {'title': Vendor._meta.verbose_name, 'icon': 'fa fa-user', 'url': self.get_model_url(Vendor, 'changelist'), 'perm': self.get_model_perm(Vendor, 'change')},
            )},
                
            {'title': '材料申请', 'icon': 'fa fa-file-text-o', 'perm': self.get_model_perm(Document, 'view'), 'menus':(
                {'title': '材料选择', 'icon': 'fa fa-list-alt', 'url': self.get_model_url(SelectedLineItem, 'changelist'), 'perm': self.get_model_perm(SelectedLineItem, 'change')},                                                                                                   
                {'title': '材料申请单', 'icon': 'fa fa-file-text-o', 'url': self.get_model_url(Document, 'changelist'), 'perm': self.get_model_perm(Document, 'change')},
#                 {'title': '项目申请单名细', 'icon': 'fa fa-align-justify', 'url': self.get_model_url(DocumentLineItem, 'changelist'), 'perm': self.get_model_perm(DocumentLineItem, 'change')},
                {'title': '申请单查询', 'icon': 'fa fa-list-alt', 'url': '/project/apply/list'},
            )},
                
            {'title': '系统管理', 'icon': 'fa fa-wrench',  'menus':(
                {'title': '公司管理', 'icon': 'fa fa-home', 'url': self.get_model_url(Company, 'changelist'), 'perm': self.get_model_perm(Company, 'change')},
                {'title': '部门管理', 'icon': 'fa fa-users', 'url': self.get_model_url(CompanyGroup, 'changelist'), 'perm': self.get_model_perm(CompanyGroup, 'change')},
                {'title': '用户管理', 'icon': 'fa fa-user', 'url': self.get_model_url(Employee, 'changelist'), 'perm': self.get_model_perm(Employee, 'change')},
                {'title': '权限管理', 'icon': 'fa fa-lock', 'url': self.get_model_url(Permission, 'changelist'), 'perm': self.get_model_perm(Permission, 'view')},
            )},
                
            {'title': '工作流', 'icon': 'fa fa-folder-o',  'menus':(
                {'title': '流程', 'icon': 'fa fa-folder-o', 'url': self.get_model_url(Route, 'changelist'), 'perm': self.get_model_perm(Route, 'change')},
                {'title': '步骤', 'icon': 'fa fa-check-square-o', 'url': self.get_model_url(Actor, 'changelist'), 'perm': self.get_model_perm(Actor, 'change')},
                {'title': '步骤处理人', 'icon': 'fa fa-user', 'url': self.get_model_url(ActorUser, 'changelist'), 'perm': self.get_model_perm(ActorUser, 'change')},
            )},
        )
        
    menu_style = 'accordion'
    
xadmin.site.register(views.CommAdminView, GlobalSetting)


class CompanyAdmin(object):
    list_display = ('name', 'short_name', 'phone', 'fax', 'zip', 'address')
    list_display_links = ('name',)

    search_fields = ['name']

    actions = [BatchChangeAction, ]
    batch_fields = ('name',)
    
    def queryset(self):
        if self.user.is_superuser:
            return super(CompanyAdmin, self).queryset()
        else:   
            return super(CompanyAdmin, self).queryset().filter(name=self.user.company.name)

    
xadmin.site.register(Company, CompanyAdmin)  



 
