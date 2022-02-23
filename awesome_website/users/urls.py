from django.urls import path,include
from . import views
# from .views import HomePageView


urlpatterns = [
    path('project_form/', views.project_form,name='project_form'),
    path('emp_active/', views.empoyee_check,name='empoyee_check'),
    path('assign_task/', views.assign_task,name='assign_task'),
    path('assign_previous/',views.assign_previous, name ="assign_previous"),
    path('check_inac/', views.check_inac,name='check_inac'),
    path('assigned/', views.assigned,name='assigned'),
    path('project_close/',views.project_close, name="project_close"),
    path('reassign_task/',views.reassign_task, name="reassign_task"),
    path('create_person/',views.create_person, name="create_person"),
    path('overall_data/',views.overall_data, name="overall_data")
    
    

             
             ]