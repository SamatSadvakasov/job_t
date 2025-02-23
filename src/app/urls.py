from django.urls import path
from .views import LogoutView, SignUp, SignIn, InfoView, Latency



urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup' ),
    path('signin/', SignIn.as_view(), name='signin'),
    path('info/', InfoView.as_view(), name='info'),
    path('latency/', Latency.as_view(), name='latency'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

