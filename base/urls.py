from django.urls import path
from . import views  # import views.py

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('profile/<int:pk>/', views.userProfile, name='user-profile'),
    
    path('', view=views.home, name="home"),  # (root directory di app) home page 
    path('room/<str:pk>/' , view=views.room, name="room"),  # string primary key, it also can be int, slug
    
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room'),
    
    path('delete-message/<int:pk>/', views.deleteMessage, name='delete-message'),
    path('update-message/<int:pk>/', views.updateMessage, name='update-message'),
    
    path('update-user/', views.updateUser, name='update-user'),
    
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
    
    path('testing/', views.test, name='test'),
]