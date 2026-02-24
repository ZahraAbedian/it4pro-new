from django.urls import path, include
from . import views
# from . import settings
# import static
# from mauth.urls import path, include 

urlpatterns = [
    path('', views.mainPage, name="mainPage"),
    path('questions/', views.questionsPage, name="questionsPage"),
    path('result/', views.resultPage, name="resultPage"),
    path('tasks/', views.taskPage, name="taskPage"),
    path('profile/', views.profilePage, name="profilePage"),
] 
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
