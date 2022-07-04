from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('signup/', views.signup, name="signup"),
	path('forgotpassword/', views.forgotpassword, name="forgotpassword"),
	path('resetpassword/', views.resetpassword, name="resetpassword"),
	path('signin/', views.signin, name="signin"),
]