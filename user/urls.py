from django.urls import path
from .views import signup_view, UserLogin, logout_view, profile_view


#app_name = 'user'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]