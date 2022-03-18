from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Bank API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/users', include('bank.users.urls')),
    path('v1/auth', include('bank.authorize.urls')),
    path('v1/accounts', include('bank.accounts.urls')),
    path('v1/transactions', include('bank.transactions.urls')),
    path('v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
