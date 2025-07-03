from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # ✅ Теперь это CustomLoginView
    path('logout/', views.CustomLoginView.as_view(), name='logout/'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]