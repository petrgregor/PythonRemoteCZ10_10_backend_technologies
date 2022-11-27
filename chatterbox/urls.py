"""chatterbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# for images
from django.conf import settings
from django.conf.urls.static import static

from chatterapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello, name='hello'),
    path('hello/<str:name>', hello, name='hello2'),
    path('ahoj/', ahoj, name='ahoj'),
    path('', home, name='home'),        # empty path (home)
    path('rooms/', rooms, name='rooms'),
    path('room/<int:pk>/', room, name='room'),
    path('new_room/', new_room, name='new_room'),                   # 1st version for creating room
    path('create_room/', create_room, name='create_room'),          # 1st version for creating room
    path('create_room_v2/', create_room_v2, name='create_room_v2'), # 2st version for creating room
    path('create_room_v3/', RoomFormView.as_view(), name='create_room_v3'),   # 3rd version for creating room
    path('create_room_v4/', RoomCreateView.as_view(), name='create_room_v4'),  # 4rd version for creating room

    path('delete_room/<int:pk>/', delete_room, name='delete_room'),
    path('delete_room_yes/<int:pk>', delete_room_yes, name='delete_room_yes'),

    # accounts app
    path('accounts/', include('accounts.urls')),             # signup
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password_change,...
    path('accounts/profile/', rooms),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
