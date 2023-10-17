from django.urls import path
from .views import login, signup, signout, update

urlpatterns = [
    path('', login, name="login"),
    path('signup/', signup, name="signup"),
    path('signout/', signout, name="signout"),
    path('update/', update, name="update" )
]