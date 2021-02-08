from django.db import router
from django.urls import path, include


from . import views



urlpatterns = [


    path('/', views.index, name="home"),
    path('report/', views.report, name='report'),
    path('login/', views.loginUser, name="login"),
    path('logoutuser/', views.logoutuser, name="logoutuser"),
    path('departments/', views.departments, name="departments"),
    path('pbis/', views.pbis, name="pbis"),
    path('filter_pbi/', views.filter_pbi, name="filter_pbi"),
    path('export_to_excel/', views.export_to_excel, name="export_to_excel"),
    path('send_mail_content/', views.send_mail_content, name="send_mail_content"),
    path('filter_report/', views.filter_report, name="filter_report"),
    path('sprint_gecisi/', views.sprint_gecisi, name="sprint_gecisi"),
    path('sprint_gecisi_done/', views.sprint_gecisi_done, name="sprint_gecisi_done"),
    path('update_pbi/', views.update_pbi, name="update_pbi"),
    path('delete_pbi/', views.delete_pbi, name="delete_pbi"),
    path('add_pbi/', views.add_pbi, name="add_pbi"),
    path('adddepartments/', views.add_departments, name="adddepartments"),
    path('department_delete/<int:id>', views.delete_departments, name="department_delete"),
]
