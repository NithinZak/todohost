from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('taskcreate', views.TaskCreate.as_view(), name='createtask'),
    path('register/', views.RegisterPage.as_view(), name='userregister'),
    path('', views.CustomLoginView.as_view(), name='login'),
    path('tasklist/', views.TaskList.as_view(), name='tasks'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('details/<int:pk>/',views.TaskDetailView.as_view(),name='taskdetails'),
    path('logout_page/',views.LogoutView.as_view(),name='logoutpage'),
    path('deletetask/<int:pk>',views.TaskDeleteView.as_view(),name='delete'),
    path('task_update/<int:pk>/',views.TaskUpdate.as_view(),name='updatetask'),  
    path('taskcompleted/<int:id>',views.TaskCompleted,name='taskcomplete')
]