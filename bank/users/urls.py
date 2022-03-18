from django.urls import path
from . import views


urlpatterns = [
    path('/<int:id>', views.UserAPIView.as_view(), name='user'),
    path('/<int:id>/admin', views.UserAdminAPIView.as_view(), name='admin-user-view'),
    path('', views.UsersAPIView.as_view(), name='users'),
]