from django.urls import path
from .views import TaskView

urlpatterns = [
    path('create/', TaskView.as_view(), name='task-create'),
    # path('tasks/<int:pk>/', TaskView.as_view(), name='task-detail'),
]
