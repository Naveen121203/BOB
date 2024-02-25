from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from uauth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.hub),
    path('signup/',views.signup,name='signup'),
    path('logiin/',views.logiin),
    path('logouut/',views.logouut),
    path('upload',views.upload),
    path('likes/<str:id>',views.likes,name='Like'),
    path('#<str:id>',views.hub_post),
    path('profile/<str:id_user>',views.profile),
    path('delete/<str:id>',views.delete),
    path('search/',views.search,name='search'),

]
