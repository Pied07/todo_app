from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TaskList, basename='task')

urlpatterns = [
    path('',views.home,name="home"),
    path('delete_all/',views.delete_all,name="delete_all"),
    path('register/',views.register,name='register'),
    path('login/',views.Login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('edit/<int:task_id>/',views.edit,name="edit"),
    path('tasks_lists/', include(router.urls)),
    path('api_key/',views.display_api_key,name="task_api"),
    path('api_docs/',views.api_docs,name="api_docs"),
]