"""nazox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from nazox import views

urlpatterns = [
    # Menu
    
    path('',views.TrasplanteView.as_view(),name='trasplante'),# Trasplante   
    path('menu/eda',views.EdaView.as_view(),name='eda'),# Trasplante  
    path('menu/upload',views.UploadView,name='update'),# Trasplante  
    path('menu/',views.DashboardView.as_view(),name='dashboard'),# Dashboard
    path('menu/reportes',views.Reportes.as_view(),name='reportes'),# Trasplante   
    path('epi/epilepsia',views.EpilepsiaView.as_view(),name='epilepsia'),# Trasplante   
    path('epi/eda_epilepsia',views.EdaViewEpi.as_view(),name='eda_epilepsia'),# Trasplante  
    path('epi/eda_upload',views.UploadViewE,name='update_e'),# Trasplante  

    path('manual',views.Manual.as_view(),name='manual'),# Trasplante  

    path('menu/calendar',views.CalendarView.as_view(),name='calendar'),# Calender
    path('menu/chat',views.ChatView.as_view(),name='chat'),# Chat
    path('menu/app-kanban-board',views.KanbanBoardView.as_view(),name='app-kanban-board'),# Kanban Board
   
    # Apps 
    path('ecommerce/',include('ecommerce.urls')),# Ecommerce
    path('email/',include('mail.urls')),# Email
    path('layouts/',include('layouts.urls')),# Layout
    path('pages/',include('utility.urls')),# Utility
    path('components/',include('components.urls')),# Components
    path('authentication/',include('authentication.urls')),# Authentication
    
    path('admin/', admin.site.urls),# Admin
]
