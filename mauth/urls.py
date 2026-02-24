from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.loginPage, name="loginPage"),
    path('signup/', views.signupPage, name="signupPage"),
    path('logout/', views.logoutPage, name="logoutPage"),
]
