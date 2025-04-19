from django.template.context_processors import request
from django.urls import path

from .views import *
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', reg_view, name='registration'),
    path('', CategoryList.as_view(), name='category-list'),
    path('api/overdue/', OverdueTasksAPIView.as_view(), name='overdue_tasks'),
    path('api/telegram-auth/', telegram_auth_view, name='telegram-auth'),
    path('profile/<username>', user_profile, name='user_profile'),  
    path('category-create/', CategoryCreate.as_view(), name='category-create'),
    path('category-<int:pk>/', CategoryTasks.as_view(), name='category_tasks'),
    path('category-<int:pk>/category-important/', category_important, name='category-important'),
    path('category-<int:pk>/category-delete/', CategoryDelete.as_view(), name='category-delete'),
    path('category-<int:category_id>/task-create/', TaskCreate.as_view(), name='task-create'),
    path('category-<int:category_id>/task-<int:pk>/task-update/', TaskUpdateView.as_view(), name='task-update'),
    path('category-<int:pk>/category-update/', CategoryUpdateView.as_view(), name="category-update"),
    path('category-<int:category_id>/task-<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),
    path('category-<int:category_id>/task-<int:pk>/important-item/', task_important, name='important-item'),
    path('category-<int:category_id>/task-<int:pk>/complete/', task_complete, name='task-complete'),
]