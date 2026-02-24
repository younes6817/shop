from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.register_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('', views.main_view, name='profile'),
]

