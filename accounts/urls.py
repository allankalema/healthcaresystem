
from django.urls import path
from .views import *


urlpatterns = [
    path('',  base, name ='home' ),
    path('enter_code/',  enter_code, name ='enter_code' ),
    path('login/',  login_view, name ='login' ),
    path('forgot_password/',  forgot_password, name ='forgot_password' ),
    path('reset_password/',  reset_password, name ='reset_password' ),

    path('signup/', signup, name='signup'),
    path('additional-details/<int:user_id>/', additional_details, name='additional_details'),
    path('change-password/', change_password, name='change_password'),
    path('logout/', user_logout, name='logout'),
    
    
    
]
