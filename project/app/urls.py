from django.urls import path
from .views import add_candidate, Edit_candidate, delete_candidate, view_candidate

urlpatterns = [
    path('', view_candidate, name='view_candidate'),
    path('add_candidate/', add_candidate, name='add_candidate'),
    path('edit_candidate/<int:pk>/', Edit_candidate, name='Edit_candidate'),
    path('delete_candidate/<int:pk>/', delete_candidate, name='delete_candidate'),
]