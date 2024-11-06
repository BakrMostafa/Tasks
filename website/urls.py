"""pcapiproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from rest_framework import routers

from website.sitemaps import *
from . import views

router = routers.DefaultRouter()

sitemaps = {
    "static": StaticViewSitemap,
    # "cars": CarSitemap
}

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # SiteMap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # path('', index_page, name='index'),
    path('', views.index_page, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.global_search, name='global_search'),
    path('projects/', views.project_list, name='projects'),
    path('tasks/', views.task_list, name='tasks'),
    path('notes/', views.note_list, name='notes'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:pk>/update/', views.note_update, name='note_update'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('knowledge/', views.knowledge_base, name='knowledge'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('register/', views.register, name='register'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('knowledge/create/', views.knowledge_base_create, name='knowledge_base_create'),
    path('knowledge/<int:pk>/', views.knowledge_base_detail, name='knowledge_base_detail'),
    path('knowledge/<int:pk>/edit/', views.knowledge_base_update, name='knowledge_base_update'),
    path('knowledge/<int:pk>/delete/', views.knowledge_base_delete, name='knowledge_base_delete'),
    path('profile/', views.profile_view, name='profile'),
    path('projects/<slug:slug>/github/connect/', views.project_github_connect, name='project_github_connect'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/<slug:slug>/update/', views.project_update, name='project_update'),
    path('projects/<slug:slug>/delete/', views.project_delete, name='project_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/appearance/', views.appearance_settings, name='appearance_settings'),
    path('settings/integrations/', views.integration_settings, name='integration_settings'),
    path('settings/notifications/', views.notification_settings, name='notification_settings'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/user/<int:user_id>/', views.chat_detail, name='user_chat'),
    path('messages/project/<slug:project_slug>/', views.chat_detail, name='project_chat'),
    path('messages/send/', views.send_message, name='send_message'),
    path('project/<slug:slug>/chat/', views.load_project_chat, name='project_chat'),
]
