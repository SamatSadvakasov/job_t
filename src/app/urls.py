from django.urls import include, path
from rest_framework import routers
from .views import LogoutView

router = routers.DefaultRouter()

# router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='logout'),

]

urlpatterns += router.urls
