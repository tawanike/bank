from django.urls import path


from bank.authorize import views

urlpatterns = [
    path('', views.AuthAPIView.as_view(), name='auth'),
]
