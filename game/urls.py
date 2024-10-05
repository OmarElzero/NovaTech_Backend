from django.urls import path,include
from game import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('unlock/<int:id>/', views.unlock_exoplanet, name='unlock_exoplanet'),
path('',include(router.urls)),
path('login/',views.login,name='login'),
path('logout/',views.logout,name='logout'),
path('t1/',views.test,name='test'),
path('t2/',views.test2,name='test'),

]
