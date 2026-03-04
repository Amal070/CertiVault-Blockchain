from django.contrib import admin
from django.urls import path, include
from users.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('institute/', include('institute.urls')),
    path('user/', include('users.urls')),
]
