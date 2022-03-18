from django.urls import path
from . import views

urlpatterns = [
    path('/<int:id>', views.AccountAPIView.as_view(), name='account'),
    path('', views.AccountsAPIView.as_view(), name='accounts')
]