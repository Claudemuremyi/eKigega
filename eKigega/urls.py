from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from authentication import views as custom_auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('signup/', custom_auth_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', custom_auth_views.logout_view, name='logout'),
]

