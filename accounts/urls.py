
from django.urls import path
from .views import *


urlpatterns = [
    path('',  base, name ='home' ),
    path('enter_code/',  enter_code, name ='enter_code' ),
    path('login/',  login_view, name ='login' ),
    path('forgot_password/',  forgot_password, name ='forgot_password' ),
    path('reset_password/',  reset_password, name ='reset_password' ),

    path('signup/patient/', signup, name='signup'),
    
    
    
]
