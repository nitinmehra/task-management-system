from django.urls import path
from .views import TaskView

urlpatterns = [
    path('create/', TaskView.as_view(), name='task-create'),
    path('update/<int:id>/', TaskView.as_view(), name='task-update'),
    path('view/<int:id>/', TaskView.as_view(), name='task-details'),
    path('list/', TaskView.as_view(), name='task-list'),
    path('delete/<int:id>/', TaskView.as_view(), name='task-delete')
]
