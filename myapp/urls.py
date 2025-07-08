from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name="about"),
    path('projects/', views.projects, name="projects"),
    path('projects/<int:id>', views.project_detail, name="project_detail"),
    path('', views.index, name="home_page"),
    path('create', views.create, name="create"),
    path('task/<int:pk>/done/', views.done_task,  name='done_task'),  
    path('task/<int:pk>/delete/', views.delete_task,  name='delete_task'),  
    path('projects/<int:pk>/delete/', views.delete_project,  name='delete_project'),  
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]

