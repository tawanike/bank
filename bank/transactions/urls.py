from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('/<int:id>', views.TransactionAPIView.as_view(), name='transaction'),
    path('', views.TransactionsAPIView.as_view(), name='transactions'),

]