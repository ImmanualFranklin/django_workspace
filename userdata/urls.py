from django.urls import path
from userdata.views import *

app_name = 'userdata'

urlpatterns = [
    
    path('registration/',RegistrationView.as_view()),
    path('login/',LoginView.as_view()),
    path('user/list',UserListing.as_view()),
    path('user/details/<int:pk>',ProfileUpdate.as_view()),
    
    
]