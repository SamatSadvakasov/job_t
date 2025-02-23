from django.urls import path
from .views import LogoutView, SignUp, SignIn, InfoView



urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup' ),
    path('signin/', SignIn.as_view(), name='signin'),
    path('info/', InfoView.as_view(), name='info'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

